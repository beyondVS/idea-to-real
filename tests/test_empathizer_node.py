import unittest
from unittest.mock import patch, MagicMock
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestEmpathizerNode(unittest.TestCase):
    def setUp(self):
        # Mock provider to avoid Django settings error during initialization
        self.agent = InquiryAgent(provider=MagicMock())

    @patch('agents.base.BaseAgent.get_response')
    def test_empathizer_refines_question(self, mock_get_response):
        """Test that the empathizer node refines the assistant's last response."""
        # Mocking the refined question from LLM
        mock_get_response.return_value = "집을 짓고 싶으시군요! 정말 멋진 생각입니다. 그런데 어떤 스타일의 집을 생각하고 계신가요?"

        initial_state: InquiryGraphState = {
            "history": [
                {"role": "user", "content": "I want to build a house."},
                {"role": "assistant", "content": "Why?"}
            ],
            "step_count": 1,
            "extracted_metadata": {"persona": "Home builder"},
            "logical_error_detected": False
        }
        
        new_state = self.agent.apply_empathy(initial_state)
        
        # History length should be the same, but content should be refined
        self.assertEqual(len(new_state["history"]), 2)
        self.assertEqual(new_state["history"][-1]["role"], "assistant")
        self.assertNotEqual(new_state["history"][-1]["content"], "Why?")
        # Should be in Korean and polite
        self.assertIsInstance(new_state["history"][-1]["content"], str)
        self.assertIn("집을 짓고 싶으시군요", new_state["history"][-1]["content"])

if __name__ == "__main__":
    unittest.main()
