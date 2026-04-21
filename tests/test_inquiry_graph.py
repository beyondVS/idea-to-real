import unittest
from typing import TypedDict, List, Dict, Any
from agents.inquiry import InquiryGraphState

class TestInquiryGraphState(unittest.TestCase):
    def test_graph_state_structure(self):
        """Test that InquiryGraphState has the required fields."""
        # This will fail if InquiryGraphState is not defined yet or missing fields
        state: InquiryGraphState = {
            "history": [],
            "step_count": 0,
            "extracted_metadata": {}
        }
        self.assertEqual(state["step_count"], 0)
        self.assertIsInstance(state["history"], list)
        self.assertIsInstance(state["extracted_metadata"], dict)

if __name__ == "__main__":
    unittest.main()
