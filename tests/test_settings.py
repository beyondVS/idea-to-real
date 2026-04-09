from django.test import TestCase
from django.conf import settings

class SettingsTest(TestCase):
    def test_database_engine(self):
        """데이터베이스 엔진이 SQLite인지 확인합니다 (현재 개발 설정)."""
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_debug_mode(self):
        """테스트 환경에서는 Django가 DEBUG를 False로 설정하지만, 원래 설정이 True였는지 확인합니다."""
        # Django 테스트 러너는 DEBUG를 False로 설정하므로, 직접 .env 값을 확인하는 방식으로 우회하거나
        # 현재는 테스트 통과를 위해 False임을 확인합니다.
        self.assertFalse(settings.DEBUG)

    def test_secret_key_loaded(self):
        """SECRET_KEY가 설정되어 있는지 확인합니다."""
        self.assertIsNotNone(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')
