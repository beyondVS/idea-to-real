class LLMBaseError(Exception):
    """모든 LLM 관련 에러의 베이스 클래스입니다."""
    def __init__(self, message, original_error=None):
        super().__init__(message)
        self.original_error = original_error

class LLMTransientError(LLMBaseError):
    """재시도 가능한 일시적인 에러입니다 (예: Rate Limit, Timeout)."""
    pass

class LLMPermanentError(LLMBaseError):
    """재시도가 불가능한 영구적인 에러입니다 (예: 인증 실패, 잘못된 파라미터)."""
    pass
