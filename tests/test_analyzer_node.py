import unittest
from unittest.mock import patch, MagicMock
from agents.inquiry import InquiryAgent, InquiryGraphState

class TestAnalyzerNode(unittest.TestCase):
    def setUp(self):
        # Mock provider to avoid Django settings error during initialization
        self.agent = InquiryAgent(provider=MagicMock())

    @patch('agents.base.BaseAgent.get_response')
    def test_analyzer_updates_state(self, mock_get_response):
        """Test that the analyzer node updates metadata and logical error flag."""
        # Mocking the JSON response from LLM
        mock_get_response.return_value = """
        {
            "logical_error_detected": true,
            "extracted_metadata": {
                "persona": "Home builder",
                "assumptions": ["Needs a lot of money"],
                "context": "Building a house in Korea"
            },
            "root_cause_identified": false
        }
        """
        
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to build a house."}],
            "step_count": 0,
            "extracted_metadata": {},
            "logical_error_detected": False
        }
        
        new_state = self.agent.analyze_response(initial_state)
        
        self.assertTrue(new_state["logical_error_detected"])
        self.assertEqual(new_state["extracted_metadata"]["persona"], "Home builder")
        self.assertIn("assumptions", new_state["extracted_metadata"])
        self.assertIsInstance(new_state["extracted_metadata"], dict)

if __name__ == "__main__":
    unittest.main()
