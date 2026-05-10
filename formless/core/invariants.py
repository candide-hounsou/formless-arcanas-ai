from __future__ import annotations

from datetime import datetime, timezone

from .decision import DecisionRecord
from .policy import PolicySnapshot, evaluate_policy, PolicyDecision


class InvariantViolation(ValueError):
    """Raised when a decision violates non-negotiable invariants."""


class PolicyViolation(ValueError):
    """Raised when policy checks fail and no exception flow is accepted."""


def enforce_hard_invariants(decision: DecisionRecord, *, now: datetime | None = None) -> None:
    """Enforce non-negotiable invariants."""

    now = now or datetime.now(timezone.utc)

    if not decision.responsibility.actors:
        raise InvariantViolation("Missing responsibility: at least one actor must be recorded")

    if not decision.responsibility.accountable_actors():
        raise InvariantViolation("Missing accountability: at least one actor must be accountable")

    if not decision.responsibility.has_human_accountability():
        raise InvariantViolation("Missing role-specific human accountability")

    if not decision.temporal.is_valid(now):
        raise InvariantViolation("Decision is not valid at commit time (outside validity window)")

    if decision.recommendation.value == "approve" and decision.confidence < 0.55:
        raise InvariantViolation("Approval confidence too low: use REVIEW or policy exception")


def enforce_with_policy(
    decision: DecisionRecord,
    *,
    policy_snapshot: PolicySnapshot,
    now: datetime | None = None,
    allow_exception: bool = False,
) -> None:
    enforce_hard_invariants(decision, now=now)
    evaluation = evaluate_policy(decision, policy_snapshot, now=now)
    if evaluation.decision == PolicyDecision.FAIL:
        raise PolicyViolation(f"Policy snapshot invalid or inactive: {evaluation.failed_rules}")
    if evaluation.decision == PolicyDecision.EXCEPTION_REQUIRED and not allow_exception:
        raise PolicyViolation(
            f"Policy exception required: {evaluation.failed_rules}; "
            f"suggested authorities={','.join(a.value for a in evaluation.suggested_exception_authorities)}"
        )


def enforce_invariants(decision: DecisionRecord, *, now: datetime | None = None) -> None:
    """Backward-compatible alias for hard invariant checks only."""

    enforce_hard_invariants(decision, now=now)
