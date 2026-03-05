import { writeFileSync } from "fs";
import { join } from "path";

export interface RunLog {
  mission: string;
  objective: string;
  startedAt: string;
  completedAt?: string;
  status: "running" | "completed" | "failed" | "aborted";
  artifactDir: string;
  leadModel: string;
  workerCount: number;
  pattern: string;
  artifacts: string[];
  error?: string;
  durationMs?: number;
}

export function createRunLog(params: {
  mission: string;
  objective: string;
  artifactDir: string;
  leadModel: string;
  workerCount: number;
  pattern: string;
}): RunLog {
  return {
    ...params,
    startedAt: new Date().toISOString(),
    status: "running",
    artifacts: [],
  };
}

export function completeRunLog(log: RunLog, artifacts: string[]): RunLog {
  const now = new Date();
  const started = new Date(log.startedAt);
  return {
    ...log,
    completedAt: now.toISOString(),
    status: "completed",
    artifacts,
    durationMs: now.getTime() - started.getTime(),
  };
}

export function failRunLog(log: RunLog, error: string): RunLog {
  const now = new Date();
  const started = new Date(log.startedAt);
  return {
    ...log,
    completedAt: now.toISOString(),
    status: "failed",
    error,
    durationMs: now.getTime() - started.getTime(),
  };
}

export function writeRunLog(artifactDir: string, log: RunLog): string {
  const logPath = join(artifactDir, "run.json");
  writeFileSync(logPath, JSON.stringify(log, null, 2), "utf-8");
  return logPath;
}
