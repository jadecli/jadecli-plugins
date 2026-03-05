import { mkdirSync, writeFileSync, readFileSync, existsSync, readdirSync } from "fs";
import { join, relative } from "path";

export interface ArtifactStore {
  readonly baseDir: string;
  ensureDir(): void;
  write(filename: string, content: string): string;
  read(filename: string): string | null;
  list(): string[];
  indexPath(): string;
  writeIndex(content: string): string;
}

export function createArtifactStore(baseDir: string): ArtifactStore {
  return {
    baseDir,

    ensureDir() {
      mkdirSync(baseDir, { recursive: true });
    },

    write(filename: string, content: string): string {
      this.ensureDir();
      const fullPath = join(baseDir, filename);
      writeFileSync(fullPath, content, "utf-8");
      return fullPath;
    },

    read(filename: string): string | null {
      const fullPath = join(baseDir, filename);
      if (!existsSync(fullPath)) return null;
      return readFileSync(fullPath, "utf-8");
    },

    list(): string[] {
      if (!existsSync(baseDir)) return [];
      return readdirSync(baseDir).filter((f: string) => !f.startsWith("."));
    },

    indexPath(): string {
      return join(baseDir, "SUMMARY.md");
    },

    writeIndex(content: string): string {
      return this.write("SUMMARY.md", content);
    },
  };
}

export function resolveArtifactDir(
  artifactsRoot: string,
  missionName: string,
  timestamp?: string,
): string {
  const ts = timestamp ?? new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  return join(artifactsRoot, missionName, ts);
}
