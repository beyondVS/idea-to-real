import unittest
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestEmpathizerNode(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    def test_empathizer_refines_question(self):
        """Test that the empathizer node refines the assistant's last response."""
        initial_state: InquiryGraphState = {
            "history": [
                {"role": "user", "content": "I want to build a house."},
                {"role": "assistant", "content": "Why?"}
            ],
            "step_count": 1,
            "extracted_metadata": {"persona": "Home builder"},
            "logical_error_detected": False
        }
        
        # This method doesn't exist yet (Red Phase)
        new_state = self.agent.apply_empathy(initial_state)
        
        # History length should be the same, but content should be refined
        self.assertEqual(len(new_state["history"]), 2)
        self.assertEqual(new_state["history"][-1]["role"], "assistant")
        self.assertNotEqual(new_state["history"][-1]["content"], "Why?")
        # Should be in Korean and polite
        self.assertIsInstance(new_state["history"][-1]["content"], str)

if __name__ == "__main__":
    unittest.main()
