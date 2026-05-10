# DR-0002 — Roadmap Freeze and Governance Answers (v1)

- **Status:** accepted
- **Date:** 2026-05-10
- **Project version:** 0.1.0
- **Related PR:** TBD
- **Related commits:** TBD

## Context

The project required converting roadmap questions into implementation decisions for a liability-aware finance reference implementation.
Answers were provided for the 10-step roadmap and needed to be codified in architecture and governance records.

## Decisions

1. **Canonical contract freeze (Step 1)**
   - `decision_id` is UUIDv7.
   - No backward compatibility guarantee for prior JSONL shape.
   - v1 jurisdiction scope is FR only.

2. **Policy/invariant stratification (Step 2)**
   - National rules are treated as mandatory constraints in policy snapshots.
   - Policy changes are effective-dated and replayable historically.
   - Exception authorities are suggested as: Risk Committee, CRO, Compliance Officer.

3. **Responsibility engine (Step 3)**
   - Overrides transfer liability.
   - Accountability is role-specific and human.
   - Four-eyes/dual-control is not mandatory in v1 baseline.

4. **Evaluator layer (Step 4)**
   - First regulator persona: internal compliance.
   - Evaluators emit both score and pass/fail.
   - Evaluator outputs are immutable records.

5. **Ledger hardening (Step 5)**
   - JSONL remains storage backend for v1.
   - Tamper-evidence is sufficient for v1.
   - Retention/deletion constraints are tracked in ledger metadata.

6. **Replay and temporal governance (Step 6)**
   - Replay requires original model provider/version provenance.
   - Re-review trigger is internal audit.
   - External data drift handling remains open (see follow-ups).

7. **Business proof scenarios (Step 7)**
   - Flagship use case: portfolio risk shift.
   - Synthetic data packs are required for demos.
   - Primary audience: internal governance teams.

8. **Assurance baseline (Step 8)**
   - Finance-grade acceptance floor target: 0.99.
   - Adversarial testing required (prompt injection, fabricated legal basis).
   - Tolerated false positive rate target: 0.01.

9. **Documentation/positioning (Step 9)**
   - Project is positioned as a reference implementation.
   - Compliance boundary statement is mandatory.

10. **v0.2 release criteria (Step 10)**
    - Release requires completed modules, evaluators, deterministic tests, examples, and frozen versioned contract.

## ADR follow-up suggestions (open items)

1. **External data drift policy**
   - Option A: snapshot critical external inputs in ledger envelope.
   - Option B: require signed data extracts for replay-critical fields.
   - Option C: classify replay-critical vs contextual-only fields and score drift severity.

2. **Legal/marketing-safe claims**
   - Safe claims: deterministic replay verification, explicit liability modeling, policy-effective dating.
   - Avoid claims: guaranteed regulatory compliance, legal admissibility in all jurisdictions.

3. **Enterprise proof artifacts**
   - Required: replay report, invariant/policy test report, retention policy statement, model provenance manifest.

4. **Milestone/demonstration proposal**
   - Target demo window suggestion: 4–6 weeks after contract freeze.
   - Demo audience suggestion: internal compliance + risk governance + architecture reviewers.

5. **Community contribution timing**
   - Suggestion: accept scoped contributions now for examples/tests; freeze core API before broad extension proposals.

6. **Integration priority suggestions**
   - Priority 1: model provider provenance adapters.
   - Priority 2: internal KYC/risk signal feed adapters.
   - Priority 3: compliance reporting export adapters.

## Consequences

- Roadmap ambiguity is materially reduced.
- Governance decisions are now explicit and traceable.
- Remaining unknowns are contained in actionable ADR follow-up topics.
