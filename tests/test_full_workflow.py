import unittest
from agents.inquiry import InquiryAgent, InquiryGraphState
from langgraph.graph.state import CompiledStateGraph

class TestFullWorkflow(unittest.TestCase):
    def setUp(self):
        self.agent = InquiryAgent()

    def test_workflow_compilation(self):
        """Test that the workflow is correctly compiled."""
        # This attribute should exist and be a compiled graph
        self.assertIsInstance(self.agent.workflow, CompiledStateGraph)

    def test_workflow_execution_step(self):
        """Test a single execution step of the workflow."""
        initial_state: InquiryGraphState = {
            "history": [{"role": "user", "content": "I want to start a business."}],
            "step_count": 0,
            "extracted_metadata": {},
            "logical_error_detected": False
        }
        
        # Run the workflow once
        # Note: In real scenarios, we might use agent.workflow.invoke(initial_state)
        # For testing, we verify the integration of nodes.
        final_state = self.agent.workflow.invoke(initial_state)
        
        self.assertTrue(final_state["step_count"] > 0)
        self.assertEqual(final_state["history"][-1]["role"], "assistant")
        self.assertIn("extracted_metadata", final_state)

if __name__ == "__main__":
    unittest.main()
