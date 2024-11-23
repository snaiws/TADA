import os  
from typing import List, Optional  
from openai import OpenAI  
from dotenv import load_dotenv  

class OpenAIClient:  
    def __init__(self):  
        load_dotenv()  
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  
        self.model = "gpt-3.5-turbo"  
        self.system_prompt = """You are a helpful AI assistant with strong contextual awareness.   
        Always maintain context from the conversation history and refer back to previous information when relevant.   
        If you're unsure about something previously discussed, you can ask for clarification.  
        Provide clear, accurate, and concise responses while maintaining a natural conversational tone."""  
        
    def get_completion(  
        self,   
        messages: List[dict],  
        temperature: float = 0.7,  
        max_tokens: Optional[int] = None  
    ) -> str:  
        """OpenAI API를 호출하여 응답을 생성"""  
        try:  
            response = self.client.chat.completions.create(  
                model=self.model,  
                messages=messages,  
                temperature=temperature,  
                max_tokens=max_tokens  
            )  
            return response.choices[0].message.content  
        except Exception as e:  
            print(f"Error during API call: {str(e)}")  
            return "죄송합니다. 응답 생성 중 오류가 발생했습니다."  

    def create_messages(  
        self,   
        user_input: str,   
        conversation_history: List[dict] = None,  
        context: str = None  
    ) -> List[dict]:  
        """대화 메시지 구성"""  
        messages = [{"role": "system", "content": self.system_prompt}]  
        
        # RAG 컨텍스트가 있는 경우 추가  
        if context:  
            messages.append({  
                "role": "system",   
                "content": f"Consider this relevant information: {context}"  
            })  
        
        # 대화 기록 추가  
        if conversation_history:  
            messages.extend(conversation_history)  
            
        # 현재 사용자 입력 추가  
        messages.append({"role": "user", "content": user_input})  
        
        return messages