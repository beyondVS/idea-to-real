import pytest
from agents.exceptions import LLMBaseError, LLMTransientError, LLMPermanentError

def test_exception_inheritance():
    """예외 클래스들이 올바르게 상속되는지 확인합니다."""
    transient = LLMTransientError("Transient error")
    permanent = LLMPermanentError("Permanent error")
    
    assert isinstance(transient, LLMBaseError)
    assert isinstance(permanent, LLMBaseError)
    assert isinstance(transient, Exception)
    assert isinstance(permanent, Exception)

def test_exception_message():
    """예외 메시지가 올바르게 설정되는지 확인합니다."""
    msg = "Test error message"
    error = LLMBaseError(msg)
    assert str(error) == msg

def test_user_friendly_message():
    """사용자 친화적인 메시지 생성 기능을 확인합니다."""
    from agents.exceptions import get_user_friendly_message
    
    transient = LLMTransientError("Rate limit exceeded")
    permanent = LLMPermanentError("Invalid API Key")
    base = LLMBaseError("Unknown error")
    
    assert "이용량이 많아" in get_user_friendly_message(transient)
    assert "인증 정보" in get_user_friendly_message(permanent)
    assert "알 수 없는 에러" in get_user_friendly_message(base)
