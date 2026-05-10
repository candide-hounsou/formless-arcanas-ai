from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator

from .responsibility import ResponsibilityGraph
from .temporal import TemporalValidity


class Recommendation(str, Enum):
    APPROVE = "approve"
    DECLINE = "decline"
    REVIEW = "review"


class LegalBasisReference(BaseModel):
    """A minimal pointer to the basis under which the decision is made."""

    instrument: str = Field(..., min_length=3, description="e.g., Basel III, internal policy X")
    section: str = Field(..., min_length=1, description="e.g., Article 12, §3.2")
    url: Optional[str] = None


class FinancialContext(BaseModel):
    """Input context for a decision. Keep it compact and composable."""

    client_id: str = Field(..., min_length=2)
    product: str = Field(..., min_length=2, description="e.g., SME_loan, mortgage")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    jurisdiction: str = Field(..., min_length=2, description="e.g., FR, EU")
    risk_signals: Dict[str, Any] = Field(default_factory=dict)


class DecisionRecord(BaseModel):
    """Audit-grade decision record."""

    model_config = ConfigDict(frozen=True)

    decision_id: str = Field(..., min_length=8)
    created_at: datetime

    context: FinancialContext
    recommendation: Recommendation
    confidence: float = Field(..., ge=0.0, le=1.0)

    responsibility: ResponsibilityGraph
    legal_basis: List[LegalBasisReference] = Field(default_factory=list)
    temporal: TemporalValidity

    # Hash that makes replay tampering evident
    replay_hash: str = Field(..., min_length=16)

    @model_validator(mode="after")
    def _basic_checks(self) -> "DecisionRecord":
        # Keep 'basic' here: avoid business policy entanglement.
        if not self.legal_basis:
            # allow empty at model level? No: legal basis is mandatory for finance-grade decisions.
            raise ValueError("legal_basis must not be empty")
        return self
