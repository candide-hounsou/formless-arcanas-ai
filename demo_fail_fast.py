"""One-file runnable demo.

Demonstrates: a decision failing fast due to missing responsibility,
then a corrected decision being committed and replay-verified.

Run:
  python demo_fail_fast.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
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
    enforce_hard_invariants,
)
from formless.ledger import commit_decision, compute_replay_hash, replay_and_verify


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def make_context() -> FinancialContext:
    return FinancialContext(
        client_id="C-001",
        product="SME_loan",
        amount=250_000,
        currency="EUR",
        jurisdiction="EU",
        risk_signals={"dscr": 1.1, "late_payments_12m": 2},
    )


def bad_decision_missing_responsibility() -> DecisionRecord:
    t0 = now_utc()
    temporal = TemporalValidity(valid_from=t0 - timedelta(minutes=1), expires_at=t0 + timedelta(days=30))

    responsibility = ResponsibilityGraph(actors=[], edges=[])

    provisional = DecisionRecord(
        decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d1"),
        created_at=t0,
        context=make_context(),
        recommendation=Recommendation.APPROVE,
        confidence=0.82,
        responsibility=responsibility,
        legal_basis=[LegalBasisReference(instrument="Code monétaire et financier", section="Article L.511-41-1")],
        temporal=temporal,
        policy_snapshot_id="POL-EU-2026-01",
        model_provider="openai",
        model_version="gpt-4o-mini",
        replay_hash="0" * 64,
    )
    return provisional


def good_decision_with_responsibility() -> DecisionRecord:
    t0 = now_utc()
    temporal = TemporalValidity(valid_from=t0 - timedelta(minutes=1), expires_at=t0 + timedelta(days=30))

    responsibility = ResponsibilityGraph(
        actors=[
            Actor(
                actor_id="human:credit_officer",
                role=ActorRole.HUMAN,
                display_name="Credit Officer",
                accountable=True,
                accountability_role="credit_officer",
                authority_level=8,
            ),
            Actor(actor_id="ai:triage", role=ActorRole.AI_SYSTEM, display_name="Triage Agent", accountable=False),
            Actor(actor_id="org:bank", role=ActorRole.ORG, display_name="Bank Entity", accountable=False),
        ],
        edges=[
            {"src": "ai:triage", "dst": "human:credit_officer", "relation": "recommended"},
            {"src": "human:credit_officer", "dst": "org:bank", "relation": "approved_for"},
        ],
    )

    provisional = DecisionRecord(
        decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d2"),
        created_at=t0,
        context=make_context(),
        recommendation=Recommendation.APPROVE,
        confidence=0.82,
        responsibility=responsibility,
        legal_basis=[LegalBasisReference(instrument="Code monétaire et financier", section="Article L.511-41-1")],
        temporal=temporal,
        policy_snapshot_id="POL-EU-2026-01",
        model_provider="openai",
        model_version="gpt-4o-mini",
        replay_hash="0" * 64,
    )

    rh = compute_replay_hash(provisional)
    return provisional.model_copy(update={"replay_hash": rh})


def main() -> None:
    print("\n=== DEMO: fail fast on missing responsibility ===")

    try:
        d1 = bad_decision_missing_responsibility()
        enforce_hard_invariants(d1)
        print("UNEXPECTED: bad decision passed invariants")
    except Exception as e:
        print("OK: decision rejected immediately")
        print(f"  -> {type(e).__name__}: {e}")

    print("\n=== DEMO: corrected decision commits + replays ===")
    d2 = good_decision_with_responsibility()
    with tempfile.TemporaryDirectory() as td:
        demo_ledger = Path(td) / "demo_ledger.jsonl"

        enforce_hard_invariants(d2)
        committed = commit_decision(d2, path=demo_ledger)
        if committed:
            print(f"Committed decision to {demo_ledger}")
        else:
            print("Skipped commit (idempotent duplicate)")

        results = replay_and_verify(demo_ledger)
        for decision_id, ok, reason in results:
            status = "OK" if ok else "FAIL"
            print(f"Replay {status}: {decision_id} ({reason})")


if __name__ == "__main__":
    main()
