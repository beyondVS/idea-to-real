from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Session, Message, ProblemSpecification

class ModelTest(TestCase):
    # ... (기존 모델 테스트 코드와 동일) ...
    def setUp(self):
        self.session = Session.objects.create(title="Test Session")
        self.problem_spec = ProblemSpecification.objects.create(
            session=self.session,
            content={"problem": "Test Problem"}
        )

    def test_session_creation(self):
        """Session 모델이 올바르게 생성되는지 확인합니다."""
        self.assertEqual(self.session.title, "Test Session")
        self.assertIsNotNone(self.session.created_at)

    def test_message_creation(self):
        """Message 모델이 올바르게 생성되는지 확인합니다."""
        message = Message.objects.create(
            session=self.session,
            sender="user",
            content="Hello AI"
        )
        self.assertEqual(message.session, self.session)
        self.assertEqual(message.sender, "user")
        self.assertEqual(message.content, "Hello AI")
        self.assertIsNotNone(message.timestamp)

    def test_problem_specification_creation(self):
        """ProblemSpecification 모델이 올바르게 생성되는지 확인합니다."""
        self.assertEqual(self.problem_spec.session, self.session)
        self.assertEqual(self.problem_spec.content["problem"], "Test Problem")
        self.assertIsNotNone(self.problem_spec.version)

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.session = Session.objects.create(title="Test View Session")

    def test_index_view(self):
        """인덱스 페이지가 정상적으로 응답하는지 확인합니다."""
        response = self.client.get(reverse('chat:index'))
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        """채팅 상세 페이지가 정상적으로 응답하는지 확인합니다."""
        response = self.client.get(reverse('chat:detail', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test View Session")

    def test_message_sending(self):
        """메시지 전송 기능이 정상적으로 작동하는지 확인합니다. (Mock 사용)"""
        from unittest.mock import patch
        with patch('agents.inquiry.InquiryAgent.generate_question') as mock_ai:
            mock_ai.return_value = "Mock AI response"
            response = self.client.post(reverse('chat:send_message', args=[self.session.id]), {
                'content': 'New user message'
            })
            self.assertEqual(response.status_code, 302)  # 성공 후 리다이렉트
            self.assertEqual(Message.objects.filter(session=self.session, sender='user').count(), 1)
            self.assertEqual(Message.objects.filter(session=self.session, sender='ai_inquiry').count(), 1)

    def test_ai_response_integration(self):
        """사용자 메시지 전송 후 AI 응답이 생성되는지 확인합니다. (Mock 사용)"""
        from unittest.mock import patch
        
        with patch('agents.inquiry.InquiryAgent.generate_question') as mock_ai:
            mock_ai.return_value = "This is a mock AI question."
            
            response = self.client.post(reverse('chat:send_message', args=[self.session.id]), {
                'content': 'I want to build a house.'
            })
            
            # AI 에이전트가 호출되었는지 확인
            mock_ai.assert_called_once()
            
            # AI 메시지가 저장되었는지 확인
            ai_messages = Message.objects.filter(session=self.session, sender='ai_inquiry')
            self.assertEqual(ai_messages.count(), 1)
            self.assertEqual(ai_messages.first().content, "This is a mock AI question.")
