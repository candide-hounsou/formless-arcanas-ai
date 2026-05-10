"""Optional Pydantic AI agent skeleton.

This file is intentionally not required for the demo to run.
If you wire a model provider + API key, the agent can produce a DecisionRecord.

The repo's thesis is not 'LLM calls', but 'audit-grade invariants'.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic_ai import Agent  # type: ignore

from ..core.decision import DecisionRecord, FinancialContext, LegalBasisReference, Recommendation
from ..core.responsibility import Actor, ActorRole, ResponsibilityGraph
from ..core.temporal import TemporalValidity
from ..ledger.event_log import compute_replay_hash


SYSTEM_PROMPT = (
    "You are a finance-grade decision system. "
    "Return ONLY a DecisionRecord-compatible structure. "
    "Never omit responsibility, legal basis, or temporal validity."
)

agent = Agent(
    model="openai:gpt-4o-mini",  # example; replace with your provider
    system_prompt=SYSTEM_PROMPT,
    result_type=DecisionRecord,
)

# NOTE: This is a placeholder example; do not run without configuring credentials.
