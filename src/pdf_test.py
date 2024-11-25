import datetime

# 이제 import 시도  
from LLM.chatbot import Chatbot
from utils.pdf import PDFGenerator

def main():  
    """사용 예시"""  
    
    chatbot = Chatbot() 
    # 예제 지식 추가 (chatbot.py의 main 함수처럼)  
    example_texts = [  
        "11.3주 주유소 휘발유 판매가격은 전주 대비 4.8원 상승한 1633.9원/리터입니다.",  
        "11.2주 정유사 휘발유 공급가격은 전주 대비 7.7원 하락한 1558.7원/리터입니다.",  
        "휘발유 및 경유 판매가격은 10.3주부터 6주 연속 상승 중입니다."  
    ]  
    chatbot.add_knowledge(example_texts)  

    # ChatGPT에 질의  
    response = chatbot.chat(query)  

    # pdf 생성
    pdf_gen = PDFGenerator()  
    
    now = datetime.now().strftime("%Y%m%d_%H%M%S")  
    # 출력 경로 설정  
    if output_path is None:  
        output_path = f"report_{now}.pdf"  
    

    # 기본 사용  
    query = "최근 유가 동향에 대해 분석해주세요." 

    pdf_path = pdf_gen.create_report(query, now, response, output_path)  
    print(f"기본 보고서 생성됨: {pdf_path}")  
    
    # 템플릿 사용  
    template = """  
    다음 형식으로 응답해주세요:  
    1. 현황 분석  
    2. 주요 이슈  
    3. 향후 전망  
    4. 시사점  
    """  
    response = chatbot.chat(  
        f"다음 형식으로 응답해주세요: {template}\n\n질문: {query}"  
    )  
    now = datetime.now().strftime("%Y%m%d_%H%M%S")  
    pdf_path = pdf_gen.create_report(query, now, response, output_path)  
    print(f"템플릿 기반 보고서 생성됨: {pdf_path}")  

if __name__ == "__main__":  
    main()