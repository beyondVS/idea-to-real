# Inquiry Engine transition to LangGraph (spec.md)

## 1. Overview
현재 단일 시스템 프롬프트로 운영 중인 Inquiry Engine을 LangGraph 기반의 상태 머신(State Machine) 워크플로우로 전환합니다. 이를 통해 대화의 흐름을 정교하게 제어하고, 각 단계(Analyzer, Questioner, Empathizer)를 모듈화하여 논리적 완결성이 높은 문제 기술서를 생성할 수 있도록 합니다.

## 2. Functional Requirements
- **GraphState 정의:** 다음 필드를 포함하는 `GraphState` 클래스를 정의합니다.
  - `history`: 대화 이력 (리스트)
  - `step_count`: 현재 5 Whys 단계 (1~5)
  - `extracted_metadata`: 추출된 페르소나 및 숨겨진 전제 (딕셔너리)
  - `logical_error_detected`: 논리적 비약이나 모순 발견 여부 (불리언)
- **노드(Node) 구현:**
  - **Analyzer:** 사용자 답변의 논리적 비약과 숨겨진 전제를 분석하고 `extracted_metadata`를 업데이트합니다.
  - **Questioner:** `step_count`와 분석 결과에 따라 5 Whys 또는 소크라테스식 질문을 생성합니다. (1문 1답 원칙 준수)
  - **Empathizer:** 모든 생성된 질문에 공감과 전문적인 한국어 톤앤매너를 적용하여 최종 출력을 다듬습니다.
- **엣지(Edge) 로직:**
  - Analyzer가 근본 원인이 파악되었다고 판단하거나 사용자가 명시적으로 종료를 요청할 경우 대화를 종료합니다.
  - 그렇지 않은 경우 다음 질문 노드로 분기하여 순환 구조를 유지합니다.
- **시스템 프롬프트 분해:** 기존 프롬프트의 5대 원칙(공감, 1문 1답, 전문성 등)을 각 노드의 전용 시스템 프롬프트로 재배치합니다.
- **Django 통합:** Django 백엔드 내에서 LangGraph 워크플로우를 호출하고 대화 상태를 지속적으로 관리할 수 있도록 통합합니다.

## 3. Non-Functional Requirements
- **비동기 처리:** Django의 비동기 기능을 활용하여 LangGraph 노드 실행 중 블로킹을 최소화합니다.
- **테스트 가능성:** 각 노드(Analyzer, Questioner 등)를 독립적으로 검증할 수 있는 단위 테스트를 작성합니다.
- **유지보수성:** 워크플로우 시각화 및 디버깅이 용이하도록 상태 추적을 명확히 합니다.

## 4. Acceptance Criteria
- LangGraph 워크플로우가 기존의 단일 프롬프트 방식 로직을 완전히 대체합니다.
- 정의된 3개 노드(Analyzer, Questioner, Empathizer)가 정상적으로 협업하여 질문을 생성합니다.
- 대화 종료 조건(논리적 완결 또는 사용자 요청)에 따라 워크플로우가 정확히 종료됩니다.
- 새로운 코드에 대해 80% 이상의 테스트 커버리지를 달성합니다.

## 5. Out of Scope
- UI/UX 디자인 전면 개편 (기존 Django 템플릿 유지).
- 다중 에이전트 간의 비판(Critique) 기능 (추후 트랙에서 구현).
