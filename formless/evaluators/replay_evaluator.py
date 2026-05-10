from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ..ledger.replay import replay_and_verify


class ReplayEvaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    evaluated_at: datetime
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool
    drift_flags: list[str]


def evaluate_replay_determinism(path: str | Path = "decision_ledger.jsonl") -> ReplayEvaluation:
    results = replay_and_verify(path)
    total = len(results)
    if total == 0:
        return ReplayEvaluation(
            evaluated_at=datetime.now(timezone.utc),
            score=0.0,
            passed=False,
            drift_flags=["no_records"],
        )

    failures = [f"{decision_id}:{reason}" for decision_id, ok, reason in results if not ok]
    score = (total - len(failures)) / total
    return ReplayEvaluation(
        evaluated_at=datetime.now(timezone.utc),
        score=score,
        passed=score >= 0.99,
        drift_flags=failures,
    )
