# Implementation Plan: Interactive Chat Feedback System

## Phase 1: Research & Setup
- [ ] Task: Research existing chat implementation
    - [ ] `chat/templates/chat/detail.html`의 메시지 전송 로직 분석
    - [ ] `chat/views.py`의 응답 처리 방식 확인 (JSON 또는 HTML 프래그먼트 반환 여부 결정)
- [ ] Task: Conductor - User Manual Verification 'Research & Setup' (Protocol in workflow.md)

## Phase 2: UI Structure & Styling
- [ ] Task: Create Loading Indicator UI
    - [ ] 애니메이션이 포함된 '답변 작성 중...' HTML/CSS 정의
- [ ] Task: Create Final Result Card UI
    - [ ] '문제 기술서'를 시각적으로 강조할 카드 스타일(CSS) 정의
- [ ] Task: Conductor - User Manual Verification 'UI Structure & Styling' (Protocol in workflow.md)

## Phase 3: Async Logic Implementation (TDD)
- [ ] Task: Write Tests for Async Interaction
    - [ ] JavaScript 동작을 테스트할 수 있는 프레임워크(있을 경우) 또는 브라우저 테스트 시나리오 작성
- [ ] Task: Implement Async Message Handling
    - [ ] `detail.html`에서 폼 전송 이벤트를 가로채고 `fetch` API로 비동기 전송 구현
    - [ ] 메시지 전송 시 즉시 '로딩 인디케이터'를 DOM에 삽입
- [ ] Task: Implement Response Rendering
    - [ ] 서버로부터 응답 수신 시 '로딩 인디케이터' 제거
    - [ ] 수신된 응답(일반 메시지 또는 최종 기술서 카드)을 DOM에 렌더링
- [ ] Task: Conductor - User Manual Verification 'Async Logic' (Protocol in workflow.md)

## Phase 4: Final Integration & Polishing
- [ ] Task: Backend View Refactoring (if needed)
    - [ ] 비동기 요청에 대응할 수 있도록 `views.py`에서 JSON 응답 또는 Partial HTML 반환 처리
- [ ] Task: End-to-End Test
    - [ ] 실제 5 Whys 과정 전체를 수행하며 로딩 표시 -> 응답 -> 최종 결과물 출력이 정상인지 확인
- [ ] Task: Conductor - User Manual Verification 'Final Integration' (Protocol in workflow.md)
