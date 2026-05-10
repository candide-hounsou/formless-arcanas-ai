from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from ..core.decision import DecisionRecord


class AuditEvaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    evaluated_at: datetime
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool
    missing_fields: list[str] = Field(default_factory=list)


def evaluate_audit_completeness(decision: DecisionRecord) -> AuditEvaluation:
    missing: list[str] = []
    if not decision.legal_basis:
        missing.append("legal_basis")
    if not decision.responsibility.accountable_actors():
        missing.append("accountability")
    if not decision.policy_snapshot_id:
        missing.append("policy_snapshot_id")

    score = max(0.0, 1.0 - (0.34 * len(missing)))
    return AuditEvaluation(
        evaluated_at=datetime.now(timezone.utc),
        score=score,
        passed=score >= 0.99,
        missing_fields=missing,
    )
