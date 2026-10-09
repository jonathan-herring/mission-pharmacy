# Decisions Log
One entry per significant design decision.

## Template
### ADR-NNN: <decision title>
- **Date:**
- **Status:** proposed / decided / replaced by ADR-NNN
- **Context:** what problem forced this decision
- **Options considered:** 2–3, with one line each on tradeoffs
- **Decision:** what I chose
- **Why:**
- **What would make me change it:**
- **Summary (2 sentences):**

---

### ADR-001: Backend language and framework
- **Date:** 2026-09-29
- **Status:** decided
- **Context:** The backend has to enforce stock correctness under concurrent dispensing, expose a sync endpoint for offline clients, and stay small enough for one developer to understand end to end. I want a framework that keeps SQL, transactions, and HTTP handling visible rather than generated behind the scenes.
- **Options considered:**
  - Python + FastAPI: thin framework, so routing, validation, and SQL stay explicit; Pydantic models double as the API schema; pytest and Testcontainers make real-database concurrency tests straightforward
  - Java + Spring Boot: mature transaction management and strong typing, builds on my Kotlin/JVM experience; much of the behavior lives in annotations and auto-configuration, which hides the mechanics I want to learn
  - Go: simple concurrency model and fast binaries; smaller ecosystem for validation and migrations means more hand-built plumbing before the interesting parts
- **Decision:** Python + FastAPI
- **Why:** I've used Python the most of the three, so I can spend my time learning backend design instead of a new language. FastAPI is new to me, but it's a thin layer, so the SQL and transactions stay where I can see them. Spring Boot hides more of that in annotations and auto-configuration, and Go would mean building more plumbing myself before I get to the interesting parts. I also want to test a lot of scenarios, and pytest makes a large suite easy to write and read.
- **What would make me change it:** Finding that it can't support something already in the plan. The most likely case is deployment: if the server has to run on a low-end clinic laptop with no internet and Python + FastAPI turns out too heavy for that, I'd reconsider.
- **Summary (2 sentences):** Python + FastAPI, because I know Python best and FastAPI keeps the database logic visible. pytest makes it easy to cover the many edge cases dispensing has.

### ADR-002: How stock is stored
- **Date:** 2026-10-09
- **Status:** decided
- **Context:** Stock changes for several reasons: dispensing, shipments arriving, recounts, and expired or damaged stock being thrown out. The app needs the current count for every drug on the prescriber screen, and a record of why the count changed. A confirmed over-dispense (the volunteer has more on hand than the app shows) also has to be recorded without stock going below zero.
- **Options considered:**
  - Stock column plus a dispenses log: simplest, but restocks, recounts, and write-offs leave no record
  - Ledger only (`stock_changes`), with stock calculated as the sum of its rows: full history and one source of truth, but every read adds up rows and `CHECK (stock >= 0)` can't apply to a sum
  - Ledger plus a `stock` column on `drugs`, updated together in one transaction: full history and a single value to read, constrain, and lock; the cost is keeping the two in sync
- **Decision:** Ledger plus a `stock` column. Each row in `stock_changes` has a type (received, dispensed, correction, recount, expired) and a signed amount. On a confirmed over-dispense, one transaction writes a `correction` row bringing stock up to the dispensed amount, then a `dispensed` row, updates `drugs.stock`, and sets `recount_needed`. Stock never goes below zero, and the ledger always sums to the column.
- **Why:** The ledger gives traceability. Every change to a drug's stock is its own row saying what happened and by how much, so I can trace how the count got to where it is. The stock column holds the current count, so reading it is a single lookup instead of adding up every ledger row for that drug. The column also makes simultaneous dispenses safe. Each dispense updates the drug's row, and the database locks that row during the update, so a second dispense waits and then sees the new count. With only a ledger, two dispenses can both pass the stock check before either one writes, and nothing stops the total from going negative.
- **What would make me change it:** If the column and the ledger keep drifting apart, for example because some code path updates one without the other, the column is costing more than it saves. Offline sync could also force a rethink if stock changes arrive out of order and can't be applied in one transaction.
- **Summary (2 sentences):** Every stock change is recorded as a row in a `stock_changes` ledger, and `drugs.stock` holds the current count. Both are updated in one transaction, which gives a full history plus a single row the database can constrain and lock.
