import pytest
from unittest.mock import patch, MagicMock
from agents.base import GeminiProvider
from agents.exceptions import LLMTransientError

@pytest.fixture
def gemini_provider():
    return GeminiProvider(api_key="test_key")

def test_gemini_provider_retry_integration(gemini_provider):
    """GeminiProvider.generate_response에 재시도 로직이 통합되었는지 확인합니다."""
    with patch.object(gemini_provider.client.models, 'generate_content') as mock_generate:
        # 두 번 실패 후 세 번째 성공
        mock_generate.side_effect = [
            Exception("Transient 1"),  # _map_error에 의해 LLMTransientError로 변환될 것임
            Exception("Transient 2"),
            MagicMock(text="success")
        ]
        
        # _map_error를 직접 패치하여 LLMTransientError를 던지도록 함 (테스트 간소화)
        with patch.object(gemini_provider, '_map_error') as mock_map:
            mock_map.side_effect = lambda e: LLMTransientError(str(e))
            
            # base_delay를 매우 작게 설정할 수 없으므로, time.sleep을 패치함
            with patch('time.sleep', return_value=None):
                result = gemini_provider.generate_response([{"role": "user", "content": "hello"}])
                
        assert result == "success"
        assert mock_generate.call_count == 3
