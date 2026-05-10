from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..core.decision import DecisionRecord
from ..core.policy import ExceptionAuthority


class RiskExceptionRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision_id: str
    reason: str = Field(..., min_length=10)
    requested_by: str = Field(..., min_length=3)


class RiskExceptionDecision(BaseModel):
    model_config = ConfigDict(frozen=True)

    approved: bool
    authority: ExceptionAuthority
    rationale: str = Field(..., min_length=10)


def evaluate_risk_exception(request: RiskExceptionRequest, decision: DecisionRecord) -> RiskExceptionDecision:
    if decision.confidence >= 0.50:
        return RiskExceptionDecision(
            approved=True,
            authority=ExceptionAuthority.RISK_COMMITTEE,
            rationale="Risk committee may authorize exception when confidence remains above safeguard threshold.",
        )
    return RiskExceptionDecision(
        approved=False,
        authority=ExceptionAuthority.CHIEF_RISK_OFFICER,
        rationale="Exception rejected due to confidence below safeguard threshold.",
    )
