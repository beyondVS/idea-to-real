import unittest
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestEdgeLogic(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    def test_should_continue_edge_logic(self):
        """Test the routing logic for the inquiry workflow."""
        # Case 1: Root cause not identified and step count < 5 -> continue
        state_continue: InquiryGraphState = {
            "history": [],
            "step_count": 2,
            "extracted_metadata": {"root_cause_identified": False},
            "logical_error_detected": False
        }
        self.assertEqual(self.agent.should_continue(state_continue), "continue")

        # Case 2: Root cause identified -> end
        state_end_cause: InquiryGraphState = {
            "history": [],
            "step_count": 2,
            "extracted_metadata": {"root_cause_identified": True},
            "logical_error_detected": False
        }
        self.assertEqual(self.agent.should_continue(state_end_cause), "end")

        # Case 3: Step count >= 5 -> end (safety break)
        state_end_steps: InquiryGraphState = {
            "history": [],
            "step_count": 5,
            "extracted_metadata": {"root_cause_identified": False},
            "logical_error_detected": False
        }
        self.assertEqual(self.agent.should_continue(state_end_steps), "end")

if __name__ == "__main__":
    unittest.main()
