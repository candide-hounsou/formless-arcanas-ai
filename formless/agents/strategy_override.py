from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from ..core.decision import DecisionRecord
from ..core.responsibility import OverrideProvenance, ResponsibilityGraph


class StrategyOverrideRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision_id: str
    from_actor_id: str
    to_actor_id: str
    rationale: str = Field(..., min_length=10)


class StrategyOverrideResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision_id: str
    override_id: str
    applied_at: datetime
    liability_transferred: bool


def apply_strategy_override(request: StrategyOverrideRequest, responsibility: ResponsibilityGraph) -> tuple[ResponsibilityGraph, StrategyOverrideResult]:
    override = OverrideProvenance(
        override_id=f"OVR-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        from_actor_id=request.from_actor_id,
        to_actor_id=request.to_actor_id,
        reason=request.rationale,
        liability_transfer=True,
    )

    updated = responsibility.model_copy(update={"overrides": [*responsibility.overrides, override]})
    result = StrategyOverrideResult(
        decision_id=request.decision_id,
        override_id=override.override_id,
        applied_at=datetime.now(timezone.utc),
        liability_transferred=True,
    )
    return updated, result
