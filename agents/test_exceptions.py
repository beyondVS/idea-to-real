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
