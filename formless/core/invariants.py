from __future__ import annotations

from datetime import datetime, timezone

from .decision import DecisionRecord
from .responsibility import ActorRole


class InvariantViolation(ValueError):
    """Raised when a decision violates non-negotiable invariants."""


def enforce_invariants(decision: DecisionRecord, *, now: datetime | None = None) -> None:
    """Enforce non-negotiable invariants.

    These invariants are intentionally strict and finance-oriented:
    - A decision must have explicit responsibility attribution.
    - At least one HUMAN must be accountable (not just involved).
    - Temporal validity must hold at commit time.
    """

    now = now or datetime.now(timezone.utc)

    # 1) Responsibility must exist and be meaningful
    if not decision.responsibility.actors:
        raise InvariantViolation("Missing responsibility: at least one actor must be recorded")

    if not decision.responsibility.accountable_actors():
        raise InvariantViolation("Missing accountability: at least one actor must be accountable")

    if not decision.responsibility.has_human_accountability():
        raise InvariantViolation("Missing human accountability: at least one HUMAN must be accountable")

    # 2) Temporal validity must hold at commit time
    if not decision.temporal.is_valid(now):
        raise InvariantViolation("Decision is not valid at commit time (outside validity window)")

    # 3) Confidence must be honest about uncertainty (guardrail)
    if decision.recommendation == "approve" and decision.confidence < 0.55:
        raise InvariantViolation("Approval confidence too low: use REVIEW or justify via policy")
