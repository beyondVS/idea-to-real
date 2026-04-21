# Specification: Inquiry Engine Simplification (simplify_inquiry_20260421)

## 1. 개요 (Overview)
Inquiry Engine의 복잡도를 낮추고 효율적인 질문 프로세스를 구축하기 위해 CritiqueAgent를 제거하고 InquiryAgent의 질문 전략을 간소화합니다.

## 2. 기능 요구사항 (Functional Requirements)
- **CritiqueAgent 삭제**: 시스템 내 논리 검증을 담당하던 CritiqueAgent를 완전히 제거합니다.
- **InquiryAgent 프롬프트 수정**: 
    - `SYSTEM_PROMPT`에서 소크라테스식 질문법 관련 내용을 삭제합니다.
    - '간결한 5 Whys' 전략을 채택하여 핵심적인 근본 원인 파악에 집중하도록 수정합니다.
- **워크플로우(LangGraph) 개편**:
    - Critique 노드 및 관련 엣지를 Graph 정의에서 제거합니다.
    - InquiryAgent의 결과가 검증 단계 없이 다음 단계(예: 요약 또는 종료)로 직접 전달되도록 구조를 변경합니다.
- **코드 정리**: `agents/critique.py` 등 더 이상 사용되지 않는 파일과 관련 테스트 코드를 삭제하거나 수정합니다.

## 3. 비기능 요구사항 (Non-Functional Requirements)
- **성능**: 검증 단계 제거로 인한 전체 응답 시간 단축.
- **안정성**: 기존의 에러 핸들링 및 LLM 프로바이더 연동 구조는 유지함.

## 4. 수락 기준 (Acceptance Criteria)
- `CritiqueAgent` 관련 클래스 및 파일이 삭제되었는가?
- `InquiryAgent`의 질문 방식이 소크라테스식에서 '간결한 5 Whys'로 변경되었는가?
- LangGraph 실행 시 Critique 단계를 거치지 않고 정상적으로 종료되는가?
- 관련된 기존 테스트가 새로운 구조에 맞게 통과하거나 적절히 수정되었는가?

## 5. 범위 외 (Out of Scope)
- 새로운 에이전트 추가.
- UI/UX의 대대적인 변경.
