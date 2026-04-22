# Specification: Interactive Chat Feedback System

## Overview
사용자의 입력에 대해 AI가 처리하는 동안 실시간 피드백('답변 작성 중...')을 제공하고, 프로세스 완료 시 생성되는 '문제 기술서'를 시각적으로 강조하여 표시함으로써 채팅 UX를 개선합니다.

## Functional Requirements
1. **로딩 상태 표시 (Loading Indicator):**
   - 사용자가 메시지를 전송하면 채팅 내역 끝에 애니메이션이 포함된 '답변 작성 중...' 표시가 나타납니다.
   - AI 응답이 도착하여 화면에 표시되면 해당 로딩 표시는 제거됩니다.
2. **비동기 통신 (Asynchronous Interaction):**
   - Vanilla JavaScript의 Fetch API를 사용하여 페이지 새로고침 없이 메시지 전송 및 응답 수신을 처리합니다.
3. **최종 결과물 강조 (Final Result Display):**
   - 5 Whys 과정이 끝나고 생성된 '문제 기술서(Problem Specification)'는 일반 대화와 구분되도록 강조된 카드 스타일(Highlighted Card)로 채팅창에 표시됩니다.

## Non-Functional Requirements
- **반응성:** 메시지 전송 즉시 로딩 표시가 나타나야 합니다.
- **일관성:** 애니메이션과 카드 스타일은 프로젝트의 기존 UI/UX 가이드를 따릅니다.

## Acceptance Criteria
- 메시지 전송 시 로딩 애니메이션이 즉시 표시되는가?
- 응답 수신 시 로딩 애니메이션이 사라지고 응답 내용이 표시되는가?
- 최종 문제 기술서가 일반 메시지와 차별화된 디자인으로 출력되는가?
- 전체 과정에서 페이지 새로고침이 발생하지 않는가?

## Out of Scope
- 응답 텍스트의 실시간 스트리밍(Incremental Display).
- 채팅 내역의 클라이언트측 영구 저장(기존 세션/DB 저장 방식 유지).
