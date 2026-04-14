import unittest
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestAnalyzerNode(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    def test_analyzer_updates_state(self):
        """Test that the analyzer node updates metadata and logical error flag."""
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to build a house."}],
            "step_count": 0,
            "extracted_metadata": {},
            "logical_error_detected": False
        }
        
        # This method doesn't exist yet, so it will fail (Red Phase)
        new_state = self.agent.analyze_response(initial_state)
        
        self.assertIn("extracted_metadata", new_state)
        self.assertIn("logical_error_detected", new_state)
        # Check if it returns a dict (simulating LLM output for now)
        self.assertIsInstance(new_state["extracted_metadata"], dict)

if __name__ == "__main__":
    unittest.main()
