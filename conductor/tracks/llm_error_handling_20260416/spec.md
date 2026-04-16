# Specification: LLM Error Handling & Retry Logic

## Overview
외부 LLM(Gemini, OpenAI, Anthropic 등) 호출 과정에서 발생하는 다양한 에러를 체계적으로 관리하고, 일시적인 에러에 대해서는 지수 백오프(Exponential Backoff)를 적용한 재시도 로직을 구현합니다. 재시도 후에도 해결되지 않거나 재시도가 불가능한 에러의 경우 사용자에게 구체적이고 명확한 안내 메시지를 제공하여 시스템의 신뢰성과 사용성을 높입니다.

## Functional Requirements
- **Error Classification:** 발생한 에러를 재시도 가능(Transient) 에러와 재시도 불가능(Permanent) 에러로 분류합니다.
  - 재시도 가능: Rate Limits (429), Timeouts, Server Errors (5xx).
  - 재시도 불가능: Auth Errors (401), Invalid Parameters (400), Quota Exhausted (일부 경우).
- **Retry Logic:**
  - 지수 백오프(Exponential Backoff) 전략을 사용하여 최대 3회 재시도합니다.
  - 각 재시도 사이의 대기 시간은 점진적으로 증가합니다.
- **User Notification:**
  - 최종적으로 실패한 경우, 에러의 종류에 맞는 구체적인 메시지를 사용자에게 표시합니다.
  - 예: "현재 서비스 이용량이 많아 잠시 후 다시 시도해 주세요 (Rate Limit)", "인증 정보에 문제가 발생했습니다. 관리자에게 문의하세요 (Auth Error)".
- **Logging:** 모든 에러 발생 및 재시도 내역을 로깅하여 추후 분석이 가능하도록 합니다.

## Non-Functional Requirements
- **Performance:** 재시도 로직이 전체 시스템의 응답 속도에 미치는 영향을 최소화해야 합니다.
- **Reliability:** 에러 발생 시에도 시스템이 비정상 종료되지 않고 안전하게 예외를 처리해야 합니다.

## Acceptance Criteria
- [ ] Rate Limit(429) 발생 시 지수 백오프를 통해 최대 3회 재시도하고 성공하는지 확인.
- [ ] Timeout 발생 시 재시도 로직이 정상 작동하는지 확인.
- [ ] Auth Error(401) 발생 시 재시도 없이 즉시 적절한 에러 메시지가 표시되는지 확인.
- [ ] 3회 재시도 후에도 실패할 경우 사용자에게 구체적인 에러 안내가 제공되는지 확인.

## Out of Scope
- LLM 서비스 자체의 가용성 보장 (외부 인프라 영역).
- 특정 언어 이외의 다국어 에러 메시지 지원 (현재는 한국어 우선).