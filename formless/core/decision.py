from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .responsibility import ResponsibilityGraph
from .temporal import TemporalValidity


class Recommendation(str, Enum):
    APPROVE = "approve"
    DECLINE = "decline"
    REVIEW = "review"


class LegalBasisReference(BaseModel):
    """A pointer to the legal basis under which the decision is made (FR scope v1)."""

    instrument: str = Field(..., min_length=3, description="e.g., Code monétaire et financier")
    section: str = Field(..., min_length=1, description="e.g., Article L.511-41-1")
    url: str | None = None


class FinancialContext(BaseModel):
    """Input context for a decision. v1 is scoped to France only."""

    client_id: str = Field(..., min_length=2)
    product: str = Field(..., min_length=2, description="e.g., SME_loan, mortgage")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    jurisdiction: str = Field(..., description="Must be FR for v1")
    risk_signals: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_scope(self) -> "FinancialContext":
        if self.jurisdiction.upper() != "FR":
            raise ValueError("v1 scope is FR only")
        return self


class DecisionRecord(BaseModel):
    """Audit-grade decision record (canonical contract v1)."""

    model_config = ConfigDict(frozen=True)

    schema_version: str = Field(default="1.0")
    decision_id: UUID
    created_at: datetime

    context: FinancialContext
    recommendation: Recommendation
    confidence: float = Field(..., ge=0.0, le=1.0)

    responsibility: ResponsibilityGraph
    legal_basis: List[LegalBasisReference] = Field(default_factory=list)

    temporal: TemporalValidity
    policy_snapshot_id: str = Field(..., min_length=3)

    # exact replay requirement for model provenance
    model_provider: str = Field(..., min_length=2)
    model_version: str = Field(..., min_length=1)

    # Hash that makes replay tampering evident
    replay_hash: str = Field(..., min_length=16)

    @model_validator(mode="after")
    def _basic_checks(self) -> "DecisionRecord":
        if self.decision_id.version != 7:
            raise ValueError("decision_id must be UUIDv7")
        if not self.legal_basis:
            raise ValueError("legal_basis must not be empty")
        return self
