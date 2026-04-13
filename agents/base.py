import os
from abc import ABC, abstractmethod
from django.conf import settings
from openai import OpenAI
from google import genai
from anthropic import Anthropic

class BaseLLMProvider(ABC):
    """모든 LLM 프로바이더의 추상 베이스 클래스입니다."""

    @abstractmethod
    def generate_response(self, messages, **kwargs):
        """LLM을 통해 응답을 생성합니다.

        Args:
            messages: 메시지 리스트입니다.
            **kwargs: 추가 설정 인자입니다.
        """
        pass

    @abstractmethod
    def handle_tool_call(self, tool_call):
        """도구 호출을 처리합니다.

        Args:
            tool_call: 도구 호출 정보입니다.
        """
        pass

class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="gemini-2.5-flash-lite"):
        self.api_key = api_key or getattr(settings, 'GEMINI_API_KEY', '')
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def generate_response(self, messages, **kwargs):
        # google-genai는 content 형식을 사용함. 간단한 변환 시도.
        # 실제 구현에서는 더 정교한 변환이 필요할 수 있음.
        contents = []
        for msg in messages:
            role = "user" if msg['role'] == "user" else "model"
            if msg['role'] == "system":
                # Gemini 2.0 SDK에서는 system_instruction을 따로 받기도 하지만 
                # 여기서는 단순화를 위해 처리
                role = "user" # 시스템 프롬프트 처리는 SDK 버전에 따라 다름
            contents.append({"role": role, "parts": [{"text": msg['content']}]})
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            **kwargs
        )
        return response.text

    def handle_tool_call(self, tool_call):
        # TODO: Implement tool call handling for Gemini
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or getattr(settings, 'OPENAI_API_KEY', '')
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_response(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def handle_tool_call(self, tool_call):
        # TODO: Implement tool call handling for OpenAI
        pass

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="claude-3-5-sonnet-20240620"):
        self.api_key = api_key or getattr(settings, 'ANTHROPIC_API_KEY', '')
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    def generate_response(self, messages, **kwargs):
        # Anthropic은 system prompt를 별도 인자로 받음
        system_prompt = next((m['content'] for m in messages if m['role'] == 'system'), "")
        filtered_messages = [m for m in messages if m['role'] != 'system']
        
        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=filtered_messages,
            max_tokens=kwargs.get('max_tokens', 1024),
            **{k: v for k, v in kwargs.items() if k != 'max_tokens'}
        )
        return response.content[0].text

    def handle_tool_call(self, tool_call):
        # TODO: Implement tool call handling for Anthropic
        pass

class ProviderFactory:
    """에이전트 이름과 설정을 바탕으로 적절한 LLM 프로바이더를 생성하는 팩토리 클래스입니다."""

    def get_provider(self, agent_name):
        """에이전트 전용 모델 설정을 확인하여 프로바이더를 반환합니다.

        설정 우선순위:
        1. 환경 변수: AGENT_<AGENT_NAME>_MODEL (예: AGENT_INQUIRYAGENT_MODEL=openai)
        2. 기본값: GeminiProvider
        """
        env_key = f"AGENT_{agent_name.upper()}_MODEL"
        model_type = os.environ.get(env_key, "gemini").lower()

        if model_type == "openai":
            return OpenAIProvider()
        elif model_type == "anthropic":
            return AnthropicProvider()
        else:
            return GeminiProvider()

class BaseAgent:
    """기본 AI 에이전트 클래스입니다. 할당된 LLM 프로바이더를 통해 통신을 담당합니다.

    Attributes:
        provider: 에이전트가 사용할 LLM 프로바이더 인스턴스입니다.
    """

    def __init__(self, provider=None):
        """BaseAgent를 초기화합니다.

        Args:
            provider: 사용할 LLM 프로바이더 인스턴스입니다. 제공되지 않으면 GeminiProvider가 기본값입니다.
        """
        self.provider = provider or GeminiProvider()

    def get_response(self, messages, **kwargs):
        """할당된 프로바이더를 통해 응답을 생성합니다.

        Args:
            messages: 메시지 리스트입니다.
            **kwargs: 추가 키워드 인자입니다.

        Returns:
            에이전트가 생성한 응답 텍스트입니다.
        """
        return self.provider.generate_response(messages, **kwargs)
