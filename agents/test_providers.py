import unittest
from unittest.mock import MagicMock, patch
from agents.base import BaseLLMProvider, BaseAgent, GeminiProvider, OpenAIProvider, AnthropicProvider

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

if __name__ == '__main__':
    unittest.main()
