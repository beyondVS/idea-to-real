from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages as django_messages
from .models import Session, Message, ProblemSpecification
from agents.inquiry import InquiryAgent
from agents.summarizer import SummarizeAgent
from agents.exceptions import LLMBaseError, get_user_friendly_message

def index(request):
    """채팅 세션 목록을 표시하는 메인 페이지 뷰입니다.

    Args:
        request: Django HttpRequest 객체입니다.

    Returns:
        세션 목록이 렌더링된 HttpResponse 객체입니다.
    """
    sessions = Session.objects.all().order_by('-created_at')
    return render(request, 'chat/index.html', {'sessions': sessions})

def detail(request, session_id):
    """특정 채팅 세션의 상세 메시지 내역을 표시하는 뷰입니다.

    Args:
        request: Django HttpRequest 객체입니다.
        session_id: 조회할 세션의 UUID입니다.

    Returns:
        채팅 내역이 렌더링된 HttpResponse 객체입니다.
    """
    session = get_object_or_404(Session, id=session_id)
    chat_messages = session.messages.all().order_by('timestamp')
    return render(request, 'chat/detail.html', {'session': session, 'chat_messages': chat_messages})

def create_session(request):
    """새로운 채팅 세션을 생성하고 상세 페이지로 리다이렉트합니다.

    Args:
        request: Django HttpRequest 객체입니다.

    Returns:
        생성된 세션 페이지로의 HttpResponseRedirect 객체입니다.
    """
    if request.method == 'POST':
        title = request.POST.get('title', 'New Session')
        session = Session.objects.create(title=title)
        return redirect('chat:detail', session_id=session.id)
    return redirect('chat:index')

def send_message(request, session_id):
    """사용자 메시지를 처리하고 AI 에이전트(Inquiry)의 응답을 생성합니다.

    Args:
        request: Django HttpRequest 객체입니다.
        session_id: 메시지를 보낼 세션의 UUID입니다.

    Returns:
        세션 상세 페이지로의 HttpResponseRedirect 객체입니다.
    """
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

            try:
                # 2. Inquiry Agent 응답 생성 (LangGraph 워크플로우 실행)
                inquiry_agent = InquiryAgent()
                ai_inquiry_content, updated_step, updated_metadata = inquiry_agent.generate_question(
                    chat_history, 
                    current_step=session.step_count, 
                    current_metadata=session.metadata
                )
                
                # 세션 상태 업데이트
                session.step_count = updated_step
                session.metadata = updated_metadata
                session.save()

                Message.objects.create(
                    session=session,
                    sender='ai_inquiry',
                    content=ai_inquiry_content
                )
            except LLMBaseError as e:
                # LLM 관련 에러 발생 시 사용자 친화적인 메시지 추가
                user_msg = get_user_friendly_message(e)
                django_messages.error(request, user_msg)
            except Exception as e:
                # 기타 알 수 없는 에러 처리
                django_messages.error(request, f"알 수 없는 에러가 발생했습니다: {str(e)}")

    return redirect('chat:detail', session_id=session.id)

def _get_or_create_specification(session):
    """세션의 대화 내역을 바탕으로 문제 기술서를 생성하거나 업데이트합니다.

    Args:
        session: ProblemSpecification을 생성할 Session 객체입니다.

    Returns:
        생성된 문제 기술서의 내용(딕셔너리)입니다. 대화 내역이 없으면 에러 메시지를 반환합니다.
    """
    chat_history = session.messages.all().order_by('timestamp')
    if not chat_history.exists():
        return {"error": "No chat history available to summarize."}

    agent = SummarizeAgent()
    summary_data = agent.summarize(chat_history)

    spec, created = ProblemSpecification.objects.update_or_create(
        session=session,
        defaults={'content': summary_data}
    )
    if not created:
        spec.version += 1
        spec.save()

    return spec.content

def export_json(request, session_id):
    """문제 기술서를 JSON 형식으로 내보내는 뷰입니다.

    Args:
        request: Django HttpRequest 객체입니다.
        session_id: 내보낼 세션의 UUID입니다.

    Returns:
        JSON 데이터가 담긴 JsonResponse 객체입니다.
    """
    session = get_object_or_404(Session, id=session_id)
    content = _get_or_create_specification(session)
    return JsonResponse(content)

def export_markdown(request, session_id):
    """문제 기술서를 Markdown 형식으로 내보내는 뷰입니다.

    Args:
        request: Django HttpRequest 객체입니다.
        session_id: 내보낼 세션의 UUID입니다.

    Returns:
        Markdown 파일 다운로드를 위한 HttpResponse 객체입니다.
    """
    session = get_object_or_404(Session, id=session_id)
    content = _get_or_create_specification(session)

    if "error" in content:
        md_text = f"# Error\n\n{content['error']}"
    else:
        md_text = f"# Problem Specification: {session.title}\n\n"
        md_text += f"## Problem Statement\n{content.get('problem_statement', '')}\n\n"
        md_text += f"## Target Users\n{content.get('target_users', '')}\n\n"
        md_text += f"## Core Features\n"
        for feature in content.get('core_features', []):
            md_text += f"- {feature}\n"
        md_text += f"\n## Constraints\n"
        for constraint in content.get('constraints', []):
            md_text += f"- {constraint}\n"
        md_text += f"\n## Success Criteria\n{content.get('success_criteria', '')}\n"

    response = HttpResponse(md_text, content_type="text/markdown; charset=utf-8")
    response['Content-Disposition'] = f'attachment; filename="specification_{session.id}.md"'
    return response
