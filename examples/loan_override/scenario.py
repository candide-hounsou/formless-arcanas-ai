from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from formless.agents.strategy_override import StrategyOverrideRequest, apply_strategy_override
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


def build_synthetic_loan_override_decision() -> tuple[DecisionRecord, str]:
    t0 = datetime.now(timezone.utc)
    responsibility = ResponsibilityGraph(
        actors=[
            Actor(
                actor_id="human:credit_officer",
                role=ActorRole.HUMAN,
                display_name="Credit Officer",
                accountable=True,
                accountability_role="credit_officer",
                authority_level=7,
            ),
            Actor(
                actor_id="human:risk_director",
                role=ActorRole.HUMAN,
                display_name="Risk Director",
                accountable=False,
                accountability_role="risk_director",
                authority_level=10,
            ),
        ],
        edges=[],
    )

    overridden_graph, override_result = apply_strategy_override(
        StrategyOverrideRequest(
            decision_id="018f4f8e-7b57-7cc1-bf8e-43f054f4e3d4",
            from_actor_id="human:credit_officer",
            to_actor_id="human:risk_director",
            rationale="Exceptional collateral update after committee review.",
        ),
        responsibility,
    )

    decision = DecisionRecord(
        decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d4"),
        created_at=t0,
        context=FinancialContext(
            client_id="SYN-LO-001",
            product="mortgage",
            amount=320000,
            currency="USD",
            jurisdiction="US",
            risk_signals={"loan_to_value": 0.71},
        ),
        recommendation=Recommendation.APPROVE,
        confidence=0.72,
        responsibility=overridden_graph,
        legal_basis=[LegalBasisReference(instrument="12 CFR Part 30", section="Section 30.3")],
        temporal=TemporalValidity(valid_from=t0, expires_at=t0 + timedelta(days=30)),
        policy_snapshot_id="POL-US-2026-01",
        model_provider="openai",
        model_version="gpt-4o-mini",
        replay_hash="0" * 64,
    )
    decision = decision.model_copy(update={"replay_hash": compute_replay_hash(decision)})
    return decision, override_result.override_id
