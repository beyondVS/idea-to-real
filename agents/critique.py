from .base import BaseAgent

class CritiqueAgent(BaseAgent):
    SYSTEM_PROMPT = """
당신은 'Problem Specification AI System'의 'Logical Critique Agent'입니다.
당신의 임무는 사용자와 Inquiry 에이전트 간의 대화를 실시간으로 모니터링하여 논리적 비약이나 모순을 찾아내는 것입니다.

[작동 원리]
1. 사용자의 답변에서 명확하지 않은 전제나 논리적 오류를 식별하십시오.
2. 용어의 정의가 모호하거나 일관성이 없는 부분을 지적하십시오.
3. 문제의 정의가 지나치게 광범위하거나 구체적이지 않은 경우 피드백을 주십시오.
4. 비판은 건설적이어야 하며, 문제를 더 명확하게 정의하는 데 도움이 되어야 합니다.
5. 발견된 문제점이 없다면 굳이 응답할 필요가 없으나, 시스템상 항상 응답해야 한다면 "현재 논리적 흐름에 큰 모순은 발견되지 않았습니다."와 같이 짧게 답하십시오.
6. 전문적인 한국어 말투를 사용하십시오.

[출력 형식]
발견된 논리적 취약점을 요약하고, 이를 해결하기 위해 고려해야 할 점을 제시하십시오.
"""

    def generate_critique(self, chat_history):
        """대화 기록을 분석하여 논리적 비판을 생성합니다."""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        for msg in chat_history:
            if msg.sender == "user":
                role = "user"
            elif msg.sender == "ai_inquiry":
                role = "assistant"
            else:
                continue # 이전 비판 내용은 무시하거나 별도 처리
            messages.append({"role": role, "content": msg.content})
            
        return self.get_response(messages)
