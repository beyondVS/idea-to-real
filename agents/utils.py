import time
import functools
import logging
from agents.exceptions import LLMTransientError

logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=10):
    """지수 백오프를 적용한 재시도 데코레이터입니다.

    Args:
        max_retries: 최대 재시도 횟수.
        base_delay: 기본 대기 시간(초).
        max_delay: 최대 대기 시간(초).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except LLMTransientError as e:
                    if retries >= max_retries:
                        logger.error(f"Max retries reached. Error: {e}")
                        raise
                    
                    delay = min(base_delay * (2 ** retries), max_delay)
                    logger.warning(f"Transient error occurred: {e}. Retrying in {delay}s... ({retries + 1}/{max_retries})")
                    time.sleep(delay)
                    retries += 1
                except Exception:
                    # PermanentError나 기타 예외는 즉시 다시 발생시킴
                    raise
        return wrapper
    return decorator
