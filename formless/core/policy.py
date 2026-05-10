from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .decision import DecisionRecord


class PolicyDecision(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    EXCEPTION_REQUIRED = "exception_required"


class ExceptionAuthority(str, Enum):
    RISK_COMMITTEE = "risk_committee"
    CHIEF_RISK_OFFICER = "chief_risk_officer"
    COMPLIANCE_OFFICER = "compliance_officer"


class PolicyRule(BaseModel):
    rule_id: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    min_confidence_for_approval: float = Field(default=0.55, ge=0.0, le=1.0)
    mandatory_legal_basis_prefix: str = Field(default="Article")


class PolicySnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    snapshot_id: str = Field(..., min_length=3)
    jurisdiction: str = Field(default="FR")
    valid_from: datetime
    valid_to: datetime
    rules: list[PolicyRule]


class PolicyEvaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    decision: PolicyDecision
    score: float = Field(..., ge=0.0, le=1.0)
    passed: bool
    failed_rules: list[str] = Field(default_factory=list)
    suggested_exception_authorities: list[ExceptionAuthority] = Field(default_factory=list)


def evaluate_policy(decision: DecisionRecord, snapshot: PolicySnapshot, *, now: datetime | None = None) -> PolicyEvaluation:
    now = now or datetime.now(timezone.utc)

    if snapshot.jurisdiction.upper() != "FR":
        raise ValueError("Only FR policy snapshots are supported in v1")
    if not (snapshot.valid_from <= now < snapshot.valid_to):
        return PolicyEvaluation(
            snapshot_id=snapshot.snapshot_id,
            decision=PolicyDecision.FAIL,
            score=0.0,
            passed=False,
            failed_rules=["snapshot_not_active"],
        )

    failed_rules: list[str] = []
    score = 1.0

    for rule in snapshot.rules:
        if decision.recommendation.value == "approve" and decision.confidence < rule.min_confidence_for_approval:
            failed_rules.append(f"{rule.rule_id}:confidence")
            score -= 0.5
        if not any(lb.section.startswith(rule.mandatory_legal_basis_prefix) for lb in decision.legal_basis):
            failed_rules.append(f"{rule.rule_id}:legal_basis")
            score -= 0.5

    if failed_rules:
        return PolicyEvaluation(
            snapshot_id=snapshot.snapshot_id,
            decision=PolicyDecision.EXCEPTION_REQUIRED,
            score=max(score, 0.0),
            passed=False,
            failed_rules=failed_rules,
            suggested_exception_authorities=[
                ExceptionAuthority.RISK_COMMITTEE,
                ExceptionAuthority.CHIEF_RISK_OFFICER,
                ExceptionAuthority.COMPLIANCE_OFFICER,
            ],
        )

    return PolicyEvaluation(
        snapshot_id=snapshot.snapshot_id,
        decision=PolicyDecision.PASS,
        score=1.0,
        passed=True,
    )
