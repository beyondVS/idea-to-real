# Implementation Plan: Add Ollama Provider for Local Development

## Phase 1: Environment Setup and Core Configuration [checkpoint: b2a4248]

- [x] Task: Update environment configuration for Ollama (25c4786)
    - [x] `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT` 등 필요 변수를 `.env.example`에 추가
    - [x] Django `settings.py`에서 Ollama 관련 설정을 로드하도록 수정
- [x] Task: Conductor - User Manual Verification 'Phase 1: Environment Setup and Core Configuration' (Protocol in workflow.md) (b2a4248)

## Phase 2: OllamaProvider Implementation (TDD) [checkpoint: 1605e57]

- [x] Task: Define OllamaProvider Foundation (bef6d64)
    - [x] **Red Phase:** `agents/test_providers.py`에 OllamaProvider 초기화 및 설정 로딩 테스트 작성 (실패 확인)
    - [x] **Green Phase:** `agents/base.py` 또는 제공자 정의 파일에 `OllamaProvider` 클래스 뼈대 구현 (테스트 통과)
    - [x] **Refactor:** 코드 정리 및 테스트 커버리지 확인
- [x] Task: Implement Chat Completion for Ollama (4511918)
    - [x] **Red Phase:** Ollama API 호출 및 응답 파싱에 대한 단위 테스트 작성 (성공/실패 케이스 포함)
    - [x] **Green Phase:** `OllamaProvider.generate()` 메서드 구현 및 실제 API 연동
    - [x] **Refactor:** 오류 처리 및 예외 계층 구조(Unified Exception Hierarchy) 반영
- [x] Task: Conductor - User Manual Verification 'Phase 2: OllamaProvider Implementation (TDD)' (Protocol in workflow.md) (1605e57)

## Phase 3: System Integration and Verification

- [ ] Task: Register OllamaProvider in Provider Factory
    - [ ] 시스템 전역에서 Ollama를 프로바이더로 선택할 수 있도록 팩토리 로직 업데이트
- [ ] Task: Verify Full Workflow with Ollama
    - [ ] `tests/test_full_workflow.py`를 실행하여 Ollama 기반으로 전체 인쿼리 엔진이 작동하는지 확인
    - [ ] Ollama 미실행 시 "Friendly Notification" 에러 처리가 의도대로 작동하는지 검증
- [ ] Task: Conductor - User Manual Verification 'Phase 3: System Integration and Final Verification' (Protocol in workflow.md)
