import unittest
from unittest.mock import MagicMock, patch

class TestInquiryAgent(unittest.TestCase):
    @patch('agents.base.ProviderFactory.get_provider')
    def setUp(self, mock_get_provider):
        # Django 설정을 참조하지 않도록 프로바이더를 미리 주입하거나 팩토리를 목 처리합니다.
        mock_provider = MagicMock()
        mock_provider.model = "test-model"
        mock_get_provider.return_value = mock_provider
        
        from agents.inquiry import InquiryAgent
        self.agent = InquiryAgent()

    def test_inquiry_agent_initialization(self):
        """InquiryAgent가 올바르게 초기화되는지 확인합니다."""
        self.assertIsNotNone(self.agent.workflow)
        self.assertIn("Inquiry Agent", self.agent.SYSTEM_PROMPT)
        self.assertIn("5 Whys", self.agent.SYSTEM_PROMPT)
        self.assertNotIn("소크라테스", self.agent.SYSTEM_PROMPT)
        # InquiryAgent 클래스 객체에서 직접 __doc__ 확인
        from agents.inquiry import InquiryAgent
        self.assertNotIn("Socratic", InquiryAgent.__doc__)

    def test_system_prompt_strategy(self):
        """SYSTEM_PROMPT가 '간결한 5 Whys' 전략을 반영하고 있는지 확인합니다."""
        self.assertIn("핵심 질문", self.agent.SYSTEM_PROMPT)
        self.assertIn("간결하고 명확한 질문", self.agent.SYSTEM_PROMPT)
        self.assertIn("'왜(Why)'에 집중", self.agent.SYSTEM_PROMPT)

if __name__ == "__main__":
    unittest.main()
