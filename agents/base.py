import os
from openai import OpenAI
from django.conf import settings

class BaseAgent:
    """기본 AI 에이전트 클래스입니다. OpenAI API와의 통신을 담당합니다.

    Attributes:
        client: OpenAI API 클라이언트 인스턴스입니다.
        model: 에이전트가 사용할 모델 이름입니다.
    """

    def __init__(self, model="gpt-4o"):
        """BaseAgent를 초기화합니다.

        Args:
            model: 사용할 OpenAI 모델의 이름입니다 (기본값: "gpt-4o").
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model

    def get_response(self, messages, **kwargs):
        """OpenAI API를 통해 응답을 생성합니다.

        Args:
            messages: OpenAI API 형식의 메시지 리스트입니다.
            **kwargs: OpenAI API에 전달할 추가 키워드 인자입니다.

        Returns:
            에이전트가 생성한 응답 텍스트입니다.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

