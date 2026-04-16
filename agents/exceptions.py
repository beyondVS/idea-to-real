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

def get_user_friendly_message(e):
    """예외 종류에 따라 사용자에게 보여줄 친화적인 메시지를 반환합니다."""
    if isinstance(e, LLMTransientError):
        return "현재 AI 서비스의 이용량이 많아 잠시 후 다시 시도해 주세요. (Rate Limit/Timeout)"
    elif isinstance(e, LLMPermanentError):
        return "AI 서비스 인증 정보에 문제가 발생했습니다. 관리자에게 문의하세요. (Auth Error)"
    else:
        return "AI 서비스 호출 중 알 수 없는 에러가 발생했습니다. 다시 시도해 주세요."
