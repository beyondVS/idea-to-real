import pytest
import time
from unittest.mock import MagicMock
from agents.utils import retry_with_backoff
from agents.exceptions import LLMTransientError, LLMPermanentError

def test_retry_success_on_first_try():
    mock_func = MagicMock(return_value="success")
    decorated = retry_with_backoff(max_retries=3)(mock_func)
    
    result = decorated()
    
    assert result == "success"
    assert mock_func.call_count == 1

def test_retry_success_after_failure():
    mock_func = MagicMock()
    mock_func.side_effect = [LLMTransientError("fail"), LLMTransientError("fail"), "success"]
    
    # 지수 백오프 시간을 줄이기 위해 base_delay 조절 (테스트용)
    decorated = retry_with_backoff(max_retries=3, base_delay=0.01)(mock_func)
    
    result = decorated()
    
    assert result == "success"
    assert mock_func.call_count == 3

def test_retry_max_retries_exceeded():
    mock_func = MagicMock()
    mock_func.side_effect = LLMTransientError("fail")
    
    decorated = retry_with_backoff(max_retries=2, base_delay=0.01)(mock_func)
    
    with pytest.raises(LLMTransientError):
        decorated()
    
    assert mock_func.call_count == 3  # Initial + 2 retries

def test_retry_stops_on_permanent_error():
    mock_func = MagicMock()
    mock_func.side_effect = LLMPermanentError("permanent fail")
    
    decorated = retry_with_backoff(max_retries=3, base_delay=0.01)(mock_func)
    
    with pytest.raises(LLMPermanentError):
        decorated()
    
    assert mock_func.call_count == 1
