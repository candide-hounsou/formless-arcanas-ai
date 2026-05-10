from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from ..core.decision import DecisionRecord


class RegulatorView(BaseModel):
    model_config = ConfigDict(frozen=True)

    generated_at: datetime
    regulator_persona: str = "internal_compliance"
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool
    summary: str


def build_internal_compliance_view(decision: DecisionRecord) -> RegulatorView:
    obligations = len(decision.legal_basis)
    score = min(1.0, 0.6 + (0.1 * obligations) + (0.3 if decision.confidence >= 0.55 else 0.0))
    return RegulatorView(
        generated_at=datetime.now(timezone.utc),
        score=score,
        passed=score >= 0.99,
        summary=(
            f"Decision {decision.decision_id} maps to {obligations} legal references, "
            f"policy snapshot {decision.policy_snapshot_id}, "
            f"and model provenance {decision.model_provider}/{decision.model_version}."
        ),
    )
