import { readFileSync, readdirSync } from "fs";
import { join, basename } from "path";
import { parse as parseYaml } from "yaml";
import { MissionSchema, type Mission } from "./mission-schema.js";

export class MissionLoadError extends Error {
  constructor(
    public readonly missionPath: string,
    public readonly cause: unknown,
  ) {
    const msg = cause instanceof Error ? cause.message : String(cause);
    super(`Failed to load mission ${missionPath}: ${msg}`);
    this.name = "MissionLoadError";
  }
}

export function loadMission(missionPath: string): Mission {
  let raw: string;
  try {
    raw = readFileSync(missionPath, "utf-8");
  } catch (err) {
    throw new MissionLoadError(missionPath, err);
  }

  let parsed: unknown;
  try {
    parsed = parseYaml(raw);
  } catch (err) {
    throw new MissionLoadError(missionPath, `YAML parse error: ${err}`);
  }

  const result = MissionSchema.safeParse(parsed);
  if (!result.success) {
    const issues = result.error.issues
      .map((i) => `  ${i.path.join(".")}: ${i.message}`)
      .join("\n");
    throw new MissionLoadError(missionPath, `Validation errors:\n${issues}`);
  }

  return result.data;
}

export function listMissions(missionsDir: string): string[] {
  try {
    return readdirSync(missionsDir)
      .filter((f: string) => f.endsWith(".yaml") && !f.startsWith("_"))
      .map((f: string) => basename(f, ".yaml"));
  } catch {
    return [];
  }
}
