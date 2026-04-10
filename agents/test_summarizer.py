import unittest
from unittest.mock import patch
from .summarizer import SummarizeAgent

class TestSummarizeAgent(unittest.TestCase):
    @patch('agents.base.BaseAgent.get_response')
    def test_summarize_chat_history(self, mock_get_response):
        mock_get_response.return_value = '{"problem_statement": "Build marketplace", "target_users": "Farmers and consumers", "core_features": [], "constraints": [], "success_criteria": ""}'
        agent = SummarizeAgent()
        
        chat_history = [
            {'sender': 'user', 'content': 'I want to build a marketplace.'},
            {'sender': 'ai_inquiry', 'content': 'Who are the target users?'},
            {'sender': 'user', 'content': 'Local farmers and consumers.'}
        ]
        
        summary = agent.summarize(chat_history)
        
        self.assertIn("target_users", summary)
        self.assertIn("farmers", summary["target_users"].lower())

