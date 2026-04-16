# Implementation Plan: LLM Error Handling & Retry Logic

## Phase 1: Error Classification and Exception Handling Base
에러를 분류하기 위한 기초 예외 구조를 정의하고, 각 LLM 공급자(Provider)에서 발생하는 에러를 통합된 형식으로 변환하는 기능을 구현합니다.

- [ ] Task: Define custom exception classes for LLM errors
    - [ ] Write tests for `LLMBaseError`, `LLMTransientError`, `LLMPermanentError`
    - [ ] Implement exception hierarchy in `agents/base.py` or a new `agents/exceptions.py`
- [ ] Task: Implement error mapping for Gemini Provider
    - [ ] Write tests for mapping `google.api_core.exceptions` to custom exceptions
    - [ ] Implement error mapping logic in `agents/base.py` (Gemini implementation)
- [ ] Task: Implement error mapping for OpenAI/Anthropic Providers (if applicable)
    - [ ] Write tests for mapping provider-specific errors
    - [ ] Implement error mapping logic in respective provider classes
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Error Classification' (Protocol in workflow.md)

## Phase 2: Exponential Backoff Retry Logic
분류된 재시도 가능 에러에 대해 지수 백오프 전략을 적용한 재시도 데코레이터 또는 유틸리티를 구현합니다.

- [ ] Task: Create retry utility with exponential backoff
    - [ ] Write tests for `retry_with_backoff` function (verifying wait times and max retries)
    - [ ] Implement `retry_with_backoff` utility in `agents/utils.py` or `agents/base.py`
- [ ] Task: Apply retry logic to LLM call methods
    - [ ] Write tests for `BaseAgent.generate` (or equivalent) simulating transient failures
    - [ ] Apply retry decorator/wrapper to LLM calling logic
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Retry Logic' (Protocol in workflow.md)

## Phase 3: User Notification and UI Integration
에러 발생 시 사용자에게 적절한 메시지를 전달하고, 프론트엔드에서 이를 표시하는 기능을 강화합니다.

- [ ] Task: Enhance error message generation logic
    - [ ] Write tests for `get_user_friendly_message(exception)`
    - [ ] Implement message generation logic based on error types
- [ ] Task: Integrate error handling into Chat views
    - [ ] Write integration tests for `chat/views.py` ensuring exceptions are caught and returned as context
    - [ ] Update views to handle LLM errors gracefully and pass messages to templates
- [ ] Task: Update UI templates to display specific error messages
    - [ ] Manually verify error display in `chat/templates/chat/detail.html`
- [ ] Task: Conductor - User Manual Verification 'Phase 3: User Notification' (Protocol in workflow.md)