from django.db import models
import uuid

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or str(self.id)

class Message(models.Model):
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
    session = models.OneToOneField(Session, related_name='specification', on_delete=models.CASCADE)
    content = models.JSONField()
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Specification for {self.session.title} (v{self.version})"
