from chatbot import Chatbot  

# 챗봇 초기화  
chatbot = Chatbot()  

# 테스트용 문서 추가  
documents = [  
    "파이썬은 1991년에 귀도 반 로섬이 개발한 프로그래밍 언어입니다.",  
    "파이썬의 특징은 읽기 쉽고 간단한 문법입니다.",  
    "인공지능은 기계가 학습, 추론, 판단을 할 수 있게 하는 기술입니다."  
]  
chatbot.add_knowledge(documents)  

# 대화 테스트  
response = chatbot.chat("파이썬은 누가 만들었어?")  
print(f"Assistant: {response}")