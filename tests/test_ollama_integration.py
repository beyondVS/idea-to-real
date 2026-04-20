import unittest
from unittest.mock import patch, MagicMock
import os
import ollama
import requests
from agents.base import ProviderFactory, OllamaProvider
from agents.inquiry import InquiryAgent
from agents.exceptions import LLMTransientError

class TestOllamaIntegration(unittest.TestCase):
    """Ollama 프로바이더의 시스템 통합 및 에러 처리를 테스트합니다."""

    def test_factory_creates_ollama_provider(self):
        """환경 변수 설정 시 ProviderFactory가 OllamaProvider를 생성하는지 확인합니다."""
        factory = ProviderFactory()
        with patch.dict('os.environ', {'AGENT_INQUIRYAGENT_MODEL': 'ollama'}):
            provider = factory.get_provider("InquiryAgent")
            self.assertIsInstance(provider, OllamaProvider)

    @patch('ollama.Client.chat')
    def test_inquiry_agent_with_ollama(self, mock_chat):
        """InquiryAgent가 OllamaProvider를 사용하여 정상적으로 작동하는지 확인합니다."""
        mock_chat.return_value = {
            'message': {
                'content': '{"logical_error_detected": false, "extracted_metadata": {"goal": "test"}, "root_cause_identified": false}'
            }
        }
        
        with patch.dict('os.environ', {'AGENT_INQUIRYAGENT_MODEL': 'ollama'}):
            agent = InquiryAgent()
            self.assertIsInstance(agent.provider, OllamaProvider)
            
            messages = [{"role": "user", "content": "Hello"}]
            response = agent.get_response(messages)
            self.assertIn("logical_error_detected", response)

    @patch('ollama.Client.chat')
    def test_ollama_connection_error_mapping(self, mock_chat):
        """Ollama 연결 실패 시 LLMTransientError로 올바르게 매핑되는지 확인합니다."""
        # 실제 연결 오류 상황 모사
        mock_chat.side_effect = requests.exceptions.ConnectionError("Failed to connect to Ollama")
        
        provider = OllamaProvider()
        with self.assertRaises(LLMTransientError):
            provider.generate_response([{"role": "user", "content": "Hello"}])

if __name__ == "__main__":
    unittest.main()
