# Implementation Plan: LangGraph Inquiry Engine (plan.md)

## Phase 1: Environment Setup & State Definition
- [x] Task: LangGraph 및 관련 의존성(`langgraph`) 설치 및 환경 설정 [ca1cb30]
- [ ] Task: Inquiry 워크플로우를 위한 `GraphState` 클래스 정의 (history, step_count, metadata 등)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment Setup & State Definition' (Protocol in workflow.md)

## Phase 2: Node Implementation
- [ ] Task: `Analyzer` 노드 구현 (논리적 비약 분석 및 메타데이터 추출)
- [ ] Task: `Questioner` 노드 구현 (5 Whys 및 소크라테스식 질문 생성)
- [ ] Task: `Empathizer` 노드 구현 (공감 및 한국어 톤앤매너 적용)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Node Implementation' (Protocol in workflow.md)

## Phase 3: Edge Logic & Workflow Construction
- [ ] Task: 조건부 엣지(Edge) 로직 구현 (근본 원인 식별 및 사용자 종료 조건)
- [ ] Task: 전체 LangGraph 워크플로우 구성 및 컴파일
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Edge Logic & Workflow Construction' (Protocol in workflow.md)

## Phase 4: Django Integration & Legacy Replacement
- [ ] Task: LangGraph 워크플로우를 기존 Django View/Action에 통합
- [ ] Task: 대화 세션 관리 로직 업데이트 (LangGraph 상태 유지 대응)
- [ ] Task: 기존 시스템 프롬프트 기반 로직의 완전한 제거 및 검증
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Django Integration & Legacy Replacement' (Protocol in workflow.md)

## Phase 5: Final Verification & Refinement
- [ ] Task: 전체 인콰이어리 흐름에 대한 통합 테스트 및 커버리지 체크 (>80%)
- [ ] Task: 예외 상황(LLM 출력 오류 등) 처리 및 성능 최적화
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Verification & Refinement' (Protocol in workflow.md)
