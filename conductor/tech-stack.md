# Technology Stack

## Language
- **Python:** Chosen for its excellent capabilities in AI integration and rapid backend development.

## Backend Framework
- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design. It is highly suitable for building robust and scalable applications.

## Frontend Framework
- **Django Template:** Utilizing Django's built-in templating engine for a seamless, server-rendered frontend experience that tightly integrates with the backend logic.

## Database
- **PostgreSQL:** A powerful, open-source object-relational database system, ideal for ensuring data integrity and handling complex queries efficiently.

## AI & LLM Providers
- **Google Gemini (Default):** Utilized via `google-genai` SDK, specifically the `gemini-2.5-flash-lite` model for fast, cost-effective reasoning.
- **OpenAI:** Supported via `openai` SDK for tasks requiring high general intelligence.
- **Anthropic:** Supported via `anthropic` SDK for tasks needing sophisticated reasoning and large contexts.
- **Multi-Agent Packaging:** A custom abstract provider interface ensures consistent integration across different LLM backends.

## AI Workflow & Graph
- **LangGraph:** Used to implement the Inquiry Engine as a state machine workflow, providing fine-grained control over dialogue flows (Analyzer, Questioner, Empathizer) and enabling complex, looping agentic patterns.