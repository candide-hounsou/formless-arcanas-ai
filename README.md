# 🜁 formless‑arcanas‑ai

**A liability‑aware financial decision engine built with Pydantic AI**

> *If your agent cannot explain who is responsible for a decision, it should not make one.*

---

## What is `formless‑arcanas‑ai`?

`formless‑arcanas‑ai` is an open‑source **reference project** that demonstrates a class of agentic systems that most AI frameworks cannot express:

> **Deterministic, auditable, liability‑aware financial decisions.**

Instead of optimizing for *“best answer”*, `formless‑arcanas‑ai` optimizes for:

- **Defensibility**
- **Replayability**
- **Responsibility attribution**
- **Temporal validity**

This project exists to show what becomes possible when **strong typing, schema validation, and agentic reasoning are treated as first‑class invariants**, not optional safeguards.

---

## Why this project exists

Modern agent frameworks are excellent at:
- invoking tools,
- reasoning step‑by‑step,
- generating text.

They are *not* designed to answer the questions that matter in regulated finance:

- Who is responsible for this decision?
- Under which regulation was it made?
- For how long is this decision valid?
- Can this decision be replayed exactly as it was made?
- What happens when its assumptions expire?

`formless‑arcanas‑ai` answers those questions **by construction**.

---

## What `formless‑arcanas‑ai` is **not**

- ❌ a chatbot  
- ❌ a RAG system  
- ❌ a scoring model  
- ❌ a workflow engine  
- ❌ a replacement for quantitative models  

This project does **not** try to outperform financial models.  
It exists *around* them — where governance, auditability, and responsibility live.

---

## Core idea

Every AI‑assisted financial decision is treated as a **Decision Record** that must satisfy **non‑negotiable invariants**.

A decision that is:
- not attributable,
- not replayable,
- not time‑bounded,

is considered **invalid**, regardless of how “reasonable” it sounds.

---

## What makes this project different

### 1. Decisions are structured, not textual

Every decision is a **validated object**, not free‑form text.

```text
Decision = Data + Responsibility + Time + Legal Basis
```

### 2. Responsibility is explicit

Each decision carries a **Responsibility Graph**:
- AI components involved
- Human overrides
- Organizational roles
- Escalation paths

### 3. Time is a first‑class constraint

Every decision:
- has a `valid_from` timestamp
- has an `expires_at` boundary
- can become *invalid* without being *wrong*

### 4. Replayability is mandatory

If a decision cannot be replayed deterministically, it is treated as non‑auditable.

---

## Why **Pydantic AI**

This project is intentionally built on **Pydantic AI**, because the design goals cannot be achieved with prompt‑centric or untyped agent frameworks.

Pydantic AI enables:

- **Strict schema enforcement** on agent outputs
- **Retry‑on‑validation failure**, not just retry‑on‑error
- **Typed dependency injection** into agent reasoning
- **Deterministic evaluation & replay**
- **Audit‑friendly observability**

`formless‑arcanas‑ai` is meant to demonstrate *why these properties matter*, not just that they exist.

---

## Why this is impossible in LangChain / LangGraph

This project is intentionally designed to demonstrate a category of agentic system that **cannot be expressed cleanly — or at all — in mainstream agent frameworks**, including LangChain and LangGraph.

This is not a critique of those frameworks’ usefulness.  
It is a statement about **design constraints**.

---

### 1. Prompt‑centric vs invariant‑centric design

LangChain‑style systems are fundamentally **prompt‑centric**:

- agent “state” lives in prompts and messages
- correctness is probabilistic
- outputs are usually text-first, parsing later

In contrast, `formless‑arcanas‑ai` is **invariant‑centric**:

- agent outputs must conform to **non‑negotiable schemas**
- failure to satisfy constraints is not “handled”, it is **rejected**
- a decision that cannot be validated **does not exist**

In LangChain, validation is optional and external.  
In this project, validation is *the definition of success*.

---

### 2. Responsibility cannot be modeled as prompts

A core requirement in this system is a **Responsibility Graph**:

- which AI components contributed
- which humans approved or overrode
- which organizational roles are accountable
- how responsibility transfers over time

LangChain and LangGraph provide no **native abstraction** for:

- responsibility attribution
- liability transfer
- authority boundaries

Attempting to encode responsibility in prompt text leads to:

- ambiguity
- non‑determinism
- zero audit value

In `formless‑arcanas‑ai`, responsibility is a **typed structure**, not a narrative.

---

### 3. Time‑bounded validity is not a LangChain concept

Financial decisions are not timeless.

A decision can be:
- correct when made
- invalid today
- dangerous tomorrow

LangChain has no first‑class concept of:

- `valid_from`
- `expires_at`
- decision invalidation without error

Time must be modeled explicitly in schemas and enforced mechanically.  
This is outside the design intent of prompt‑driven agent graphs.

---

### 4. Deterministic replay is structurally unsupported

A central invariant of this project:

> A decision must be replayable exactly as it was produced, or it is not auditable.

LangChain systems:
- depend on mutable prompts
- depend on evolving chain logic
- rarely guarantee identical re‑execution

In `formless‑arcanas‑ai`, replayability is enforced by:
- schema‑locked outputs
- hashed decision states
- explicit dependency injection

This level of determinism is **structurally incompatible** with prompt‑assembled chains.

---

### 5. “Retry until valid” is different from “retry until it sounds right”

LangChain retries are usually triggered by:
- exceptions
- tool failures
- parsing errors

Pydantic AI retries are triggered by:
- **schema violations**
- **invariant breaches**
- **semantic invalidity**

This difference is critical.

In this project, an agent is forced to reason again **until it produces a legally admissible decision object** — not just a plausible string.

---

## A minimal LangChain attempt (and where it breaks)

To make the comparison concrete, consider what a *good‑faith*, minimal LangChain implementation of a “decision record” might look like.

### What the attempt looks like

In LangChain, one would typically:
- prompt an LLM to return a JSON‑like structure
- parse that structure into a Python object
- store the parsed result for later use

Conceptually:

```python
prompt = """
Make a credit decision and include:
- recommendation
- rationale
- responsible party
- validity period
"""

result = llm.invoke(prompt)
decision = json.loads(result)
```

At first glance, this seems workable.

It is not.

---

### Where it breaks (structurally)

#### 1. Responsibility is narrative, not enforceable

In this setup, “responsible party” is:
- a string produced by an LLM
- unverifiable
- unbounded
- non‑transferrable

Nothing prevents the model from:
- omitting responsibility
- inventing authority
- changing attribution across retries

There is no mechanism to *reject* a decision that fails to satisfy responsibility invariants — only to notice it after the fact.

---

#### 2. Time validity cannot be enforced

The LLM may produce:
- inconsistent date formats
- expired validity windows
- no time boundaries at all

LangChain does not provide:
- mandatory temporal constraints
- execution failure on temporal invalidity
- automatic decision expiration

As a result, **a decision can remain “accepted” long after it is no longer valid**.

---

#### 3. Retry logic optimizes for syntax, not admissibility

LangChain retries generally occur when:
- parsing fails
- a tool errors

They do *not* retry because:
- responsibility is missing
- legal basis is insufficient
- temporal scope is unsafe

A decision that *sounds reasonable* but is **legally inadmissible** will pass through unchanged.

---

#### 4. Replayability is not guaranteed

Re‑running the same chain later typically involves:
- different prompt versions
- updated chain logic
- different hidden state

Even with careful controls, **semantic replay is not guaranteed**.

In regulated finance, “approximately the same decision” is not replay.

---

#### 5. Failure is silent

Most importantly, when LangChain fails in this context:
- it fails *silently*
- downstream systems inherit risk without visibility
- responsibility becomes retroactive guesswork

This is not a LangChain bug — it is a consequence of design philosophy.

---

### Why `formless‑arcanas‑ai` does not break here

In contrast:

- A decision **cannot exist** unless it satisfies schema invariants
- Missing responsibility causes **hard failure**
- Invalid time windows are **rejected at execution**
- Schema‑driven retries force admissibility, not fluency
- Replay is a design requirement, not a best‑effort property

The difference is not “better prompts”.  
It is **a different category of system**.

---

## Architecture overview

```text
formless/
├─ core/
│  ├─ decision.py            # Canonical decision schema
│  ├─ responsibility.py     # Responsibility graph model
│  ├─ temporal.py           # Time‑bounded validity
│  └─ invariants.py         # Non‑violable constraints
│
├─ agents/
│  └─ credit_decision.py     # Optional Pydantic AI agent skeleton (no API key required unless executed)
│
├─ ledger/
│  ├─ event_log.py           # Append‑only decision log
│  └─ replay.py              # Deterministic replay engine
│
└─ demo_fail_fast.py         # One‑file runnable demo
```

---

## Quickstart

### 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the one‑file demo (fail fast on missing responsibility)

```bash
python demo_fail_fast.py
```

You should see:
- a validation/invariant failure for the bad decision
- a successful commit + replay verification for the corrected decision

---

## License

MIT — use freely, attribute responsibly.

---

## Final note

> An AI system that cannot explain its responsibility boundaries  
> should not be trusted with financial decisions.

That is the thesis of **`formless‑arcanas‑ai`**.
