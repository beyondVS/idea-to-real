from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Message

def index(request):
    """세션 목록 및 새 세션 생성 페이지"""
    sessions = Session.objects.all()
    return render(request, 'chat/index.html', {'sessions': sessions})

def detail(request, session_id):
    """채팅 인터페이스 페이지"""
    session = get_object_or_404(Session, id=session_id)
    messages = session.messages.all()
    return render(request, 'chat/detail.html', {'session': session, 'messages': messages})

def create_session(request):
    """새 채팅 세션 생성"""
    if request.method == 'POST':
        title = request.POST.get('title', 'New Session')
        session = Session.objects.create(title=title)
        return redirect('chat:detail', session_id=session.id)
    return redirect('chat:index')

def send_message(request, session_id):
    """메시지 전송 및 저장"""
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                session=session,
                sender='user',
                content=content
            )
    return redirect('chat:detail', session_id=session.id)
