# RC-0002 — EU mortgage underwriting override

## Status

Draft research brief (sources to verify).

## Summary

A mortgage application is initially rejected by a risk model.
A human override is approved after a verified collateral update or income revision.
This use case validates override governance, accountability transfer, and time-bounded validity.

## Jurisdiction

EU

## Decision trigger

- Mortgage application recommendation is **deny**.
- A subsequent override is approved by a senior risk or credit authority.

## Regulatory drivers (candidate)

- EBA Guidelines on loan origination and monitoring (EBA/GL/2020/06).
- Mortgage Credit Directive (2014/17/EU).

> Sources and exact sections must be verified before use.

## DecisionRecord mapping

- `context`: applicant profile, product=mortgage, amount, jurisdiction=EU.
- `recommendation`: APPROVE after override.
- `responsibility`: override transfer from credit officer to senior authority.
- `legal_basis`: EU loan origination guidelines (to confirm).
- `temporal`: override validity window (e.g., 30–90 days).
- `policy_snapshot_id`: EU policy snapshot in force at decision time.

## Responsibility chain

- Primary: credit officer initiating the case.
- Override authority: senior risk director (accountable after override).

## Data & evidence requirements

- Collateral valuation update and provenance.
- Income verification or updated financial statements.
- Override rationale and approval timestamp.

## Replay & traceability

- Replay must demonstrate override transfer and updated evidence.
- Exception policy references must be preserved with the decision.

## Open questions

- What override thresholds require committee review?
- How long should override validity persist before re-review?
- Which collateral valuation standards apply?

## Sources (to verify)

- EBA/GL/2020/06 (loan origination & monitoring)
- Directive 2014/17/EU (mortgage credit)
