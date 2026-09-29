# Decisions Log
One entry per significant design decision.

## Template
### ADR-NNN: <decision title>
- **Date:**
- **Status:** proposed / decided / replaced by ADR-NNN
- **Context:** what problem forced this decision
- **Options considered:** 2–3, with one line each on tradeoffs
- **Decision:** what I chose
- **Why (my words):**
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
- **Why (my words):** I've used Python the most of the three, so I can spend my time learning backend design instead of a new language. FastAPI is new to me, but it's a thin layer, so the SQL and transactions stay where I can see them. Spring Boot hides more of that in annotations and auto-configuration, and Go would mean building more plumbing myself before I get to the interesting parts. I also want to test a lot of scenarios, and pytest makes a large suite easy to write and read.
- **What would make me change it:** Finding that it can't support something already in the plan. The most likely case is deployment: if the server has to run on a low-end clinic laptop with no internet and Python + FastAPI turns out too heavy for that, I'd reconsider.
- **Summary (2 sentences):** Python + FastAPI, because I know Python best and FastAPI keeps the database logic visible. pytest makes it easy to cover the many edge cases dispensing has.
