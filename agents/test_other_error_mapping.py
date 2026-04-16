import pytest
from unittest.mock import patch
import openai
import anthropic
from agents.base import OpenAIProvider, AnthropicProvider
from agents.exceptions import LLMTransientError, LLMPermanentError

@pytest.fixture
def openai_provider():
    return OpenAIProvider(api_key="test_key")

@pytest.fixture
def anthropic_provider():
    return AnthropicProvider(api_key="test_key")

def test_openai_rate_limit_error_mapping(openai_provider):
    with patch.object(openai_provider.client.chat.completions, 'create') as mock_create:
        mock_create.side_effect = openai.RateLimitError(
            message="Rate limit reached",
            response=patch('httpx.Response').start(),
            body={}
        )
        with pytest.raises(LLMTransientError):
            openai_provider.generate_response([{"role": "user", "content": "hello"}])

def test_openai_auth_error_mapping(openai_provider):
    with patch.object(openai_provider.client.chat.completions, 'create') as mock_create:
        mock_create.side_effect = openai.AuthenticationError(
            message="Invalid key",
            response=patch('httpx.Response').start(),
            body={}
        )
        with pytest.raises(LLMPermanentError):
            openai_provider.generate_response([{"role": "user", "content": "hello"}])

def test_anthropic_rate_limit_error_mapping(anthropic_provider):
    with patch.object(anthropic_provider.client.messages, 'create') as mock_create:
        mock_create.side_effect = anthropic.RateLimitError(
            message="Rate limit reached",
            response=patch('httpx.Response').start(),
            body={}
        )
        with pytest.raises(LLMTransientError):
            anthropic_provider.generate_response([{"role": "user", "content": "hello"}])
