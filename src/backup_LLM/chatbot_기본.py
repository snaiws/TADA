from typing import List, Optional  
from core.openai import OpenAIClient  
import json  
import os  

class Chatbot:  
    def __init__(self):  
        self.client = OpenAIClient()  
        self.conversation_history: List[dict] = []  
        self.max_history = 10  # 최대 대화 기록 수  
        
    def get_context_from_rag(self, query: str) -> Optional[str]:  
        """  
        RAG 시스템에서 관련 컨텍스트 검색  
        실제 구현 시 벡터 DB나 다른 검색 시스템과 연동  
        """  
        # TODO: 실제 RAG 구현  
        return None  
        
    def save_conversation(self):  
        """대화 내용 저장"""  
        if not self.conversation_history:  
            return  
            
        os.makedirs('conversations', exist_ok=True)  
        filename = f"conversations/chat_{len(os.listdir('conversations'))}.json"  
        
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
        self.save_conversation()  # 기존 대화 저장  
        self.conversation_history = []  

def main():  
    chatbot = Chatbot()  
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

if __name__ == "__main__":  
    main()