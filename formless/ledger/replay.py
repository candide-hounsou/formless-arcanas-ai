from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from pydantic import ValidationError

from ..core.decision import DecisionRecord
from ..core.policy import PolicySnapshot
from .event_log import canonical_json, compute_replay_hash, iter_ledger


def replay_and_verify(path: str | Path = "decision_ledger.jsonl") -> List[Tuple[str, bool, str]]:
    """Reconstruct decisions and verify chain + replay hashes."""
    results: List[Tuple[str, bool, str]] = []
    prev_hash = ""

    for item in iter_ledger(path):
        expected_chain_hash = hashlib.sha256(
            canonical_json(
                {
                    "committed_at": item.get("committed_at"),
                    "retention_years": item.get("retention_years"),
                    "deletion_policy": item.get("deletion_policy"),
                    "prev_hash": item.get("prev_hash"),
                    "payload": item.get("payload", item),
                }
            ).encode("utf-8")
        ).hexdigest()

        if item.get("prev_hash", "") != prev_hash:
            results.append((item.get("payload", item).get("decision_id", "<unknown>"), False, "chain broken"))
            prev_hash = item.get("entry_hash", "")
            continue

        if item.get("entry_hash", "") != expected_chain_hash:
            results.append((item.get("payload", item).get("decision_id", "<unknown>"), False, "entry hash mismatch"))
            prev_hash = item.get("entry_hash", "")
            continue

        payload = item.get("payload", item)
        try:
            decision = DecisionRecord.model_validate(payload)
        except ValidationError as e:
            results.append((payload.get("decision_id", "<unknown>"), False, f"schema invalid: {e}"))
            prev_hash = item.get("entry_hash", "")
            continue

        expected = compute_replay_hash(decision)
        if expected != decision.replay_hash:
            results.append((str(decision.decision_id), False, "hash mismatch (tampering or non-determinism)"))
        else:
            results.append((str(decision.decision_id), True, "ok"))

        prev_hash = item.get("entry_hash", "")

    return results


def replay_at_time(
    replay_time: datetime,
    *,
    policy_snapshots: list[PolicySnapshot],
    path: str | Path = "decision_ledger.jsonl",
) -> List[Tuple[str, bool, str]]:
    """Replay decisions with the policy snapshot active at replay_time."""
    active_snapshots = [s for s in policy_snapshots if s.valid_from <= replay_time < s.valid_to]
    if not active_snapshots:
        return [("<none>", False, "no active policy snapshot for replay time")]

    snapshot = active_snapshots[0]
    outcomes: List[Tuple[str, bool, str]] = []

    for item in iter_ledger(path):
        payload = item.get("payload", item)
        decision_id = payload.get("decision_id", "<unknown>")
        decision_policy_snapshot = payload.get("policy_snapshot_id")
        if decision_policy_snapshot != snapshot.snapshot_id:
            outcomes.append((decision_id, False, "policy snapshot mismatch for replay"))
            continue

        provider = payload.get("model_provider")
        model_version = payload.get("model_version")
        if not provider or not model_version:
            outcomes.append((decision_id, False, "missing model provenance"))
            continue

        outcomes.append((decision_id, True, "policy and model provenance matched"))

    return outcomes
