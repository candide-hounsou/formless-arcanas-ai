# 🜁 formless‑arcanas‑ai

**A liability-aware financial decision reference implementation built with Pydantic AI**

`formless-arcanas-ai` demonstrates deterministic, auditable, liability-aware AI decisioning for regulated finance.

This project is exploratory, conceptual and designed to start discussions, not end them.

All suggestions, infos or use cases are welcomed !

## Current scope (v0.1.x)

- **Jurisdiction:** FR only
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

## Compliance boundary (important)

This repository is a **reference implementation**, not a production compliance system.
It does **not** guarantee legal sufficiency, model fairness, anti-fraud completeness, or regulatory approval.

## License

MIT
