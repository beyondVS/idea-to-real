from typing import TypedDict, List, Dict, Any, Annotated
import operator
import json
from langgraph.graph import StateGraph, START, END
from .base import BaseAgent

class InquiryGraphState(TypedDict):
    """Inquiry 워크플로우의 상태를 정의합니다.
    
    Attributes:
        history: 대화 이력 (기존 메시지에 누적됨)
        step_count: 현재 5 Whys 단계 (1~5)
        extracted_metadata: 분석을 통해 추출된 페르소나 및 숨겨진 전제
        logical_error_detected: 논리적 비약이나 모순 발견 여부
    """
    history: Annotated[List[Dict[str, str]], operator.add]
    step_count: int
    extracted_metadata: Dict[str, Any]
    logical_error_detected: bool

class InquiryAgent(BaseAgent):
    """사용자에게 질문을 던져 아이디어를 구체화하는 소크라테스식 질문 엔진입니다.

    Attributes:
        SYSTEM_PROMPT: 소크라테스식 질문을 위한 시스템 프롬프트입니다.
    """
    def __init__(self, provider=None):
        super().__init__(provider)
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """LangGraph 워크플로우를 구축하고 컴파일합니다."""
        builder = StateGraph(InquiryGraphState)
        
        # 노드 등록
        builder.add_node("analyzer", self.analyze_response)
        builder.add_node("questioner", self.generate_next_question)
        builder.add_node("empathizer", self.apply_empathy)
        
        # 엣지 연결
        builder.add_edge(START, "analyzer")
        
        # Analyzer 이후 조건부 분기
        builder.add_conditional_edges(
            "analyzer",
            self.should_continue,
            {
                "continue": "questioner",
                "end": END
            }
        )
        
        builder.add_edge("questioner", "empathizer")
        builder.add_edge("empathizer", END)
        
        return builder.compile()

    SYSTEM_PROMPT = """
당신은 'Problem Specification AI System'의 핵심 엔진인 'Socratic Inquiry Agent'입니다.
당신의 목표는 사용자의 간략한 아이디어나 직면한 문제를 구조화된 문제 기술서로 발전시키기 위해 질문을 던지는 것입니다.

[작동 원리]
1. 5 Whys 기법을 활용하여 문제의 근본 원인(Root Cause)을 파악하십시오.
2. 소크라테스식 질문법을 사용하여 사용자가 자신의 생각에 숨겨진 전제를 발견하게 하십시오.
3. 한 번에 하나씩만 질문하십시오. 너무 많은 질문은 사용자를 지치게 합니다.
4. 사용자의 답변을 경청하고, 공감한 뒤, 논리적 비약이 있는 부분을 파고드십시오.
5. 친절하고 전문적인 한국어 말투를 사용하십시오.

[출력 형식]
사용자의 답변에 대한 분석을 간단히 언급한 후, 다음 단계로 나아가기 위한 날카로운 질문을 하나 던지십시오.
"""

    ANALYZER_PROMPT = """
당신은 사용자의 답변을 분석하여 논리적 취약점과 핵심 정보를 추출하는 'Logical Analyzer'입니다.

[분석 지침]
1. 사용자의 답변에서 논리적 비약(Jump in logic)이나 숨겨진 전제(Hidden assumption)를 찾아내십시오.
2. 현재까지 파악된 사용자의 페르소나(역할)나 문제의 배경 정보를 추출하십시오.
3. 근본 원인이 이미 파악되었는지, 혹은 추가 질문이 필요한지 판단하십시오.

[출력 형식]
반드시 아래의 JSON 형식을 지켜서 응답하십시오. 다른 텍스트는 포함하지 마십시오.
{
    "logical_error_detected": true/false,
    "extracted_metadata": {
        "persona": "추출된 페르소나",
        "assumptions": ["전제1", "전제2"],
        "context": "배경 정보"
    },
    "root_cause_identified": true/false
}
"""

    EMPATHIZER_PROMPT = """
당신은 AI의 질문을 검토하여 공감과 전문적인 한국어 톤앤매너를 적용하는 'Empathy Specialist'입니다.

[작업 지침]
1. 입력받은 질문의 핵심 의도는 유지하십시오.
2. 사용자의 상황에 공감하는 문장을 추가하여 대화의 부드러움을 높이십시오.
3. '해요체'나 '하십시오체'를 적절히 혼용하여 전문적이면서도 친절한 한국어 어조를 완성하십시오.
4. 질문은 한 번에 하나만 포함되어야 합니다.

[입력 정보]
- 원본 질문: {raw_question}
- 현재 페르소나/맥락: {metadata}

[출력 형식]
공감과 질문이 포함된 정제된 한국어 문장만 출력하십시오.
"""

    def analyze_response(self, state: InquiryGraphState) -> InquiryGraphState:
        """사용자의 마지막 답변을 분석하여 상태를 업데이트합니다.
        
        Args:
            state: 현재 워크플로우 상태
            
        Returns:
            업데이트된 상태
        """
        messages = [
            {"role": "system", "content": self.ANALYZER_PROMPT},
        ]
        # 최신 대화 이력 추가
        messages.extend(state["history"])
        
        response_text = self.get_response(messages)
        
        try:
            # JSON 응답 파싱 (LLM이 마크다운 코드 블록으로 감쌌을 경우 처리)
            clean_json = response_text.strip().replace("```json", "").replace("```", "")
            analysis = json.loads(clean_json)
            
            # 상태 업데이트
            state["logical_error_detected"] = analysis.get("logical_error_detected", False)
            # 기존 메타데이터와 병합
            state["extracted_metadata"].update(analysis.get("extracted_metadata", {}))
            # root_cause_identified는 엣지 로직에서 사용하므로 메타데이터에 임시 저장하거나 
            # 필요한 경우 상태 구조를 확장할 수 있음. 현재는 metadata에 저장.
            state["extracted_metadata"]["root_cause_identified"] = analysis.get("root_cause_identified", False)
            
        except (json.JSONDecodeError, KeyError, Exception) as e:
            # 파싱 실패 시 기본값 유지 (로깅 필요)
            print(f"Error parsing analyzer response: {e}")
            pass
            
        return state

    def generate_next_question(self, state: InquiryGraphState) -> InquiryGraphState:
        """분석된 상태를 바탕으로 다음 질문을 생성합니다.
        
        Args:
            state: 현재 워크플로우 상태
            
        Returns:
            업데이트된 상태 (history에 질문 추가, step_count 증가)
        """
        # 시스템 프롬프트 구성 (분석된 메타데이터 반영 가능)
        system_prompt = self.SYSTEM_PROMPT
        if state["extracted_metadata"]:
            system_prompt += f"\n\n[현재까지 파악된 정보]\n{state['extracted_metadata']}"
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(state["history"])
        
        question = self.get_response(messages)
        
        # 상태 업데이트
        state["history"].append({"role": "assistant", "content": question})
        state["step_count"] += 1
        
        return state

    def apply_empathy(self, state: InquiryGraphState) -> InquiryGraphState:
        """생성된 질문에 공감과 한국어 톤앤매너를 적용합니다.
        
        Args:
            state: 현재 워크플로우 상태
            
        Returns:
            업데이트된 상태 (마지막 assistant 메시지 수정)
        """
        if not state["history"] or state["history"][-1]["role"] != "assistant":
            return state
            
        raw_question = state["history"][-1]["content"]
        
        prompt = self.EMPATHIZER_PROMPT.format(
            raw_question=raw_question,
            metadata=json.dumps(state["extracted_metadata"], ensure_ascii=False)
        )
        
        refined_question = self.get_response([
            {"role": "system", "content": prompt},
            {"role": "user", "content": "질문을 정제해 주세요."}
        ])
        
        # 마지막 메시지 교체
        state["history"][-1]["content"] = refined_question
        
        return state

    def should_continue(self, state: InquiryGraphState) -> str:
        """대화를 계속할지 종료할지 결정하는 엣지 로직입니다.
        
        Args:
            state: 현재 워크플로우 상태
            
        Returns:
            "continue" 또는 "end"
        """
        # 1. 근본 원인이 파악되었으면 종료
        if state["extracted_metadata"].get("root_cause_identified", False):
            return "end"
            
        # 2. 최대 질문 단계(5단계)에 도달했으면 종료
        if state["step_count"] >= 5:
            return "end"
            
        # 그 외에는 계속 진행
        return "continue"

    def generate_question(self, chat_history, current_step=0, current_metadata=None):
        """LangGraph 워크플로우를 실행하여 다음 질문을 생성합니다.

        Args:
            chat_history: Django 모델의 Message 객체 리스트입니다.
            current_step: 세션의 현재 질문 단계입니다.
            current_metadata: 세션의 현재 메타데이터 (JSON)입니다.

        Returns:
            Tuple[str, int, dict]: (생성된 질문, 업데이트된 step_count, 업데이트된 metadata)
        """
        if current_metadata is None:
            current_metadata = {}

        # 1. Django 메시지를 GraphState history 형식으로 변환
        history = []
        for msg in chat_history:
            # ai_inquiry와 ai_critique는 모두 assistant로 간주하거나, 
            # 5 Whys 흐름을 위해서는 ai_inquiry만 assistant로 간주할 수도 있음.
            # 여기서는 모든 AI 메시지를 assistant로 간주함.
            role = "user" if msg.sender == "user" else "assistant"
            history.append({"role": role, "content": msg.content})

        # 2. 초기 상태 구성
        initial_state: InquiryGraphState = {
            "history": history,
            "step_count": current_step,
            "extracted_metadata": current_metadata,
            "logical_error_detected": False
        }

        # 3. 워크플로우 실행
        final_state = self.workflow.invoke(initial_state)

        # 4. 마지막 생성된 질문 추출
        # history의 마지막 메시지가 assistant가 아닐 경우(예: 종료됨)를 처리
        last_message = final_state["history"][-1]
        question = last_message["content"] if last_message["role"] == "assistant" else "문제가 충분히 정의되었습니다. 기술서를 확인해 보세요."

        return question, final_state["step_count"], final_state["extracted_metadata"]
