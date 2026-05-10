from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from pydantic import ValidationError

from ..core.decision import DecisionRecord
from .event_log import iter_ledger, compute_replay_hash


def replay_and_verify(path: str | Path = "decision_ledger.jsonl") -> List[Tuple[str, bool, str]]:
    """Reconstruct decisions and verify replay hashes.

    Returns list of (decision_id, ok, reason).
    """
    results: List[Tuple[str, bool, str]] = []
    for item in iter_ledger(path):
        try:
            decision = DecisionRecord.model_validate(item)
        except ValidationError as e:
            results.append((item.get("decision_id", "<unknown>"), False, f"schema invalid: {e}"))
            continue
        expected = compute_replay_hash(decision)
        if expected != decision.replay_hash:
            results.append((decision.decision_id, False, "hash mismatch (tampering or non-determinism)"))
        else:
            results.append((decision.decision_id, True, "ok"))
    return results
