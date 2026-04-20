# Track Specification: Add Ollama Provider for Local Development

## 1. Overview
개발 환경에서 비용 절감 및 데이터 보안을 위해 로컬에 설치된 AI 모델(Ollama)을 사용할 수 있도록 새로운 프로바이더를 추가합니다. 기존 `Multi-Agent Packaging` 추상 인터페이스를 확장하여 다른 LLM 제공자(Gemini, OpenAI 등)와 동일한 방식으로 투명하게 교체하여 사용할 수 있도록 구현합니다.

## 2. Functional Requirements
- **Ollama Provider Implementation:** `agents/` 폴더 내의 추상 프로바이더 클래스를 상속하여 `OllamaProvider`를 구현합니다.
- **Model Configuration via Environment:** `.env` 파일을 통해 사용할 모델명을 지정할 수 있어야 하며, 기본값으로 `gemma4:e4b`를 사용합니다.
- **Connection Settings:**
    - `OLLAMA_BASE_URL`: Ollama 서버 주소 (기본값: http://localhost:11434)
    - `OLLAMA_TIMEOUT`: 요청 타임아웃 설정
    - `OLLAMA_PARAMETERS`: Temperature, Top-p 등 LLM 생성 매개변수 지원
- **Error Handling:**
    - Ollama 서비스가 로컬에서 실행 중이지 않거나 연결할 수 없는 경우, 사용자에게 명확한 안내 메시지(예: "Ollama가 실행 중인지 확인하세요.")를 제공하고 프로세스를 종료합니다.
- **Compatibility:** 기존 LangGraph 기반 Inquiry Engine의 Analyzer, Questioner, Empathizer 노드에서 Ollama 프로바이더를 문제없이 사용할 수 있어야 합니다.

## 3. Non-Functional Requirements
- **Performance:** 로컬 환경의 자원을 사용하므로 응답 속도가 모델 크기에 따라 달라질 수 있음을 고려합니다.
- **Security:** 모든 데이터는 로컬 네트워크 내에서만 처리되어야 합니다.

## 4. Acceptance Criteria
- [ ] `OllamaProvider` 클래스가 기존 추상 인터페이스를 올바르게 구현함.
- [ ] `.env` 설정을 통해 Ollama 모델을 로딩하고 테스트 메시지를 정상적으로 주고받을 수 있음.
- [ ] Ollama 서비스 중단 시 적절한 에러 메시지가 출력됨을 확인.
- [ ] 기존 Inquiry Engine의 워크플로우가 Ollama 기반으로 정상 작동함.

## 5. Out of Scope
- Ollama 서버 자체의 자동 설치 또는 관리 기능.
- 특정 하드웨어 가속(GPU) 최적화 설정 (Ollama 기본 설정에 의존).
