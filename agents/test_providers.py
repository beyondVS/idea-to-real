import unittest
from unittest.mock import MagicMock, patch
from agents.base import BaseLLMProvider, BaseAgent, GeminiProvider, OpenAIProvider, AnthropicProvider, ProviderFactory

class MockProvider(BaseLLMProvider):
    """테스트를 위한 모의 LLM 프로바이더 클래스입니다."""

    def generate_response(self, messages, **kwargs):
        """모의 응답을 생성합니다.

        Args:
            messages: 메시지 리스트입니다.
            **kwargs: 추가 설정 인자입니다.

        Returns:
            "Mock Response" 문자열을 반환합니다.
        """
        return "Mock Response"

    def handle_tool_call(self, tool_call):
        """모의 도구 호출을 처리합니다.

        Args:
            tool_call: 도구 호출 정보입니다.

        Returns:
            "Tool Result" 문자열을 반환합니다.
        """
        return "Tool Result"

class TestLLMProviders(unittest.TestCase):
    """LLM 프로바이더 및 에이전트 연동 기능을 테스트하는 클래스입니다."""

    def test_base_provider_is_abstract(self):
        """BaseLLMProvider가 추상 클래스이며 직접 인스턴스화할 수 없는지 테스트합니다."""
        with self.assertRaises(TypeError):
            BaseLLMProvider()

    def test_base_agent_uses_provider(self):
        """BaseAgent가 주입된 프로바이더를 사용하여 응답을 생성하는지 테스트합니다."""
        mock_provider = MagicMock(spec=BaseLLMProvider)
        mock_provider.generate_response.return_value = "Agent Response"
        
        agent = BaseAgent(provider=mock_provider)
        messages = [{"role": "user", "content": "Hello"}]
        response = agent.get_response(messages)
        
        self.assertEqual(response, "Agent Response")
        mock_provider.generate_response.assert_called_once_with(messages)

    @patch('google.genai.Client')
    def test_gemini_provider(self, mock_client_class):
        """GeminiProvider가 올바른 모델과 API 호출을 수행하는지 테스트합니다."""
        mock_client = mock_client_class.return_value
        mock_client.models.generate_content.return_value = MagicMock(text="Gemini Response")
        
        provider = GeminiProvider(api_key="test_key")
        self.assertEqual(provider.model, "gemini-2.5-flash-lite")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "Gemini Response")

    @patch('openai.resources.chat.Completions.create')
    def test_openai_provider(self, mock_create):
        """OpenAIProvider가 올바른 API 호출을 수행하는지 테스트합니다."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="OpenAI Response"))]
        mock_create.return_value = mock_response
        
        provider = OpenAIProvider(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "OpenAI Response")

    @patch('anthropic.resources.messages.Messages.create')
    def test_anthropic_provider(self, mock_create):
        """AnthropicProvider가 올바른 API 호출을 수행하는지 테스트합니다."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Anthropic Response")]
        mock_create.return_value = mock_response
        
        provider = AnthropicProvider(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "Anthropic Response")

    def test_provider_factory(self):
        """ProviderFactory가 설정에 따라 올바른 프로바이더를 생성하는지 테스트합니다."""
        # Default case
        factory = ProviderFactory()
        provider = factory.get_provider("InquiryAgent")
        self.assertIsInstance(provider, GeminiProvider)

        # Environment override case
        with patch.dict('os.environ', {'AGENT_INQUIRYAGENT_MODEL': 'openai'}):
            provider = factory.get_provider("InquiryAgent")
            self.assertIsInstance(provider, OpenAIProvider)

        with patch.dict('os.environ', {'AGENT_CRITIQUEAGENT_MODEL': 'anthropic'}):
            provider = factory.get_provider("CritiqueAgent")
            self.assertIsInstance(provider, AnthropicProvider)

    def test_base_agent_auto_provider(self):
        """BaseAgent가 클래스 이름을 기반으로 프로바이더를 자동으로 선택하는지 테스트합니다."""
        # By default, BaseAgent should use factory based on its class name
        with patch.dict('os.environ', {'AGENT_BASEAGENT_MODEL': 'openai'}):
            agent = BaseAgent()
            self.assertIsInstance(agent.provider, OpenAIProvider)

    def test_agent_tool_call(self):
        """에이전트가 도구 호출을 프로바이더에게 올바르게 전달하는지 테스트합니다."""
        mock_provider = MagicMock(spec=BaseLLMProvider)
        mock_provider.handle_tool_call.return_value = "Tool Result"
        agent = BaseAgent(provider=mock_provider)
        result = agent.handle_tool_call({"name": "test_tool"})
        self.assertEqual(result, "Tool Result")

    @patch('google.genai.Client')
    def test_gemini_system_prompt(self, mock_client_class):
        """GeminiProvider가 시스템 프롬프트를 올바르게 처리하는지 테스트합니다."""
        mock_client = mock_client_class.return_value
        provider = GeminiProvider(api_key="test_key")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        provider.generate_response(messages)
        
        # Verify system prompt is handled in config
        call_args = mock_client.models.generate_content.call_args
        config = call_args.kwargs['config']
        self.assertEqual(config['system_instruction'], "You are a helpful assistant.")
        contents = call_args.kwargs['contents']
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0]['parts'][0]['text'], "Hello")

    @patch('anthropic.resources.messages.Messages.create')
    def test_anthropic_system_prompt(self, mock_create):
        """AnthropicProvider가 시스템 프롬프트를 올바르게 처리하는지 테스트합니다."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Anthropic Response")]
        mock_create.return_value = mock_response
        
        provider = AnthropicProvider(api_key="test_key")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        provider.generate_response(messages)
        
        # Verify system prompt is passed as 'system' argument to Anthropic API
        call_args = mock_create.call_args
        self.assertEqual(call_args.kwargs['system'], "You are a helpful assistant.")
        self.assertEqual(len(call_args.kwargs['messages']), 1)

if __name__ == '__main__':
    unittest.main()
