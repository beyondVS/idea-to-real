import os
from openai import OpenAI
from django.conf import settings

class BaseAgent:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model

    def get_response(self, messages, **kwargs):
        """OpenAI API를 통해 응답을 생성합니다."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
