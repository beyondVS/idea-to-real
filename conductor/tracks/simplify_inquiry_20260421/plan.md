# Implementation Plan: Inquiry Engine Simplification (simplify_inquiry_20260421)

이 계획은 불필요한 에이전트를 제거하고 질문 전략을 간소화하여 시스템을 최적화하는 과정을 단계별로 정의합니다.

## Phase 1: CritiqueAgent 제거 및 InquiryAgent 전략 수정 [checkpoint: b5ca66b]
- [x] Task: `agents/critique.py` 파일 및 관련 단위 테스트(`agents/test_critique.py` 등) 삭제
- [x] Task: `agents/inquiry.py`의 `InquiryAgent.SYSTEM_PROMPT`에서 소크라테스식 질문법 관련 내용 삭제 및 '간결한 5 Whys'로 전략 수정
- [x] Task: 수정된 `InquiryAgent`에 대한 단위 테스트 작성 및 기존 테스트 업데이트
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: LangGraph 워크플로우 리팩토링 [checkpoint: 6dedfa2]
- [x] Task: `agents/base.py` (또는 Graph 정의 위치)에서 Critique 노드 및 관련 엣지(Edge) 정의 제거
- [x] Task: 워크플로우를 InquiryAgent 응답 후 즉시 종료하거나 요약 단계로 이어지도록 재구성
- [x] Task: `tests/test_inquiry_graph.py` 등 통합 테스트 파일을 수정된 그래프 구조에 맞춰 업데이트
- [x] Task: 전체 워크플로우 실행 테스트 및 논리적 흐름 검증
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)


## Phase 3: 최종 검증 및 정리
- [x] Task: 전체 테스트 스위트 실행 및 코드 커버리지 확인 (>80%)
- [x] Task: 사용되지 않는 코드 조각 및 주석 정리
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
