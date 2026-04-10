from .base import BaseAgent

class InquiryAgent(BaseAgent):
    """사용자에게 질문을 던져 아이디어를 구체화하는 소크라테스식 질문 엔진입니다.

    Attributes:
        SYSTEM_PROMPT: 소크라테스식 질문을 위한 시스템 프롬프트입니다.
    """
    SYSTEM_PROMPT = """
당신은 'Problem Specification AI System'의 핵심 엔진인 'Socratic Inquiry Agent'입니다.
당신의 목표는 사용자의 간략한 아이디어나 직면한 문제를 구조화된 문제 기술서로 발전시키기 위해 질문을 던지는 것입니다.

[작동 원리]
1. 5 Whys 기법을 활용하여 문제의 근본 원인(Root Cause)을 파악하십시오.
2. 소크라테스식 질문법을 사용하여 사용자가 자신의 생각에 숨겨진 전제를 발견하게 하십시오.
3. 한 번에 하나씩만 질문하십시오. 너무 많은 질문은 사용자를 지치게 합니다.
4. 사용자의 답변을 경청하고, 공감한 뒤, 논리적 비약이 있는 부분을 파고드십시오.
5. 친절하고 전문적인 한국어 말투를 사용하십시오.

[출력 형식]
사용자의 답변에 대한 분석을 간단히 언급한 후, 다음 단계로 나아가기 위한 날카로운 질문을 하나 던지십시오.
"""

    def generate_question(self, chat_history):
        """채팅 기록을 바탕으로 다음 소크라테스식 질문을 생성합니다.

        Args:
            chat_history: Django 모델의 Message 객체 리스트 또는 딕셔너리 리스트입니다.

        Returns:
            AI가 생성한 질문 문자열입니다.
        """
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

        # 이전 대화 내용을 OpenAI 메시지 형식으로 변환
        for msg in chat_history:
            role = "user" if msg.sender == "user" else "assistant"
            messages.append({"role": role, "content": msg.content})

        return self.get_response(messages)
