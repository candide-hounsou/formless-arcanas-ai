# RC-0003 — EU portfolio suitability-driven rebalance

## Status

Draft research brief (sources to verify).

## Summary

Market conditions shift and a portfolio is recommended for rebalancing.
For retail clients, the decision must document suitability, responsibility, and a clear validity horizon.
This use case validates time-bounded decisions and audit-grade replay of suitability rationale.

## Jurisdiction

EU

## Decision trigger

- Portfolio risk metrics breach threshold (e.g., volatility or VaR shift).
- Recommendation to rebalance client portfolio holdings.

## Regulatory drivers (candidate)

- MiFID II suitability requirements (Directive 2014/65/EU).
- ESMA guidelines on suitability (to confirm).

> Sources and exact sections must be verified before use.

## DecisionRecord mapping

- `context`: client profile, portfolio characteristics, jurisdiction=EU.
- `recommendation`: REVIEW or APPROVE rebalance.
- `responsibility`: portfolio manager accountable for suitability.
- `legal_basis`: MiFID II references (to confirm).
- `temporal`: validity window before re-review (e.g., 7–14 days).
- `policy_snapshot_id`: EU policy snapshot in force at decision time.

## Responsibility chain

- Primary: portfolio manager (accountable).
- Oversight: risk governance reviewer (non-accountable but recorded).

## Data & evidence requirements

- Client risk profile and suitability assessment.
- Portfolio allocation snapshot at decision time.
- Market data inputs used for recommendation.

## Replay & traceability

- Replay must reproduce suitability rationale and allocation deltas.
- Market data snapshots should be captured or referenced.

## Open questions

- What triggers mandatory client communication?
- Which market data fields must be archived for replay?
- How to handle suitability re-validation on drift?

## Sources (to verify)

- Directive 2014/65/EU (MiFID II)
- ESMA suitability guidelines
