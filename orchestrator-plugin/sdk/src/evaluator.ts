import { readFileSync, existsSync } from "fs";
import type { Mission } from "./mission-schema.js";

export interface EvaluationResult {
  passed: boolean;
  score: number;
  checks: EvaluationCheck[];
}

export interface EvaluationCheck {
  name: string;
  passed: boolean;
  message: string;
}

export function evaluateArtifacts(
  mission: Mission,
  artifactDir: string,
): EvaluationResult {
  const checks: EvaluationCheck[] = [];

  // Check index file exists
  const indexFile = mission.artifacts?.index ?? "SUMMARY.md";
  const indexPath = `${artifactDir}/${indexFile}`;
  const indexExists = existsSync(indexPath);
  checks.push({
    name: "index_exists",
    passed: indexExists,
    message: indexExists
      ? `Index file ${indexFile} found`
      : `Missing index file: ${indexFile}`,
  });

  // Check index has content
  if (indexExists) {
    const content = readFileSync(indexPath, "utf-8");
    const hasContent = content.trim().length > 100;
    checks.push({
      name: "index_has_content",
      passed: hasContent,
      message: hasContent
        ? `Index file has ${content.length} characters`
        : `Index file is too short (${content.length} chars)`,
    });

    // Check required sections in worker artifacts
    for (const [role, worker] of Object.entries(mission.workers)) {
      const sections = worker.artifact_schema?.required_sections;
      if (!sections) continue;

      const workerFiles = findWorkerArtifacts(artifactDir, role);
      if (workerFiles.length === 0) {
        checks.push({
          name: `${role}_artifacts_exist`,
          passed: false,
          message: `No artifacts found for worker role: ${role}`,
        });
        continue;
      }

      for (const file of workerFiles) {
        const fileContent = readFileSync(file, "utf-8").toLowerCase();
        for (const section of sections) {
          const found = fileContent.includes(section.toLowerCase()) ||
            fileContent.includes(`## ${section.toLowerCase()}`);
          checks.push({
            name: `${role}_section_${section}`,
            passed: found,
            message: found
              ? `Section "${section}" found in ${file}`
              : `Missing section "${section}" in ${file}`,
          });
        }
      }
    }
  }

  // Check evaluation criteria if defined
  if (mission.evaluation?.criteria) {
    for (const criterion of mission.evaluation.criteria) {
      checks.push({
        name: `criterion_${criterion}`,
        passed: true, // Criteria are advisory; lead agent handles actual evaluation
        message: `Criterion "${criterion}" noted (evaluated by lead agent)`,
      });
    }
  }

  const passed = checks.filter((c) => c.passed).length;
  const total = checks.length;
  const score = total > 0 ? passed / total : 0;

  return {
    passed: score >= 0.7,
    score,
    checks,
  };
}

function findWorkerArtifacts(artifactDir: string, role: string): string[] {
  if (!existsSync(artifactDir)) return [];
  const { readdirSync } = require("fs") as typeof import("fs");
  return readdirSync(artifactDir)
    .filter((f: string) => f.startsWith(role) && !f.startsWith("."))
    .map((f: string) => `${artifactDir}/${f}`);
}

export function formatEvaluation(result: EvaluationResult): string {
  const lines = [
    `Evaluation: ${result.passed ? "PASSED" : "FAILED"} (score: ${(result.score * 100).toFixed(0)}%)`,
    "",
  ];

  for (const check of result.checks) {
    const icon = check.passed ? "[ok]" : "[!!]";
    lines.push(`  ${icon} ${check.name}: ${check.message}`);
  }

  return lines.join("\n");
}
