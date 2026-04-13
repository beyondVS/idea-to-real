# Implementation Plan: LLM Packaging for Multi-Agent Support

## Phase 1: Core LLM Provider Interface [checkpoint: 9dfceff]
다양한 LLM 프로바이더를 일관된 방식으로 다룰 수 있는 인터페이스와 베이스 클래스를 구축합니다.

- [x] Task: Define Base LLM Provider Class [50abecf]
    - [x] `agents/base.py` 에 모든 LLM 프로바이더가 상속받을 추상 베이스 클래스 정의.
    - [x] 공통 메서드(`generate_response`, `handle_tool_call` 등) 명세 작성.
- [x] Task: Implement Gemini Provider (Default) [50abecf]
    - [x] `google-genai` 라이브러리를 활용한 Gemini 전용 프로바이더 구현.
    - [x] 테스트 코드 작성 및 검증.
- [x] Task: Implement OpenAI and Anthropic Providers [50abecf]
    - [x] `openai`, `anthropic` 라이브러리를 활용한 프로바이더 구현.
    - [x] 각 프로바이더별 단위 테스트 작성 및 통과 확인.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Core LLM Provider Interface' (Protocol in workflow.md) [9dfceff]

## Phase 2: Agent-Model Mapping and Configuration
에이전트가 환경 변수를 통해 모델을 선택하고 사용할 수 있는 매핑 시스템을 구축합니다.

- [ ] Task: Create Provider Factory and Environment Config
    - [ ] 에이전트 이름에 따라 적절한 프로바이더를 반환하는 `ProviderFactory` 구현.
    - [ ] 환경 변수(`.env`)를 통한 에이전트별 모델 맵핑 설정 기능 추가.
- [ ] Task: Update Base Agent to use Provider
    - [ ] `BaseAgent` 클래스가 직접 API를 호출하는 대신 프로바이더 인터페이스를 사용하도록 리팩토링.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Agent-Model Mapping and Configuration' (Protocol in workflow.md)

## Phase 3: Common Agent Features Enhancement
모든 에이전트가 공통적으로 사용할 수 있는 고급 기능들을 프로바이더 인터페이스에 통합합니다.

- [ ] Task: Implement Tool Use Support in Wrapper
    - [ ] 각 프로바이더의 Tool Calling 기능을 통합된 인터페이스로 노출.
- [ ] Task: Implement Short-term Memory Context
    - [ ] 프로바이더 레벨에서 대화 이력을 관리하고 프롬프트에 포함시키는 기능 추가.
- [ ] Task: Implement System Prompt Customization
    - [ ] 각 에이전트의 역할에 맞는 시스템 프롬프트를 프로바이더에 전달하는 구조 강화.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Common Agent Features Enhancement' (Protocol in workflow.md)
