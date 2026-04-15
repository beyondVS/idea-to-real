# Initial Concept
본 프로젝트는 사용자의 간략한 아이디어를 입력받아 5 Whys 및 소크라테스식 질문법을 통해 문제의 근본 원인을 파악하고, 논리적 무결성이 검증된 **'구조화된 문제 기술서(Problem Specification)'**를 생성하는 AI 멀티 에이전트 시스템의 기초 단계를 구축하는 것을 목적으로 합니다.

# Problem Specification AI System

## Vision
To provide a structured, logical approach to problem definition using AI, moving from vague ideas to a high-quality, verified problem specification.

## Target Users
- **Software Developers & Architects:** For refining complex system designs and identifying architectural bottlenecks.
- **Business Strategists & Product Managers:** For validating market problems and clarifying product vision.
- **Creative Thinkers & Researchers:** For brainstorming and systematic root cause analysis in any domain.

## Key Goals
- **Root Cause Identification:** Systematically drilling down to the core issue using the 5 Whys technique.
- **Logical Consistency Verification:** Ensuring the problem statement is sound and free of logical fallacies.
- **Standardized Specification Generation:** Producing a high-quality, structured document for downstream development or analysis.

## Core Features
- **LangGraph-based Inquiry Engine:** A state-machine powered AI agent specialized in asking probing questions using 5 Whys and Socratic methods. It utilizes independent 'Analyzer', 'Questioner', and 'Empathizer' nodes to ensure logical depth and emotional resonance in every turn.
- **Multi-Agent Reflection & Critique:** Multiple agents that review and validate each other's reasoning and conclusions.
- **Structured Document Exporter:** Automatically transforming the interaction history into a structured 'Problem Specification'.

## Problem Scope
- **Technical & Engineering Challenges:** Addressing complex software bugs, architectural flaws, or engineering constraints.
- **Process & Organizational Inefficiencies:** Identifying bottlenecks in team workflows or organizational structures.
- **Product & User Experience Gaps:** Validating user pain points and the underlying needs for new features.
