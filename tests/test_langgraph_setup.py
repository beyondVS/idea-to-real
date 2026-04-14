import unittest
from langgraph.graph import StateGraph

class TestLangGraphSetup(unittest.TestCase):
    def test_import_langgraph(self):
        """Test that langgraph can be imported and StateGraph can be instantiated."""
        try:
            from langgraph.graph import StateGraph
            graph = StateGraph(dict)
            self.assertIsNotNone(graph)
        except ImportError:
            self.fail("langgraph not installed")

if __name__ == "__main__":
    unittest.main()
