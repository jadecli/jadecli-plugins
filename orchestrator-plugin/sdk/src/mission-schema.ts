import { z } from "zod";

const ScalingTierSchema = z.object({
  agents: z.number().int().min(1).max(20),
  max_tool_calls: z.number().int().min(1).max(100),
});

const ArtifactSchemaSchema = z.object({
  format: z.enum(["markdown", "json", "yaml", "text"]),
  required_sections: z.array(z.string()).optional(),
});

const WorkerSchema = z.object({
  model: z.enum(["opus", "sonnet", "haiku"]).default("sonnet"),
  count: z.union([z.number().int().min(1), z.literal("dynamic")]),
  tools: z.array(z.string()),
  artifact_schema: ArtifactSchemaSchema.optional(),
  constraints: z.array(z.string()).optional(),
});

const EvaluationSchema = z.object({
  method: z.enum(["lead_synthesis", "checklist", "none"]).default("lead_synthesis"),
  criteria: z.array(z.string()).optional(),
});

const ArtifactsConfigSchema = z.object({
  directory: z.string().default("artifacts/{mission_name}/{timestamp}"),
  index: z.string().default("SUMMARY.md"),
  worker_prefix: z.string().default("{role}-{n}"),
});

export const MissionSchema = z.object({
  name: z.string().min(1),
  description: z.string().min(1),

  scaling: z.record(z.string(), ScalingTierSchema).optional(),

  lead: z.object({
    model: z.enum(["opus", "sonnet", "haiku"]).default("opus"),
    strategy: z.string().min(1),
    tools: z.array(z.string()),
  }),

  workers: z.record(z.string(), WorkerSchema),

  artifacts: ArtifactsConfigSchema.optional(),

  evaluation: EvaluationSchema.optional(),

  pattern: z.enum(["parallel", "sequential", "pipeline"]).default("parallel"),
});

export type Mission = z.infer<typeof MissionSchema>;
export type ScalingTier = z.infer<typeof ScalingTierSchema>;
export type Worker = z.infer<typeof WorkerSchema>;
