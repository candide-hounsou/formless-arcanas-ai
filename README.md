# 🜁 formless‑arcanas‑ai

**A liability-aware financial decision reference implementation built with Pydantic AI**

_"If your agent cannot explain who is responsible for a decision, it should not make one !"_
--------------------------------------------------------------------------------------------------------------------------------------------
formless‑arcanas‑ai is an open‑source reference project that demonstrates a class of agentic systems that most AI frameworks cannot express:

Deterministic, auditable, liability-aware AI decisioning for regulated finance

This project is exploratory, conceptual and designed to start discussions, not end them.

All ideas, suggestions, infos or use cases are welcomed !

Instead of optimizing for “best answer”, formless‑arcanas‑ai optimizes for:

Defensibility
Replayability
Responsibility attribution
Temporal validity

This project exists to show what becomes possible when strong typing, schema validation, and agentic reasoning are treated as first‑class invariants, not optional safeguards.
--------------------------------------------------------------------------------------------------------------------
## Why this project exists
Modern agent frameworks are excellent at:

invoking tools,
reasoning step‑by‑step,
generating text.

They are not designed to answer the questions that matter in regulated finance:

Who is responsible for this decision?
Under which regulation was it made?
For how long is this decision valid?
Can this decision be replayed exactly as it was made?
What happens when its assumptions expire?

formless‑arcanas‑ai answers those questions by construction.
-------------------------------------------------------------------------------------------------------------------
## What formless‑arcanas‑ai is not

❌ a chatbot
❌ a RAG system
❌ a scoring model
❌ a workflow engine
❌ a replacement for quantitative models

This project does not try to outperform financial models.
It exists around them — where governance, auditability, and responsibility live.

--------------------------------------------------------------------------------------------------------------------
## Core idea
Every AI‑assisted financial decision is treated as a Decision Record that must satisfy non‑negotiable invariants.
A decision that is:

not attributable,
not replayable,
not time‑bounded,

is considered invalid, regardless of how “reasonable” it sounds.

#" What makes this project different
1. Decisions are structured, not textual
Every decision is a validated object, not free‑form text.
Decision = Data + Responsibility + Time + Legal Basis

2. Responsibility is explicit
Each decision carries a Responsibility Graph:

AI components involved
Human overrides
Organizational roles
Escalation paths

3. Time is a first‑class constraint
Every decision:

has a valid_from timestamp
has an expires_at boundary
can become invalid without being wrong

4. Replayability is mandatory
If a decision cannot be replayed deterministically, it is treated as non‑auditable.

-----------------------------------------------------------------------------------------------------------------------------------------------
## Why Pydantic AI
This project is intentionally built on Pydantic AI, because the design goals cannot be achieved with prompt‑centric or untyped agent frameworks.
Pydantic AI enables:

Strict schema enforcement on agent outputs
Retry‑on‑validation failure, not just retry‑on‑error
Typed dependency injection into agent reasoning
Deterministic evaluation & replay
Audit‑friendly observability

formless‑arcanas‑ai is meant to demonstrate why these properties matter, not just that they exist.

------------------------------------------------------------------------------------------------------------------------------------------------

## Conceptual core: DecisionRecord
Every agent in formless‑arcanas‑ai produces a DecisionRecord.
Conceptually:

DecisionRecord(
    decision_id,
    financial_context,
    recommendation,
    confidence,

    responsibility_chain,
    legal_basis,

    valid_from,
    expires_at,

    replay_hash
)

A DecisionRecord is immutable once committed.

--------------------------------------------------------------------------------------------

## Current scope (v0.1.x)

- **Jurisdiction:** EU/US
- **Decision ID:** UUIDv7 required
- **Liability model:** explicit responsibility graph with transfer-aware overrides
- **Replay model:** tamper-evident hash chain + deterministic replay hash verification
- **Governance model:** ADR/Decision Records under `decision_records/`

## Architecture

```text
formless/
├─ core/
│  ├─ decision.py        # Canonical DecisionRecord v1 contract
│  ├─ responsibility.py  # Authority, delegation, override transfer
│  ├─ temporal.py        # Time-bounded validity
│  ├─ invariants.py      # Hard invariants + policy-enforced checks
│  └─ policy.py          # Effective-dated FR policy snapshots and exceptions
│
├─ agents/
│  ├─ credit_decision.py
│  ├─ risk_exception.py
│  └─ strategy_override.py
│
├─ evaluators/
│  ├─ audit_evaluator.py
│  ├─ regulator_view.py
│  └─ replay_evaluator.py
│
├─ ledger/
│  ├─ event_log.py       # Idempotent append, hash chain, retention metadata
│  └─ replay.py          # Replay verify + replay at time T
│
└─ demo_fail_fast.py
```

## Decision records

Project governance is tracked in:

```text
decision_records/
├─ README.md
├─ events.jsonl
└─ records/
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo_fail_fast.py
python -m unittest discover -s tests -p "test_*.py"
```

## Example scenarios

Synthetic scenario starters:

- `examples/credit_committee/scenario.py`
- `examples/loan_override/scenario.py`
- `examples/portfolio_risk_shift/scenario.py` (flagship)

* Credit decision override *

An agent recommends rejecting a loan.
A human overrides the recommendation.
The system records:

who approved the override,
under which authority,
until when the decision is valid,
who now bears the risk.

* Decision invalidation over time *

A portfolio allocation is approved.
Macro conditions shift.
The system flags the decision as expired, not “wrong”.

This distinction matters in real audits.

## Real cases (research)

Research briefs for EU/US real-world use cases live in `real_cases/`.
These drafts map regulatory drivers to DecisionRecord requirements and must be source-verified before use.

## What this project demonstrates

That agentic AI can be audit‑grade
That responsibility can be modeled, not implied
That time can invalidate correctness
That Pydantic AI enables invariants other frameworks cannot enforce

## Intended audience
This project is for:

engineers building regulated AI systems
teams exploring AI governance
architects designing long‑lived agent systems
anyone skeptical of “just prompt it” approaches in finance

## Compliance boundary (important)

This repository is a **reference implementation**, not a production compliance system.
It does **not** guarantee legal sufficiency, model fairness, anti-fraud completeness, or regulatory approval.

## License

MIT
