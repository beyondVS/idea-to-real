import json
from .base import BaseAgent

class SummarizeAgent(BaseAgent):
    """대화 내용을 분석하여 구조화된 문제 기술서(JSON)를 생성하는 요약 에이전트입니다.

    Attributes:
        SYSTEM_PROMPT: 구조화된 요약을 생성하기 위한 시스템 프롬프트입니다.
    """
    SYSTEM_PROMPT = """
당신은 대화 내용을 요약하여 구조화된 문제 기술서(Problem Specification)를 생성하는 AI 요약 에이전트입니다.
제공된 대화 내역을 분석하여 JSON 형식으로 구조화된 요약을 생성해야 합니다.
반드시 아래의 키를 포함하는 JSON만 출력하십시오. Markdown 포맷(```json 등)은 제외하고 순수 JSON 문자열만 반환하세요.

필수 JSON 구조:
{
    "problem_statement": "문제의 핵심 요약",
    "target_users": "예상되는 타겟 사용자 또는 대상",
    "core_features": ["핵심 기능 1", "핵심 기능 2"],
    "constraints": ["제약 조건 1", "제약 조건 2"],
    "success_criteria": "성공/목표 달성 기준"
}
"""

    def summarize(self, chat_history):
        """대화 기록을 분석하여 구조화된 JSON 요약본을 반환합니다.

        Args:
            chat_history: Django 모델의 Message 객체 리스트 또는 딕셔너리 리스트입니다.

        Returns:
            구조화된 데이터가 담긴 딕셔너리입니다. 파싱 실패 시 에러 메시지를 포함한 기본 딕셔너리를 반환합니다.
        """
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        for msg in chat_history:
            # msg could be a dict (in test) or a Model object (in real use)
            if isinstance(msg, dict):
                sender = msg.get('sender')
                content = msg.get('content')
            else:
                sender = getattr(msg, 'sender', '')
                content = getattr(msg, 'content', '')

            role = "user" if sender == "user" else "assistant"
            messages.append({"role": role, "content": content})

        raw_response = self.get_response(messages)

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            # Fallback for LLM returning markdown
            cleaned = raw_response.strip().removeprefix('```json').removesuffix('```').strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {
                    "problem_statement": "Failed to parse JSON summary.",
                    "target_users": "",
                    "core_features": [],
                    "constraints": [],
                    "success_criteria": ""
                }
