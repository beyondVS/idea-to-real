import unittest
from unittest.mock import patch, MagicMock
from agents.inquiry import InquiryAgent, InquiryGraphState
from langgraph.graph.state import CompiledStateGraph

class TestFullWorkflow(unittest.TestCase):
    def setUp(self):
        # Mock provider to avoid Django settings error during initialization
        self.agent = InquiryAgent(provider=MagicMock())

    def test_workflow_compilation(self):
        """Test that the workflow is correctly compiled."""
        # This attribute should exist and be a compiled graph
        self.assertIsInstance(self.agent.workflow, CompiledStateGraph)

    @patch('agents.base.BaseAgent.get_response')
    def test_workflow_execution_step(self, mock_get_response):
        """Test a single execution step of the workflow."""
        # side_effect: analyzer (JSON), questioner (Question), empathizer (Refined Question)
        mock_get_response.side_effect = [
            '{"logical_error_detected": false, "extracted_metadata": {"goal": "business"}, "root_cause_identified": false}',
            "What kind of business are you planning?",
            "새로운 사업을 구상 중이시군요! 구체적으로 어떤 종류의 사업을 계획하고 계신가요?"
        ]

        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to start a business."}],
            "step_count": 0,
            "extracted_metadata": {},
            "logical_error_detected": False
        }
        
        # Run the workflow once
        final_state = self.agent.workflow.invoke(initial_state)
        
        self.assertTrue(final_state["step_count"] > 0)
        self.assertEqual(final_state["history"][-1]["role"], "assistant")
        self.assertIn("goal", final_state["extracted_metadata"])
        self.assertIn("사업을 구상 중이시군요", final_state["history"][-1]["content"])

if __name__ == "__main__":
    unittest.main()
