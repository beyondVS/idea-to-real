import pytest
from django.test import TestCase
from chat.models import Session, Message
from agents.inquiry import InquiryAgent
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
class TestDjangoIntegration(TestCase):
    @patch('agents.base.ProviderFactory.get_provider')
    def setUp(self, mock_get_provider):
        # Mock provider to avoid Django settings error
        mock_get_provider.return_value = MagicMock()
        self.session = Session.objects.create(title="Test Session")
        self.agent = InquiryAgent()
        # Mock provider to avoid API calls
        self.agent.provider = MagicMock()

    @patch('agents.base.BaseAgent.get_response')
    def test_send_message_updates_session_state(self, mock_get_response):
        """Test that calling generate_question updates step_count and metadata."""
        # Analyzer JSON response
        analyzer_response = '{"extracted_metadata": {"persona": "Architect"}, "root_cause_identified": false}'
        # Questioner response
        questioner_response = "건축을 하고 싶으시군요! 어떤 종류의 건물을 구상 중이신가요?"
        
        mock_get_response.side_effect = [analyzer_response, questioner_response]

        # Simulate user message
        Message.objects.create(session=self.session, sender='user', content="I want to design a building.")
        chat_history = self.session.messages.all()

        # Execute
        question, step_count, metadata = self.agent.generate_question(
            chat_history,
            current_step=self.session.step_count,
            current_metadata=self.session.metadata
        )

        # Verify
        self.assertEqual(step_count, 1)
        self.assertEqual(metadata["persona"], "Architect")
        self.assertIn("건축", question)
        
        # Simulate saving in view
        self.session.step_count = step_count
        self.session.metadata = metadata
        self.session.save()
        
        self.session.refresh_from_db()
        self.assertEqual(self.session.step_count, 1)
        self.assertEqual(self.session.metadata["persona"], "Architect")
