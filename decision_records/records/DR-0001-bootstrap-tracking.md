# DR-0001 — Bootstrap Decision Tracking

- **Status:** accepted
- **Date:** 2026-05-10
- **Project version:** 0.1.0
- **Related PR:** TBD
- **Related commits:** TBD

## Context

The project needs a durable way to track governance decisions while development accelerates.
Core traceability targets are lingering questions, answers, PR links, commits, versioning, and event dates.

## Decision

Create a root `decision_records/` folder with:
- markdown decision records in `records/`,
- append-only synthetic timeline in `events.jsonl`.

## Consequences

- Governance context is explicit and reviewable.
- Open questions are visible until closure.
- Version and change references remain linked to decisions.

## Lingering questions

1. Should Decision Record IDs be global (`DR-XXXX`) or per domain (`CORE-DR-XXXX`)?
2. Should `events.jsonl` become hash-chained for tamper evidence?
3. What is the minimum required metadata to enforce for each event?

## Answers (current)

1. Start with global IDs; revisit if domain count grows.
2. Keep synthetic plain JSONL now; add hash-chaining in ledger hardening phase.
3. Require event_id, event_date, event_type, project_version, and references when available.
