# Technology Stack

## Language
- **Python:** Chosen for its excellent capabilities in AI integration and rapid backend development.

## Backend Framework
- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design. It is highly suitable for building robust and scalable applications.

## Frontend Framework
- **Django Template:** Utilizing Django's built-in templating engine for a seamless, server-rendered frontend experience that tightly integrates with the backend logic.
- **Vanilla JavaScript (Fetch API):** Employed for asynchronous client-server interactions, eliminating page reloads and providing immediate UI feedback during AI processing.

## Database
- **PostgreSQL:** A powerful, open-source object-relational database system, ideal for ensuring data integrity and handling complex queries efficiently.

## AI & LLM Providers
- **Google Gemini (Default):** Utilized via `google-genai` SDK, specifically the `gemini-2.5-flash-lite` model for fast, cost-effective reasoning.
- **OpenAI:** Supported via `openai` SDK for tasks requiring high general intelligence.
- **Anthropic:** Supported via `anthropic` SDK for tasks needing sophisticated reasoning and large contexts.
- **Ollama (Local AI):** Integrated via the official `ollama` Python package for cost-effective local development and privacy-focused reasoning.
- **Multi-Agent Packaging:** A custom abstract provider interface ensures consistent integration across different LLM backends.

## Resilience & Reliability
- **Error Classification:** Provider-specific errors are mapped to a unified exception hierarchy (Transient vs. Permanent).
- **Exponential Backoff Retry:** Automatic retries for transient errors (Rate Limits, Timeouts) using a decorator-based approach.
- **User-Friendly Error Notification:** Meaningful guidance provided to users when LLM calls fail.

## AI Workflow & Graph
- **LangGraph:** Used to implement the Inquiry Engine as a state machine workflow, providing fine-grained control over dialogue flows (Analyzer, Questioner) and enabling complex, looping agentic patterns.
