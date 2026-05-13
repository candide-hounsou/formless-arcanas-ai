from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from formless.core import (
    Actor,
    ActorRole,
    DecisionRecord,
    FinancialContext,
    LegalBasisReference,
    Recommendation,
    ResponsibilityGraph,
    TemporalValidity,
)
from formless.ledger import compute_replay_hash


def build_synthetic_credit_committee_decision() -> DecisionRecord:
    t0 = datetime.now(timezone.utc)
    base = DecisionRecord(
        decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d3"),
        created_at=t0,
        context=FinancialContext(
            client_id="SYN-CC-001",
            product="SME_loan",
            amount=500000,
            currency="EUR",
            jurisdiction="EU",
            risk_signals={"prob_default": 0.07, "sector_stress": "moderate"},
        ),
        recommendation=Recommendation.REVIEW,
        confidence=0.61,
        responsibility=ResponsibilityGraph(
            actors=[
                Actor(
                    actor_id="human:committee_chair",
                    role=ActorRole.HUMAN,
                    display_name="Committee Chair",
                    accountable=True,
                    accountability_role="credit_committee_chair",
                    authority_level=9,
                ),
            ],
            edges=[],
        ),
        legal_basis=[LegalBasisReference(instrument="Code monétaire et financier", section="Article L.511-41-1")],
        temporal=TemporalValidity(valid_from=t0, expires_at=t0 + timedelta(days=14)),
        policy_snapshot_id="POL-EU-2026-01",
        model_provider="openai",
        model_version="gpt-4o-mini",
        replay_hash="0" * 64,
    )
    return base.model_copy(update={"replay_hash": compute_replay_hash(base)})
