import unittest
from unittest.mock import MagicMock, patch
from agents.base import BaseLLMProvider, BaseAgent, GeminiProvider, OpenAIProvider, AnthropicProvider, ProviderFactory

class MockProvider(BaseLLMProvider):
    def generate_response(self, messages, **kwargs):
        return "Mock Response"

    def handle_tool_call(self, tool_call):
        return "Tool Result"

class TestLLMProviders(unittest.TestCase):
    def test_base_provider_is_abstract(self):
        with self.assertRaises(TypeError):
            BaseLLMProvider()

    def test_base_agent_uses_provider(self):
        mock_provider = MagicMock(spec=BaseLLMProvider)
        mock_provider.generate_response.return_value = "Agent Response"
        
        agent = BaseAgent(provider=mock_provider)
        messages = [{"role": "user", "content": "Hello"}]
        response = agent.get_response(messages)
        
        self.assertEqual(response, "Agent Response")
        mock_provider.generate_response.assert_called_once_with(messages)

    @patch('google.genai.Client')
    def test_gemini_provider(self, mock_client_class):
        mock_client = mock_client_class.return_value
        mock_client.models.generate_content.return_value = MagicMock(text="Gemini Response")
        
        provider = GeminiProvider(api_key="test_key")
        self.assertEqual(provider.model, "gemini-2.5-flash-lite")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "Gemini Response")

    @patch('openai.resources.chat.Completions.create')
    def test_openai_provider(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="OpenAI Response"))]
        mock_create.return_value = mock_response
        
        provider = OpenAIProvider(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "OpenAI Response")

    @patch('anthropic.resources.messages.Messages.create')
    def test_anthropic_provider(self, mock_create):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Anthropic Response")]
        mock_create.return_value = mock_response
        
        provider = AnthropicProvider(api_key="test_key")
        messages = [{"role": "user", "content": "Hello"}]
        response = provider.generate_response(messages)
        
        self.assertEqual(response, "Anthropic Response")

    def test_provider_factory(self):
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
        # By default, BaseAgent should use factory based on its class name
        with patch.dict('os.environ', {'AGENT_BASEAGENT_MODEL': 'openai'}):
            agent = BaseAgent()
            self.assertIsInstance(agent.provider, OpenAIProvider)

    def test_agent_tool_call(self):
        mock_provider = MagicMock(spec=BaseLLMProvider)
        mock_provider.handle_tool_call.return_value = "Tool Result"
        agent = BaseAgent(provider=mock_provider)
        result = agent.handle_tool_call({"name": "test_tool"})
        self.assertEqual(result, "Tool Result")

    @patch('google.genai.Client')
    def test_gemini_system_prompt(self, mock_client_class):
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
