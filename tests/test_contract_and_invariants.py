from __future__ import annotations

import unittest
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
    enforce_hard_invariants,
)
from formless.ledger import compute_replay_hash


class ContractTests(unittest.TestCase):
    def _decision(self) -> DecisionRecord:
        t0 = datetime.now(timezone.utc)
        provisional = DecisionRecord(
            decision_id=UUID("018f4f8e-7b57-7cc1-bf8e-43f054f4e3d6"),
            created_at=t0,
            context=FinancialContext(
                client_id="T-001",
                product="SME_loan",
                amount=100_000,
                currency="EUR",
                jurisdiction="FR",
                risk_signals={},
            ),
            recommendation=Recommendation.APPROVE,
            confidence=0.8,
            responsibility=ResponsibilityGraph(
                actors=[
                    Actor(
                        actor_id="human:approver",
                        role=ActorRole.HUMAN,
                        display_name="Approver",
                        accountable=True,
                        accountability_role="credit_officer",
                        authority_level=7,
                    )
                ],
                edges=[],
            ),
            legal_basis=[LegalBasisReference(instrument="Code monétaire et financier", section="Article L.511-41-1")],
            temporal=TemporalValidity(valid_from=t0 - timedelta(minutes=1), expires_at=t0 + timedelta(days=1)),
            policy_snapshot_id="POL-FR-2026-01",
            model_provider="openai",
            model_version="gpt-4o-mini",
            replay_hash="0" * 64,
        )
        return provisional.model_copy(update={"replay_hash": compute_replay_hash(provisional)})

    def test_hard_invariants_pass(self) -> None:
        enforce_hard_invariants(self._decision())

    def test_non_fr_scope_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FinancialContext(
                client_id="T-002",
                product="SME_loan",
                amount=100_000,
                currency="EUR",
                jurisdiction="EU",
                risk_signals={},
            )


if __name__ == "__main__":
    unittest.main()
