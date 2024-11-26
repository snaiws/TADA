import os
from typing import List, Dict, Optional
import json

from .core.openaiAPI import OpenAIClient
from .core.document_store import DocumentStore



class Chatbot:
    def __init__(self, client, max_history, path_history, session_id: str):
        self.client = client
        self.document_store = DocumentStore()
        self.conversation_history: List[dict] = []
        self.max_history = max_history
        self.path_history = path_history
        self.session_id = session_id


    def add_knowledge(self, texts: List[str], metadata: Optional[List[Dict]] = None):
        """지식 베이스에 문서 추가"""
        self.document_store.add_documents(texts, metadata)


    def get_context_from_rag(self, query: str) -> Optional[str]:
        """RAG 시스템에서 관련 컨텍스트 검색"""
        try:
            relevant_docs = self.document_store.search(query)
            # 검색 결과가 비어 있으면 None 반환
            if not relevant_docs or len(relevant_docs) == 0:
                print("검색 결과가 비어 있습니다.")
                return None

            # 검색된 문서를 문자열로 병합하여 반환
            return "\n".join(relevant_docs)

        except Exception as e:
            print(f"RAG 검색 중 오류 발생: {str(e)}")
            return None


    def save_conversation(self):
        """대화 내용 저장"""
        if not self.conversation_history:
            return

        os.makedirs(self.path_history, exist_ok=True)
        filename = f"{self.path_history}/{self.session_id}_chat.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)


    def chat(self, user_input: str) -> str:
        """사용자 입력에 대한 응답 생성"""
        try:
            # RAG를 통한 컨텍스트 검색
            context = self.get_context_from_rag(user_input)

            # 메시지 구성
            messages = self.client.create_messages(
                user_input,
                self.conversation_history,
                context
            )

            # 응답 생성
            response = self.client.get_completion(messages)

            # 대화 기록 업데이트
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": response})

            # 대화 기록 제한
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = self.conversation_history[-self.max_history * 2:]

            return response

        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return "죄송합니다. 오류가 발생했습니다."


    def clear_history(self):
        """대화 기록 초기화"""
        self.save_conversation()
        self.conversation_history = []


class SessionManager:
    def __init__(self, client, max_history, path_history):
        self.client = client
        self.max_history = max_history
        self.path_history = path_history
        self.sessions: Dict[str, Chatbot] = {}


    def get_chatbot(self, session_id: str) -> Chatbot:
        """특정 세션 ID에 해당하는 Chatbot 인스턴스를 반환하거나 새로 생성"""
        if session_id not in self.sessions:
            self.sessions[session_id] = Chatbot(
                client=self.client,
                max_history=self.max_history,
                path_history=self.path_history,
                session_id=session_id
            )
        return self.sessions[session_id]



if __name__ == "__main__":
    # python -m src.LLM.chatbot

    from dotenv import load_dotenv
    load_dotenv(verbose=False)

    # init
    model_name = "gpt-3.5-turbo"
    key = os.getenv("OPENAI_API_KEY")
    system_prompt = """You are a helpful AI assistant with strong contextual awareness.   
        Always maintain context from the conversation history and refer back to previous information when relevant.   
        If you're unsure about something previously discussed, you can ask for clarification.  
        Provide clear, accurate, and concise responses while maintaining a natural conversational tone.
        """
    core = OpenAIClient(model_name, key, system_prompt)
    max_history = 10
    path_history = "conversations"
    manager = SessionManager(core, max_history, path_history)

    print("챗봇을 시작합니다. 종료하려면 'quit' 또는 'exit'를 입력하세요.")
    while True:
        session_id = input("\nSession ID (새 세션 시작하려면 ID 입력): ").strip()
        if not session_id:
            print("세션 ID를 입력해주세요.")
            continue

        chatbot = manager.get_chatbot(session_id)

        while True:
            user_input = input(f"\n[{session_id}] User: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                chatbot.save_conversation()
                print(f"세션 {session_id} 대화를 종료합니다.")
                break

            if user_input.lower() == 'clear':
                chatbot.clear_history()
                print(f"세션 {session_id} 대화 기록이 초기화되었습니다.")
                continue

            if not user_input:
                continue

            response = chatbot.chat(user_input)
            print(f"\n[{session_id}] Assistant: {response}")
