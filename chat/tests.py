from django.test import TestCase
from django.utils import timezone
from .models import Session, Message, ProblemSpecification

class ModelTest(TestCase):
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
