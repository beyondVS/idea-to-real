# Specification: Build core conversational inquiry engine MVP

## Objective
Develop the foundational MVP for the Problem Specification AI System, focusing on the interactive 5 Whys and Socratic chat interface, real-time logical critique, and structured document export.

## Requirements
- **Chat Interface:** Users can input a vague problem and answer probing questions.
- **LLM Integration:** Connect to an LLM prompted to use Socratic methods and 5 Whys to drill down to the root cause.
- **Logic Critique Agent:** A background process that reviews the chat for logical fallacies or gaps in reasoning.
- **Document Generator:** Export the finalized, structured problem specification in Markdown and JSON formats.

## Tech Stack
- **Language:** Python
- **Backend:** Django
- **Frontend:** Django Templates
- **Database:** PostgreSQL