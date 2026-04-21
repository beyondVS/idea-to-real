import unittest
from unittest.mock import patch, MagicMock
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestQuestionerNode(unittest.TestCase):
    @patch('agents.base.ProviderFactory.get_provider')
    def setUp(self, mock_get_provider):
        # Django 설정을 참조하지 않도록 프로바이더를 미리 주입하거나 팩토리를 목 처리합니다.
        mock_provider = MagicMock()
        mock_provider.model = "test-model"
        mock_get_provider.return_value = mock_provider
        
        from agents.inquiry import InquiryAgent
        self.agent = InquiryAgent()

    @patch('agents.base.BaseAgent.get_response')
    def test_questioner_updates_state(self, mock_get_response):
        """Test that the questioner node generates a question and increments step count."""
        mock_get_response.return_value = "Why do you want to build a house?"
        
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to build a house."}],
            "step_count": 0,
            "extracted_metadata": {"persona": "Home builder"}
        }
        
        new_state = self.agent.generate_next_question(initial_state)
        
        self.assertEqual(new_state["step_count"], 1)
        self.assertTrue(len(new_state["history"]) > 1)
        self.assertEqual(new_state["history"][-1]["role"], "assistant")
        self.assertEqual(new_state["history"][-1]["content"], "Why do you want to build a house?")

if __name__ == "__main__":
    unittest.main()
