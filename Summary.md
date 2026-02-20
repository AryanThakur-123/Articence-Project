# Universal Data Connector — Project Summary
## Challenges Faced

One major challenge was integrating LLM function calling in a controlled way. Ensuring that the model did not hallucinate values required strict separation between tool outputs and conversational generation. I solved this by enforcing structured function schemas and passing only validated backend data to the LLM.

Another challenge was designing connectors that supported filtering, pagination, and standardized responses across different data domains (CRM, Support, Analytics). I addressed this by defining a base connector interface and implementing domain-specific connectors that adhered to a shared response contract.

## Design Decisions & Tradeoffs

I chose a modular layered architecture:

Router Layer (API entry point)

LLM Handler (function calling orchestration)

Connector Layer (data source abstraction)

Business Rules Engine

Voice Optimizer

Tradeoffs:

Used JSON-based mock data instead of a real database for simplicity.

Kept connectors synchronous to reduce complexity.

Used structured metadata instead of dynamic response shaping.

These tradeoffs improved clarity and maintainability at the cost of production-scale readiness.

## What I Would Improve With More Time

Replace JSON storage with PostgreSQL.

Convert connectors to fully asynchronous operations.

Add Redis caching.

Implement authentication (JWT).

Add CI/CD pipeline.

Add monitoring with Prometheus + structured metrics.

Add comprehensive integration tests for LLM workflows.

## What I Learned

This project taught me:

How to design extensible backend architectures.

How to safely integrate LLM function calling.

How to structure connectors for multi-domain data.

How to implement production-level logging and testing.

How to containerize services for deployment.

Most importantly, I learned how to treat LLMs as controlled orchestration layers rather than direct data sources.
