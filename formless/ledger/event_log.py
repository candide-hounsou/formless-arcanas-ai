from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel

from ..core.decision import DecisionRecord


def canonical_json(obj) -> str:
    """Stable JSON encoding for hashing/replay."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_replay_hash(decision: DecisionRecord) -> str:
    payload = decision.model_dump(mode="json")
    # Do not include replay_hash in its own hash
    payload.pop("replay_hash", None)
    data = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def commit_decision(decision: DecisionRecord, *, path: str | Path = "decision_ledger.jsonl") -> None:
    """Append-only commit to a JSONL ledger."""
    path = Path(path)
    payload = decision.model_dump(mode="json")
    payload["schema_version"] = "0.1"
    with path.open("a", encoding="utf-8") as f:
        f.write(canonical_json(payload) + "\n")


def iter_ledger(path: str | Path = "decision_ledger.jsonl") -> Iterable[dict]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)
