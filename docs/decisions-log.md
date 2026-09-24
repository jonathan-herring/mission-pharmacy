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
- **Date:**
- **Status:** proposed
- **Context:** The backend has to enforce stock correctness under concurrent dispensing, expose a sync endpoint for offline clients, and stay small enough for one developer to understand end to end. I want a framework that keeps SQL, transactions, and HTTP handling visible rather than generated behind the scenes.
- **Options considered:**
  - Python + FastAPI: thin framework, so routing, validation, and SQL stay explicit; Pydantic models double as the API schema; pytest and Testcontainers make real-database concurrency tests straightforward
  - Java + Spring Boot: mature transaction management and strong typing, builds on my Kotlin/JVM experience; much of the behavior lives in annotations and auto-configuration, which hides the mechanics I want to learn
  - Go: simple concurrency model and fast binaries; smaller ecosystem for validation and migrations means more hand-built plumbing before the interesting parts
- **Decision:**
- **Why (my words):**
- **What would make me change it:**
- **Summary (2 sentences):**
