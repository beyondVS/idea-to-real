import unittest
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestQuestionerNode(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    def test_questioner_updates_state(self):
        """Test that the questioner node generates a question and increments step count."""
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to build a house."}],
            "step_count": 0,
            "extracted_metadata": {"persona": "Home builder"},
            "logical_error_detected": False
        }
        
        # This method doesn't exist yet (Red Phase)
        new_state = self.agent.generate_next_question(initial_state)
        
        self.assertEqual(new_state["step_count"], 1)
        # Check if history is updated (system prompt not included in history, only dialog)
        self.assertTrue(len(new_state["history"]) > 1)
        self.assertEqual(new_state["history"][-1]["role"], "assistant")
        self.assertIsInstance(new_state["history"][-1]["content"], str)

if __name__ == "__main__":
    unittest.main()
