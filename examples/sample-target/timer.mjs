export const MIN_DURATION_MS = 1000;
export const MAX_DURATION_MS = 86400000;

export function createTimer(durationMs = 60000) {
  if (!Number.isInteger(durationMs) || durationMs < MIN_DURATION_MS || durationMs > MAX_DURATION_MS) {
    return { error: "invalid_duration" };
  }
  return {
    state: "idle",
    duration_ms: durationMs,
    remaining_ms: durationMs,
    warning_active: false,
  };
}

export function advanceTimer(snapshot, elapsedMs) {
  if (snapshot.state !== "running" || elapsedMs <= 0) {
    return snapshot;
  }
  const nextRemaining = Math.max(0, snapshot.remaining_ms - elapsedMs);
  const nextState = nextRemaining === 0 ? "completed" : "running";
  return {
    ...snapshot,
    state: nextState,
    remaining_ms: nextRemaining,
    warning_active: nextState === "running" && nextRemaining <= 10000,
  };
}
