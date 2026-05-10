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


def build_synthetic_portfolio_risk_shift_decision() -> DecisionRecord:
    t0 = datetime.now(timezone.utc)
    decision = DecisionRecord(
        decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d5"),
        created_at=t0,
        context=FinancialContext(
            client_id="SYN-PRS-001",
            product="portfolio_rebalance",
            amount=2_500_000,
            currency="EUR",
            jurisdiction="FR",
            risk_signals={"var_shift": 0.18, "credit_spread_delta": 0.05},
        ),
        recommendation=Recommendation.REVIEW,
        confidence=0.68,
        responsibility=ResponsibilityGraph(
            actors=[
                Actor(
                    actor_id="human:portfolio_risk_head",
                    role=ActorRole.HUMAN,
                    display_name="Portfolio Risk Head",
                    accountable=True,
                    accountability_role="portfolio_risk_head",
                    authority_level=9,
                )
            ],
            edges=[],
        ),
        legal_basis=[LegalBasisReference(instrument="Code monétaire et financier", section="Article L.533-10")],
        temporal=TemporalValidity(valid_from=t0, expires_at=t0 + timedelta(days=7)),
        policy_snapshot_id="POL-FR-2026-01",
        model_provider="openai",
        model_version="gpt-4o-mini",
        replay_hash="0" * 64,
    )
    return decision.model_copy(update={"replay_hash": compute_replay_hash(decision)})
