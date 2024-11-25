import os  
from typing import List, Dict, Optional  
import json  

from .core.openai import OpenAIClient  
from .core.document_store import DocumentStore  



class Chatbot:  
    def __init__(self, client, max_history, path_history):  
        self.client = client
        self.document_store = DocumentStore()  
        self.conversation_history: List[dict] = []
        self.max_history = max_history
        self.path_history = path_history
        

    def add_knowledge(self, texts: List[str], metadata: Optional[List[Dict]] = None):  
        """지식 베이스에 문서 추가"""  
        self.document_store.add_documents(texts, metadata)  
        
        
    def get_context_from_rag(self, query: str) -> Optional[str]:  
        """RAG 시스템에서 관련 컨텍스트 검색"""  
        try:  
            relevant_docs = self.document_store.search(query)  
            if relevant_docs:  
                return "\n".join(relevant_docs)  
        except Exception as e:  
            print(f"RAG 검색 중 오류 발생: {str(e)}")  
        return None  
        
        
    def save_conversation(self):  
        """대화 내용 저장"""  
        if not self.conversation_history:  
            return  
            
        os.makedirs(self.path_history, exist_ok=True)  
        filename = f"conversations/chat_{len(os.listdir(self.path_history))}.json"  
        
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
                self.conversation_history = self.conversation_history[-self.max_history*2:]  
            
            return response  
            
        except Exception as e:  
            print(f"Error in chat: {str(e)}")  
            return "죄송합니다. 오류가 발생했습니다."  
            

    def clear_history(self):  
        """대화 기록 초기화"""  
        self.save_conversation()  
        self.conversation_history = []  



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
    chatbot = Chatbot(core, max_history, path_history)  
    
    # 예제 지식 추가  
    example_texts = [  
        "파이썬은 1991년에 귀도 반 로섬이 개발한 프로그래밍 언어입니다.",  
        "파이썬은 읽기 쉽고 간단한 문법을 가진 언어입니다.",  
        "ChatGPT는 OpenAI가 개발한 대규모 언어 모델입니다."  
    ]  
    chatbot.add_knowledge(example_texts)  

    # start
    print("챗봇을 시작합니다. 종료하려면 'quit' 또는 'exit'를 입력하세요.")  
    while True:  
        user_input = input("\nUser: ").strip()  
        
        if user_input.lower() in ['quit', 'exit']:  
            chatbot.save_conversation()  
            print("대화를 종료합니다.")  
            break  
            
        if user_input.lower() == 'clear':  
            chatbot.clear_history()  
            print("대화 기록이 초기화되었습니다.")  
            continue  
            
        if not user_input:  
            continue  
            
        response = chatbot.chat(user_input)  
        print(f"\nAssistant: {response}")  

