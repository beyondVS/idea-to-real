import pytest
from django.test import TestCase
from chat.models import Session, Message
from agents.inquiry import InquiryAgent
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
class TestDjangoIntegration(TestCase):
    def setUp(self):
        self.session = Session.objects.create(title="Test Session")
        self.agent = InquiryAgent()
        # Mock provider to avoid API calls
        self.agent.provider = MagicMock()

    @patch('agents.base.BaseAgent.get_response')
    def test_send_message_updates_session_state(self, mock_get_response):
        """Test that calling generate_question updates step_count and metadata."""
        # Analyzer JSON response
        analyzer_response = '{"logical_error_detected": false, "extracted_metadata": {"persona": "Architect"}, "root_cause_identified": false}'
        # Questioner response
        questioner_response = "What kind of building?"
        # Empathizer response
        empathizer_response = "I see. What kind of building do you want to design?"
        
        mock_get_response.side_effect = [analyzer_response, questioner_response, empathizer_response]

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
        self.assertIn("design", question)
        
        # Simulate saving in view
        self.session.step_count = step_count
        self.session.metadata = metadata
        self.session.save()
        
        self.session.refresh_from_db()
        self.assertEqual(self.session.step_count, 1)
        self.assertEqual(self.session.metadata["persona"], "Architect")
