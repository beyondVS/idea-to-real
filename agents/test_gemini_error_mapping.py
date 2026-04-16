import pytest
from unittest.mock import MagicMock, patch
from google.genai import errors
from agents.base import GeminiProvider
from agents.exceptions import LLMTransientError, LLMPermanentError

@pytest.fixture
def gemini_provider():
    return GeminiProvider(api_key="test_key")

def test_gemini_api_error_mapping(gemini_provider):
    """APIError가 발생했을 때 code에 따라 올바르게 매핑되는지 확인합니다."""
    with patch.object(gemini_provider.client.models, 'generate_content') as mock_generate:
        # Rate Limit (429) 시뮬레이션
        mock_error = errors.APIError(code=429, response_json={"message": "Rate limit exceeded"})
        mock_generate.side_effect = mock_error
        
        with pytest.raises(LLMTransientError):
            gemini_provider.generate_response([{"role": "user", "content": "hello"}])

        # Unauthorized (401) 시뮬레이션
        mock_error = errors.APIError(code=401, response_json={"message": "Invalid API key"})
        mock_generate.side_effect = mock_error
        
        with pytest.raises(LLMPermanentError):
            gemini_provider.generate_response([{"role": "user", "content": "hello"}])
