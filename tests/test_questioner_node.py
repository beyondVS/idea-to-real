import unittest
from unittest.mock import patch
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestQuestionerNode(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    @patch('agents.base.BaseAgent.get_response')
    def test_questioner_updates_state(self, mock_get_response):
        """Test that the questioner node generates a question and increments step count."""
        mock_get_response.return_value = "Why do you want to build a house?"
        
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to build a house."}],
            "step_count": 0,
            "extracted_metadata": {"persona": "Home builder"},
            "logical_error_detected": False
        }
        
        new_state = self.agent.generate_next_question(initial_state)
        
        self.assertEqual(new_state["step_count"], 1)
        self.assertTrue(len(new_state["history"]) > 1)
        self.assertEqual(new_state["history"][-1]["role"], "assistant")
        self.assertEqual(new_state["history"][-1]["content"], "Why do you want to build a house?")

if __name__ == "__main__":
    unittest.main()
