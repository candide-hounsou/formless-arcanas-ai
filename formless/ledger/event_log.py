from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from ..core.decision import DecisionRecord


def canonical_json(obj) -> str:
    """Stable JSON encoding for hashing/replay."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_replay_hash(decision: DecisionRecord) -> str:
    payload = decision.model_dump(mode="json")
    payload.pop("replay_hash", None)
    data = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _iter_lines(path: Path) -> Iterable[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _last_entry_hash(path: Path) -> str:
    prev = ""
    for item in _iter_lines(path):
        prev = item.get("entry_hash", "")
    return prev


def _contains_decision_id(path: Path, decision_id: str) -> bool:
    for item in _iter_lines(path):
        payload = item.get("payload", item)
        if payload.get("decision_id") == decision_id:
            return True
    return False


def commit_decision(
    decision: DecisionRecord,
    *,
    path: str | Path = "decision_ledger.jsonl",
    retention_years: int = 10,
    deletion_policy: str = "review_required",
) -> bool:
    """Append-only idempotent commit to a tamper-evident JSONL ledger."""
    path = Path(path)
    payload = decision.model_dump(mode="json")
    payload["schema_version"] = decision.schema_version

    if _contains_decision_id(path, payload["decision_id"]):
        return False

    prev_hash = _last_entry_hash(path)
    envelope = {
        "committed_at": datetime.now(timezone.utc).isoformat(),
        "retention_years": retention_years,
        "deletion_policy": deletion_policy,
        "prev_hash": prev_hash,
        "payload": payload,
    }
    envelope["entry_hash"] = hashlib.sha256(canonical_json(envelope).encode("utf-8")).hexdigest()

    with path.open("a", encoding="utf-8") as f:
        f.write(canonical_json(envelope) + "\n")
    return True


def iter_ledger(path: str | Path = "decision_ledger.jsonl") -> Iterable[dict]:
    path = Path(path)
    yield from _iter_lines(path)
