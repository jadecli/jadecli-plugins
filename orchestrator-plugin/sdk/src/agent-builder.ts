import type { Mission, Worker } from "./mission-schema.js";
import { resolveModel, type ModelTier } from "./model-router.js";

export interface AgentDefinition {
  description: string;
  prompt: string;
  tools: string[];
  model?: string;
}

export interface OrchestrationPlan {
  leadModel: string;
  leadSystemPrompt: string;
  leadTools: string[];
  workers: Record<string, AgentDefinition>;
  pattern: string;
}

function buildLeadPrompt(mission: Mission, objective: string, artifactDir: string): string {
  const scalingRules = mission.scaling
    ? Object.entries(mission.scaling)
        .map(([tier, cfg]) => `  ${tier}: ${cfg.agents} agents, ${cfg.max_tool_calls} max tool calls`)
        .join("\n")
    : "  No scaling rules defined. Use your judgment.";

  const workerRoles = Object.keys(mission.workers).join(", ");

  return `You are the lead orchestrator for the "${mission.name}" mission.

OBJECTIVE: ${objective}

MISSION: ${mission.description}

STRATEGY:
${mission.lead.strategy}

SCALING RULES:
${scalingRules}

AVAILABLE WORKER ROLES: ${workerRoles}

PATTERN: ${mission.pattern}

ARTIFACT DIRECTORY: ${artifactDir}

INSTRUCTIONS:
1. Assess the complexity of the objective
2. Select the appropriate scaling tier
3. Decompose the objective into worker tasks
4. Spawn workers using the Agent tool with the defined roles
5. Each worker writes to ${artifactDir}/ and returns the file path
6. Read all worker artifact files
7. Synthesize results into ${artifactDir}/SUMMARY.md

Each worker writes findings to a file in the artifact directory.
${mission.pattern === "parallel" ? "Spawn all workers in parallel, then synthesize." : "Run workers SEQUENTIALLY -- each step depends on prior outputs. Wait for each worker to complete before spawning the next."}
After all workers complete, read their outputs and write SUMMARY.md with
a synthesized view. SUMMARY.md structure:

# {Mission}: {Objective}
## Executive Summary
## Detailed Findings
## Sources
## Methodology`;
}

function buildWorkerPrompt(
  role: string,
  worker: Worker,
  artifactDir: string,
  options?: { sequenceIndex?: number; priorArtifacts?: string[] },
): string {
  const constraints = worker.constraints?.join("\n- ") ?? "None";
  const sections = worker.artifact_schema?.required_sections?.join(", ") ?? "freeform";
  const prefix = options?.sequenceIndex != null ? `[Step ${options.sequenceIndex + 1}] ` : "";

  let priorContext = "";
  if (options?.priorArtifacts?.length) {
    priorContext = `\nPRIOR ARTIFACTS (read these before starting):
${options.priorArtifacts.map((p) => `- ${p}`).join("\n")}
`;
  }

  return `${prefix}You are a worker agent with role: ${role}

OUTPUT FORMAT: ${worker.artifact_schema?.format ?? "markdown"}
REQUIRED SECTIONS: ${sections}

CONSTRAINTS:
- ${constraints}
${priorContext}
Write your output to a file in: ${artifactDir}
Use filename pattern: ${role}-findings.md
Return ONLY the file path after writing.`;
}

export function buildOrchestrationPlan(
  mission: Mission,
  objective: string,
  artifactDir: string,
): OrchestrationPlan {
  const workers: Record<string, AgentDefinition> = {};
  const isSequential = mission.pattern === "sequential" || mission.pattern === "pipeline";
  const roles = Object.entries(mission.workers);

  for (let i = 0; i < roles.length; i++) {
    const [role, worker] = roles[i];
    const priorRoles = isSequential ? roles.slice(0, i).map(([r]) => `${artifactDir}/${r}-findings.md`) : undefined;

    workers[role] = {
      description: `${isSequential ? `[Step ${i + 1}/${roles.length}] ` : ""}${role} worker for ${mission.name} mission`,
      prompt: buildWorkerPrompt(role, worker, artifactDir, {
        sequenceIndex: isSequential ? i : undefined,
        priorArtifacts: priorRoles,
      }),
      tools: worker.tools,
      model: resolveModel(worker.model as ModelTier),
    };
  }

  return {
    leadModel: resolveModel(mission.lead.model as ModelTier),
    leadSystemPrompt: buildLeadPrompt(mission, objective, artifactDir),
    leadTools: [...mission.lead.tools, "Agent"],
    workers,
    pattern: mission.pattern,
  };
}
