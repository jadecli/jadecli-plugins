import { join, resolve } from "path";
import { loadMission, listMissions } from "./mission-loader.js";
import { buildOrchestrationPlan } from "./agent-builder.js";
import { estimateMissionCost, checkBudget, type ModelTier } from "./model-router.js";
import { createArtifactStore, resolveArtifactDir } from "./artifact-store.js";
import { createRunLog, completeRunLog, failRunLog, writeRunLog } from "./logger.js";
import { evaluateArtifacts, formatEvaluation } from "./evaluator.js";

const PLUGIN_ROOT = resolve(join(import.meta.dirname, "..", ".."));
const MISSIONS_DIR = join(PLUGIN_ROOT, "missions");
const ARTIFACTS_DIR = join(PLUGIN_ROOT, "artifacts");

interface CliArgs {
  mission?: string;
  objective?: string;
  dryRun: boolean;
  budget?: number;
  tier?: string;
  list: boolean;
}

function parseArgs(args: string[]): CliArgs {
  const result: CliArgs = { dryRun: false, list: false };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--mission":
        result.mission = args[++i];
        break;
      case "--dry-run":
        result.dryRun = true;
        break;
      case "--budget":
        result.budget = parseFloat(args[++i]);
        break;
      case "--tier":
        result.tier = args[++i];
        break;
      case "--list":
        result.list = true;
        break;
      default:
        if (!args[i].startsWith("--") && !result.objective) {
          result.objective = args[i];
        }
    }
  }

  return result;
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.list) {
    const missions = listMissions(MISSIONS_DIR);
    console.log("Available missions:");
    for (const m of missions) {
      console.log(`  - ${m}`);
    }
    return;
  }

  if (!args.mission) {
    console.error("Usage: orchestrator --mission <name> [objective] [--dry-run] [--budget N] [--tier T]");
    console.error("       orchestrator --list");
    process.exit(1);
  }

  const missionPath = join(MISSIONS_DIR, `${args.mission}.yaml`);
  const mission = loadMission(missionPath);

  console.log(`Mission: ${mission.name}`);
  console.log(`Description: ${mission.description}`);
  console.log(`Pattern: ${mission.pattern}`);
  console.log(`Lead model: ${mission.lead.model}`);
  console.log(`Worker roles: ${Object.keys(mission.workers).join(", ")}`);

  if (mission.scaling) {
    console.log("\nScaling tiers:");
    for (const [tier, cfg] of Object.entries(mission.scaling)) {
      console.log(`  ${tier}: ${cfg.agents} agents, ${cfg.max_tool_calls} max calls`);
    }
  }

  const firstWorker = Object.values(mission.workers)[0];
  const workerCount = typeof firstWorker.count === "number" ? firstWorker.count : 3;
  const cost = estimateMissionCost(
    mission.lead.model as ModelTier,
    firstWorker.model as ModelTier,
    workerCount,
  );
  console.log("\nCost estimate:");
  console.log(cost.breakdown);

  if (args.budget) {
    const budgetCheck = checkBudget(args.budget, cost);
    console.log(`\nBudget: ${budgetCheck.message}`);
    if (!budgetCheck.ok && !args.dryRun) {
      console.error("Aborting: budget insufficient. Use --dry-run to see plan anyway.");
      process.exit(1);
    }
  }

  if (args.dryRun) {
    const objective = args.objective ?? "(no objective provided)";
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const artifactDir = join(ARTIFACTS_DIR, mission.name, timestamp);

    const plan = buildOrchestrationPlan(mission, objective, artifactDir);
    console.log("\n--- Dry Run: Orchestration Plan ---");
    console.log(`Artifact directory: ${artifactDir}`);
    console.log(`Lead model: ${plan.leadModel}`);
    console.log(`Lead tools: ${plan.leadTools.join(", ")}`);
    console.log(`Pattern: ${plan.pattern}`);
    console.log(`Workers: ${Object.keys(plan.workers).join(", ")}`);
    console.log("\nLead system prompt (first 500 chars):");
    console.log(plan.leadSystemPrompt.slice(0, 500));
    console.log("\n--- End Dry Run ---");
    return;
  }

  if (!args.objective) {
    console.error("\nError: objective required for live run. Use --dry-run for validation only.");
    process.exit(1);
  }

  await runLive(mission, args.objective!, args.budget);
}

async function runLive(
  mission: ReturnType<typeof loadMission>,
  objective: string,
  budget?: number,
): Promise<void> {
  const artifactDir = resolveArtifactDir(ARTIFACTS_DIR, mission.name);
  const store = createArtifactStore(artifactDir);
  store.ensureDir();

  const plan = buildOrchestrationPlan(mission, objective, artifactDir);

  const firstWorker = Object.values(mission.workers)[0];
  const workerCount = typeof firstWorker.count === "number" ? firstWorker.count : 3;

  const runLog = createRunLog({
    mission: mission.name,
    objective,
    artifactDir,
    leadModel: plan.leadModel,
    workerCount,
    pattern: plan.pattern,
  });
  writeRunLog(artifactDir, runLog);

  console.log(`\nArtifact directory: ${artifactDir}`);
  console.log("Starting lead agent...\n");

  let aborted = false;
  const sigintHandler = () => {
    if (aborted) {
      console.error("\nForce quit.");
      process.exit(2);
    }
    aborted = true;
    console.error("\nSIGINT received. Gracefully aborting... (press Ctrl+C again to force quit)");
    const abortLog = failRunLog(runLog, "Aborted by user (SIGINT)");
    abortLog.status = "aborted";
    writeRunLog(artifactDir, abortLog);
  };
  process.on("SIGINT", sigintHandler);

  try {
    const { query } = await import("@anthropic-ai/claude-agent-sdk");

    const agentDefs: Record<string, { description: string; prompt: string; tools: string[] }> = {};
    for (const [role, def] of Object.entries(plan.workers)) {
      agentDefs[role] = {
        description: def.description,
        prompt: def.prompt,
        tools: def.tools,
      };
    }

    for await (const message of query({
      prompt: objective,
      options: {
        systemPrompt: plan.leadSystemPrompt,
        allowedTools: plan.leadTools,
        model: plan.leadModel,
        agents: agentDefs,
        cwd: PLUGIN_ROOT,
        permissionMode: "acceptEdits",
        maxTurns: 50,
        ...(budget != null ? { maxBudgetUsd: budget } : {}),
      },
    })) {
      if ("result" in message) {
        console.log("\n--- Mission Result ---");
        console.log(message.result);
      }
    }

    const artifacts = store.list();
    const finalLog = completeRunLog(runLog, artifacts);
    writeRunLog(artifactDir, finalLog);

    console.log(`\n--- Mission Complete ---`);
    console.log(`Artifacts: ${artifacts.length} files in ${artifactDir}`);
    console.log(`Duration: ${finalLog.durationMs}ms`);
    if (store.read("SUMMARY.md")) {
      console.log(`Summary: ${store.indexPath()}`);
    }

    // Post-run evaluation
    const evalResult = evaluateArtifacts(mission, artifactDir);
    console.log(`\n${formatEvaluation(evalResult)}`);
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    const finalLog = failRunLog(runLog, errorMsg);
    writeRunLog(artifactDir, finalLog);
    console.error(`\nMission failed: ${errorMsg}`);
    process.exit(1);
  } finally {
    process.removeListener("SIGINT", sigintHandler);
  }
}

main();
