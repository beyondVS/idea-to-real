# Implementation Plan: LLM Error Handling & Retry Logic

## Phase 1: Error Classification and Exception Handling Base [checkpoint: d02f967]
에러를 분류하기 위한 기초 예외 구조를 정의하고, 각 LLM 공급자(Provider)에서 발생하는 에러를 통합된 형식으로 변환하는 기능을 구현합니다.

- [x] Task: Define custom exception classes for LLM errors
    - [x] Write tests for `LLMBaseError`, `LLMTransientError`, `LLMPermanentError`
    - [x] Implement exception hierarchy in `agents/base.py` or a new `agents/exceptions.py`
- [x] Task: Implement error mapping for Gemini Provider
    - [x] Write tests for mapping `google.api_core.exceptions` to custom exceptions
    - [x] Implement error mapping logic in `agents/base.py` (Gemini implementation)
- [x] Task: Implement error mapping for OpenAI/Anthropic Providers (if applicable)
    - [x] Write tests for mapping provider-specific errors
    - [x] Implement error mapping logic in respective provider classes
- [x] Task: Conductor - User Manual Verification 'Phase 1: Error Classification' (Protocol in workflow.md)

## Phase 2: Exponential Backoff Retry Logic [checkpoint: 32036f8]
분류된 재시도 가능 에러에 대해 지수 백오프 전략을 적용한 재시도 데코레이터 또는 유틸리티를 구현합니다.

- [x] Task: Create retry utility with exponential backoff
    - [x] Write tests for `retry_with_backoff` function (verifying wait times and max retries)
    - [x] Implement `retry_with_backoff` utility in `agents/utils.py` or `agents/base.py`
- [x] Task: Apply retry logic to LLM call methods
    - [x] Write tests for `BaseAgent.generate` (or equivalent) simulating transient failures
    - [x] Apply retry decorator/wrapper to LLM calling logic
- [x] Task: Conductor - User Manual Verification 'Phase 2: Retry Logic' (Protocol in workflow.md)

## Phase 3: User Notification and UI Integration [checkpoint: 4942cd5]
에러 발생 시 사용자에게 적절한 메시지를 전달하고, 프론트엔드에서 이를 표시하는 기능을 강화합니다.

- [x] Task: Enhance error message generation logic
    - [x] Write tests for `get_user_friendly_message(exception)`
    - [x] Implement message generation logic based on error types
- [x] Task: Integrate error handling into Chat views
    - [x] Write integration tests for `chat/views.py` ensuring exceptions are caught and returned as context
    - [x] Update views to handle LLM errors gracefully and pass messages to templates
- [x] Task: Update UI templates to display specific error messages
    - [x] Manually verify error display in `chat/templates/chat/detail.html`
- [x] Task: Conductor - User Manual Verification 'Phase 3: User Notification' (Protocol in workflow.md)

## Phase: Review Fixes
- [x] Task: Apply review suggestions and augment tests ffa6f56