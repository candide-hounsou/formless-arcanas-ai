# RC-0001 — US adverse action notice (consumer credit)

## Status

Draft research brief (sources to verify).

## Summary

A consumer credit application is declined by an AI-assisted decisioning process.
The institution must issue an adverse action notice that is timely, attributable, and replayable.
This use case validates explicit responsibility, reason capture, and time-bound obligations.

## Jurisdiction

US

## Decision trigger

- Loan or credit card application recommendation is **deny** or **approve with materially worse terms**.

## Regulatory drivers (candidate)

- Equal Credit Opportunity Act (ECOA) and Regulation B (12 CFR Part 1002) — adverse action notice timing and reasons.
- Fair Credit Reporting Act (FCRA) — adverse action disclosures when consumer reports are used.

> Sources and exact sections must be verified before use.

## DecisionRecord mapping

- `context`: applicant profile, product, amount, jurisdiction=US, risk signals used.
- `recommendation`: DENY or REVIEW.
- `responsibility`: accountable credit officer + oversight role (if override).
- `legal_basis`: ECOA / Reg B / FCRA references (to confirm).
- `temporal`: notice deadline window (e.g., 30 days) captured as `expires_at`.
- `policy_snapshot_id`: policy active at decision time.

## Responsibility chain

- Primary: credit officer or underwriting lead (accountable).
- Secondary: compliance reviewer for adverse action notices (non-accountable but recorded).

## Data & evidence requirements

- Reason codes and model inputs used for the decision.
- Evidence of notice delivery (timestamp, channel).
- Audit trail of overrides or exception approvals.

## Replay & traceability

- Replay must reproduce recommendation and reason codes deterministically.
- Notice content should be reproducible from the decision record and policy snapshot.

## Open questions

- What specific notice timelines apply to product type?
- Which reason code taxonomy is accepted by internal compliance?
- How to store delivery confirmation in the ledger?

## Sources (to verify)

- ECOA / Regulation B (12 CFR Part 1002)
- FCRA adverse action provisions (15 U.S.C. §1681m)
