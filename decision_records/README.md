# Decision Records

This folder stores Architecture/Decision Records for project governance.

## Purpose

Track over time:
- lingering questions,
- answers and rationale,
- related PRs,
- related commits,
- project version at decision time,
- event dates,
- ADR follow-up suggestions for unresolved strategic items.

## Structure

- `records/`: human-readable decision records (`DR-XXXX-*.md`)
- `events.jsonl`: append-only event feed for synthetic tracking and replay

## Minimal workflow

1. Add/update a record in `records/`.
2. Append one or more events to `events.jsonl`.
3. Reference PR + commit + version in both places.
4. Keep unresolved items in a `Lingering questions` or `ADR follow-up suggestions` section until closure.

## Naming convention

- Record IDs: `DR-0001`, `DR-0002`, ...
- Event IDs: `EVT-YYYYMMDD-###`
