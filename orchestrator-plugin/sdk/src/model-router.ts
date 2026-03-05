export type ModelTier = "opus" | "sonnet" | "haiku";

interface ModelConfig {
  id: string;
  inputPer1M: number;
  outputPer1M: number;
}

const MODEL_MAP: Record<ModelTier, ModelConfig> = {
  opus: { id: "claude-opus-4-6", inputPer1M: 5.0, outputPer1M: 25.0 },
  sonnet: { id: "claude-sonnet-4-6", inputPer1M: 3.0, outputPer1M: 15.0 },
  haiku: { id: "claude-haiku-4-5", inputPer1M: 1.0, outputPer1M: 5.0 },
};

export function resolveModel(tier: ModelTier): string {
  return MODEL_MAP[tier].id;
}

export function estimateCost(
  tier: ModelTier,
  inputTokens: number,
  outputTokens: number,
): number {
  const config = MODEL_MAP[tier];
  return (
    (inputTokens / 1_000_000) * config.inputPer1M +
    (outputTokens / 1_000_000) * config.outputPer1M
  );
}

export function estimateMissionCost(
  leadTier: ModelTier,
  workerTier: ModelTier,
  workerCount: number,
): { low: number; high: number; breakdown: string } {
  const leadCost = estimateCost(leadTier, 10_000, 4_000);
  const workerCostEach = estimateCost(workerTier, 8_000, 3_000);
  const totalWorkerCost = workerCostEach * workerCount;

  const low = leadCost + totalWorkerCost * 0.5;
  const high = (leadCost + totalWorkerCost) * 2.0;

  const breakdown = [
    `Lead (${leadTier}): ~$${leadCost.toFixed(3)}`,
    `Workers (${workerCount}x ${workerTier}): ~$${totalWorkerCost.toFixed(3)}`,
    `Estimated range: $${low.toFixed(3)} - $${high.toFixed(3)}`,
  ].join("\n");

  return { low, high, breakdown };
}

export function checkBudget(
  budget: number,
  estimated: { low: number; high: number },
): { ok: boolean; message: string } {
  if (estimated.high <= budget) {
    return { ok: true, message: `Budget $${budget.toFixed(2)} is sufficient (estimated max: $${estimated.high.toFixed(3)})` };
  }
  if (estimated.low <= budget) {
    return { ok: true, message: `Budget $${budget.toFixed(2)} may be tight (estimated: $${estimated.low.toFixed(3)} - $${estimated.high.toFixed(3)})` };
  }
  return { ok: false, message: `Budget $${budget.toFixed(2)} is likely insufficient (estimated min: $${estimated.low.toFixed(3)})` };
}
