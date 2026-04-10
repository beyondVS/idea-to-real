from django.db import models
import uuid

class Session(models.Model):
    """사용자와의 대화 세션을 관리하는 모델입니다.

    Attributes:
        id: 세션의 고유 식별자 (UUID)입니다.
        title: 세션의 제목입니다.
        created_at: 세션 생성 일시입니다.
        updated_at: 세션 정보 수정 일시입니다.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or str(self.id)

class Message(models.Model):
    """대화 세션 내의 개별 메시지를 관리하는 모델입니다.

    Attributes:
        session: 메시지가 속한 세션에 대한 외래 키입니다.
        sender: 메시지 발신자 (user, ai_inquiry, ai_critique)입니다.
        content: 메시지 내용입니다.
        timestamp: 메시지 전송 일시입니다.
    """
    SENDER_CHOICES = (
        ('user', 'User'),
        ('ai_inquiry', 'AI Inquiry'),
        ('ai_critique', 'AI Critique'),
    )
    session = models.ForeignKey(Session, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class ProblemSpecification(models.Model):
    """세션의 대화 내용을 요약하여 생성된 문제 기술서 모델입니다.

    Attributes:
        session: 대응하는 세션에 대한 일대일 관계 키입니다.
        content: 구조화된 기술서 내용 (JSON 형식)입니다.
        version: 기술서의 버전 번호입니다.
        created_at: 기술서 최초 생성 일시입니다.
        updated_at: 기술서 수정 일시입니다.
    """
    session = models.OneToOneField(Session, related_name='specification', on_delete=models.CASCADE)
    content = models.JSONField()
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Specification for {self.session.title} (v{self.version})"

