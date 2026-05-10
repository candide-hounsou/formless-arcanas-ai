"""One-file runnable demo.

Demonstrates: a decision failing fast due to missing responsibility,
then a corrected decision being committed and replay-verified.

Run:
  python demo_fail_fast.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic import ValidationError

from formless_arcanas_ai.core import (
    Actor,
    ActorRole,
    DecisionRecord,
    FinancialContext,
    LegalBasisReference,
    Recommendation,
    ResponsibilityGraph,
    TemporalValidity,
    enforce_invariants,
)
from formless_arcanas_ai.ledger import commit_decision, compute_replay_hash, replay_and_verify


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def make_context() -> FinancialContext:
    return FinancialContext(
        client_id="C-001",
        product="SME_loan",
        amount=250_000,
        currency="EUR",
        jurisdiction="FR",
        risk_signals={"dscr": 1.1, "late_payments_12m": 2},
    )


def bad_decision_missing_responsibility() -> DecisionRecord:
    t0 = now_utc()
    temporal = TemporalValidity(valid_from=t0 - timedelta(minutes=1), expires_at=t0 + timedelta(days=30))

    # Intentionally empty responsibility graph -> should fail invariants immediately.
    responsibility = ResponsibilityGraph(actors=[], edges=[])

    provisional = DecisionRecord(
        decision_id="DEC-0001",
        created_at=t0,
        context=make_context(),
        recommendation=Recommendation.APPROVE,
        confidence=0.82,
        responsibility=responsibility,
        legal_basis=[LegalBasisReference(instrument="Internal Credit Policy", section="§2.1")],
        temporal=temporal,
        replay_hash="0" * 64,  # will be replaced in corrected version
    )
    return provisional


def good_decision_with_responsibility() -> DecisionRecord:
    t0 = now_utc()
    temporal = TemporalValidity(valid_from=t0 - timedelta(minutes=1), expires_at=t0 + timedelta(days=30))

    responsibility = ResponsibilityGraph(
        actors=[
            Actor(actor_id="human:credit_officer", role=ActorRole.HUMAN, display_name="Credit Officer", accountable=True),
            Actor(actor_id="ai:triage", role=ActorRole.AI_SYSTEM, display_name="Triage Agent", accountable=False),
            Actor(actor_id="org:bank", role=ActorRole.ORG, display_name="Bank Entity", accountable=False),
        ],
        edges=[
            # AI informs, human approves
            {"src": "ai:triage", "dst": "human:credit_officer", "relation": "recommended"},
            {"src": "human:credit_officer", "dst": "org:bank", "relation": "approved_for"},
        ],
    )

    provisional = DecisionRecord(
        decision_id="DEC-0002",
        created_at=t0,
        context=make_context(),
        recommendation=Recommendation.APPROVE,
        confidence=0.82,
        responsibility=responsibility,
        legal_basis=[LegalBasisReference(instrument="Internal Credit Policy", section="§2.1")],
        temporal=temporal,
        replay_hash="0" * 64,
    )

    # Compute replay hash from canonical content
    rh = compute_replay_hash(provisional)
    return provisional.model_copy(update={"replay_hash": rh})


def main() -> None:
    print("\n=== DEMO: fail fast on missing responsibility ===")

    try:
        d1 = bad_decision_missing_responsibility()
        enforce_invariants(d1)
        print("UNEXPECTED: bad decision passed invariants")
    except Exception as e:
        print("OK: decision rejected immediately")
        print(f"  -> {type(e).__name__}: {e}")

    print("\n=== DEMO: corrected decision commits + replays ===")
    d2 = good_decision_with_responsibility()

    # Enforce invariants before committing
    enforce_invariants(d2)
    commit_decision(d2, path="decision_ledger.jsonl")
    print("Committed DEC-0002 to decision_ledger.jsonl")

    results = replay_and_verify("decision_ledger.jsonl")
    for decision_id, ok, reason in results[-3:]:
        status = "OK" if ok else "FAIL"
        print(f"Replay {status}: {decision_id} ({reason})")


if __name__ == "__main__":
    main()
