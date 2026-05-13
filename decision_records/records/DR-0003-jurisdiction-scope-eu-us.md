# DR-0003 — Expand Jurisdiction Scope to EU/US

- **Status:** accepted
- **Date:** 2026-05-13
- **Project version:** 0.1.0
- **Related PR:** TBD
- **Related commits:** TBD

## Context

The v1 contract restricted jurisdiction to FR only, which blocks incorporating EU and US real-world liability cases.
The research backlog requires EU/US examples and testable scenarios while keeping the rest of the contract stable.

## Decision

Expand the v1 jurisdiction scope to **EU/US**:
- `FinancialContext.jurisdiction` accepts only EU or US.
- Policy snapshots accept EU/US.
- Examples, demo, and sample data are aligned with the new scope.

## Consequences

- EU and US case studies can be modeled directly in the reference implementation.
- Existing FR-only assumptions are removed from validation and policy checks.
- Future policy snapshots must declare EU or US explicitly.

