from django.shortcuts import render, get_object_or_404, redirect
from .models import Session, Message
from agents.inquiry import InquiryAgent
from agents.critique import CritiqueAgent

def index(request):
    # ... (기존 코드와 동일) ...
    sessions = Session.objects.all().order_by('-created_at')
    return render(request, 'chat/index.html', {'sessions': sessions})

def detail(request, session_id):
    # ... (기존 코드와 동일) ...
    session = get_object_or_404(Session, id=session_id)
    messages = session.messages.all().order_by('timestamp')
    return render(request, 'chat/detail.html', {'session': session, 'messages': messages})

def create_session(request):
    """새 채팅 세션 생성"""
    if request.method == 'POST':
        title = request.POST.get('title', 'New Session')
        session = Session.objects.create(title=title)
        return redirect('chat:detail', session_id=session.id)
    return redirect('chat:index')

def send_message(request, session_id):
    """메시지 전송 및 저장, 그리고 AI 에이전트들의 응답 생성"""
    session = get_object_or_404(Session, id=session_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # 1. 사용자 메시지 저장
            Message.objects.create(
                session=session,
                sender='user',
                content=content
            )
            
            # 대화 기록 가져오기
            chat_history = session.messages.all().order_by('timestamp')
            
            # 2. Inquiry Agent 응답 생성
            inquiry_agent = InquiryAgent()
            ai_inquiry_content = inquiry_agent.generate_question(chat_history)
            Message.objects.create(
                session=session,
                sender='ai_inquiry',
                content=ai_inquiry_content
            )
            
            # 3. Critique Agent 응답 생성
            critique_agent = CritiqueAgent()
            ai_critique_content = critique_agent.generate_critique(chat_history)
            Message.objects.create(
                session=session,
                sender='ai_critique',
                content=ai_critique_content
            )
            
    return redirect('chat:detail', session_id=session.id)
