import os
import logging
from abc import ABC, abstractmethod
from django.conf import settings
from openai import OpenAI
from google import genai
from anthropic import Anthropic

import openai
import anthropic
import ollama
import requests

from google.genai import errors as genai_errors
from agents.exceptions import LLMBaseError, LLMTransientError, LLMPermanentError
from agents.utils import retry_with_backoff

logger = logging.getLogger(__name__)

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

    def _map_error(self, e):
        """프로바이더 전용 에러를 공통 에러로 매핑합니다."""
        # Gemini (google-genai)
        if isinstance(e, genai_errors.APIError):
            if e.code in [429, 500, 503, 504]:
                return LLMTransientError(str(e), original_error=e)
            else:
                return LLMPermanentError(str(e), original_error=e)
        
        # OpenAI
        if isinstance(e, (openai.RateLimitError, openai.APITimeoutError, openai.InternalServerError)):
            return LLMTransientError(str(e), original_error=e)
        if isinstance(e, (openai.AuthenticationError, openai.BadRequestError)):
            return LLMPermanentError(str(e), original_error=e)
        if isinstance(e, openai.OpenAIError):
            return LLMBaseError(str(e), original_error=e)

        # Anthropic
        if isinstance(e, (anthropic.RateLimitError, anthropic.APITimeoutError, anthropic.InternalServerError)):
            return LLMTransientError(str(e), original_error=e)
        if isinstance(e, (anthropic.AuthenticationError, anthropic.BadRequestError)):
            return LLMPermanentError(str(e), original_error=e)
        if isinstance(e, anthropic.AnthropicError):
            return LLMBaseError(str(e), original_error=e)

        # Ollama
        if isinstance(e, requests.exceptions.RequestException):
            return LLMTransientError(str(e), original_error=e)
        if hasattr(ollama, 'ResponseError') and isinstance(e, ollama.ResponseError):
            if e.status_code in [429, 500, 503, 504]:
                return LLMTransientError(str(e), original_error=e)
            return LLMPermanentError(str(e), original_error=e)

        return e

class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="gemini-2.5-flash-lite"):
        self.api_key = api_key or getattr(settings, 'GEMINI_API_KEY', '')
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    @retry_with_backoff(max_retries=3)
    def generate_response(self, messages, **kwargs):
        # google-genai는 system_instruction과 contents를 분리하여 처리함
        system_instruction = next((m['content'] for m in messages if m['role'] == 'system'), None)
        
        contents = []
        for msg in messages:
            if msg['role'] == "system":
                continue
            role = "user" if msg['role'] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg['content']}]})
        
        config = {}
        if system_instruction:
            config['system_instruction'] = system_instruction
        
        # kwargs에 있는 설정들 (max_output_tokens 등) 통합
        if kwargs:
            config.update(kwargs)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config if config else None
            )
            return response.text
        except Exception as e:
            raise self._map_error(e)

    def handle_tool_call(self, tool_call):
        # TODO(callo): Implement tool call handling
        pass

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or getattr(settings, 'OPENAI_API_KEY', '')
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    @retry_with_backoff(max_retries=3)
    def generate_response(self, messages, **kwargs):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise self._map_error(e)

    def handle_tool_call(self, tool_call):
        # TODO(callo): Implement tool call handling
        pass

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM 프로바이더입니다."""

    def __init__(self, api_key=None, model="claude-3-5-sonnet-20240620"):
        self.api_key = api_key or getattr(settings, 'ANTHROPIC_API_KEY', '')
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

    @retry_with_backoff(max_retries=3)
    def generate_response(self, messages, **kwargs):
        # Anthropic은 system prompt를 별도 인자로 받음
        system_prompt = next((m['content'] for m in messages if m['role'] == 'system'), "")
        filtered_messages = [m for m in messages if m['role'] != 'system']
        
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=filtered_messages,
                max_tokens=kwargs.get('max_tokens', 1024),
                **{k: v for k, v in kwargs.items() if k != 'max_tokens'}
            )
            return response.content[0].text
        except Exception as e:
            raise self._map_error(e)

    def handle_tool_call(self, tool_call):
        # TODO(callo): Implement tool call handling
        pass

class OllamaProvider(BaseLLMProvider):
    """Ollama 로컬 LLM 프로바이더입니다."""

    def __init__(self, model=None, base_url=None, timeout=None):
        self.model = model or getattr(settings, 'OLLAMA_MODEL', 'gemma4:e4b')
        self.base_url = base_url or getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.timeout = timeout or getattr(settings, 'OLLAMA_TIMEOUT', 60)
        self.client = ollama.Client(host=self.base_url)

    @retry_with_backoff(max_retries=3)
    def generate_response(self, messages, **kwargs):
        """Ollama API를 통해 응답을 생성합니다."""
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                options=kwargs
            )
            return response['message']['content']
        except Exception as e:
            raise self._map_error(e)

    def handle_tool_call(self, tool_call):
        """Ollama는 현재 도구 호출을 기본적으로 지원하지 않을 수 있으므로 패스합니다."""
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
        elif model_type == "ollama":
            return OllamaProvider()
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
            provider: 사용할 LLM 프로바이더 인스턴스입니다. 제공되지 않으면 ProviderFactory를 통해 생성합니다.
        """
        if provider:
            self.provider = provider
        else:
            factory = ProviderFactory()
            self.provider = factory.get_provider(self.__class__.__name__)

    def get_response(self, messages, **kwargs):
        """할당된 프로바이더를 통해 응답을 생성합니다.

        Args:
            messages: 메시지 리스트입니다.
            **kwargs: 추가 키워드 인자입니다.

        Returns:
            에이전트가 생성한 응답 텍스트입니다.
        """
        logger.info(f"Agent '{self.__class__.__name__}' using provider '{self.provider.__class__.__name__}' with model '{self.provider.model}'")
        return self.provider.generate_response(messages, **kwargs)

    def handle_tool_call(self, tool_call):
        """할당된 프로바이더를 통해 도구 호출을 처리합니다.

        Args:
            tool_call: 도구 호출 정보입니다.
        """
        return self.provider.handle_tool_call(tool_call)
