# src/utils/pdf.py  
from reportlab.lib import colors  
from reportlab.lib.pagesizes import A4  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont  
import sys  
import os  
from datetime import datetime  

# 경로 설정  
current_dir = os.path.dirname(os.path.abspath(__file__))  
project_root = os.path.dirname(os.path.dirname(current_dir))  
llm_dir = os.path.join(project_root, 'src', 'LLM')  

# 필요한 경로들을 시스템 경로에 추가  
sys.path.append(project_root)  
sys.path.append(llm_dir)  
sys.path.append(os.path.join(llm_dir, 'core'))  

# 이제 import 시도  
from src.LLM.chatbot import Chatbot  

class PDFGenerator:  
    def __init__(self):  
        self.chatbot = Chatbot() 
        
        # 예제 지식 추가 (chatbot.py의 main 함수처럼)  
        example_texts = [  
            "11.3주 주유소 휘발유 판매가격은 전주 대비 4.8원 상승한 1633.9원/리터입니다.",  
            "11.2주 정유사 휘발유 공급가격은 전주 대비 7.7원 하락한 1558.7원/리터입니다.",  
            "휘발유 및 경유 판매가격은 10.3주부터 6주 연속 상승 중입니다."  
        ]  
        self.chatbot.add_knowledge(example_texts)  

        self.setup_fonts()  
        self.styles = self.setup_styles()  

    def setup_fonts(self):  
        # 한글 폰트 설정 (맑은 고딕 예시)  
        try:  
            pdfmetrics.registerFont(TTFont('Malgun', 'malgun.ttf'))  
        except:  
            print("Warning: Malgun Gothic font not found. Using default font.")  

    def setup_styles(self):  
        styles = getSampleStyleSheet()  
        # 한글 지원을 위한 스타일 설정  
        styles.add(ParagraphStyle(  
            name='Korean',  
            fontName='Malgun',  
            fontSize=10,  
            leading=16  
        ))  
        return styles  

    def create_report(self, query, template=None, output_path=None):  
        """  
        ChatGPT 응답을 받아 PDF 보고서 생성  
        
        Args:  
            query (str): ChatGPT에 물어볼 질문  
            template (str, optional): 응답 형식 템플릿  
            output_path (str, optional): PDF 저장 경로. 없으면 자동 생성  
        
        Returns:  
            str: 생성된 PDF 파일 경로  
        """  
        # 출력 경로 설정  
        if output_path is None:  
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
            output_path = f"report_{timestamp}.pdf"  

        # ChatGPT에 질의  
        if template:  
            response = self.chatbot.chat(  
                f"다음 형식으로 응답해주세요: {template}\n\n질문: {query}"  
            )  
        else:  
            response = self.chatbot.chat(query)  

        # PDF 문서 설정  
        doc = SimpleDocTemplate(  
            output_path,  
            pagesize=A4,  
            rightMargin=72,  
            leftMargin=72,  
            topMargin=72,  
            bottomMargin=72  
        )  

        # PDF 구성 요소  
        elements = []  

        # 제목 추가  
        title = Paragraph("분석 보고서", self.styles['Title'])  
        elements.append(title)  
        elements.append(Spacer(1, 30))  

        # 날짜 추가  
        date = Paragraph(  
            f"작성일자: {datetime.now().strftime('%Y년 %m월 %d일')}",  
            self.styles['Korean']  
        )  
        elements.append(date)  
        elements.append(Spacer(1, 20))  

        # 질문 추가  
        question = Paragraph(f"질문: {query}", self.styles['Korean'])  
        elements.append(question)  
        elements.append(Spacer(1, 20))  

        # 응답 내용 추가  
        for paragraph in response.split('\n'):  
            if paragraph.strip():  
                p = Paragraph(paragraph, self.styles['Korean'])  
                elements.append(p)  
                elements.append(Spacer(1, 12))  

        # PDF 생성  
        doc.build(elements)  
        return output_path  

def main():  
    """사용 예시"""  
    pdf_gen = PDFGenerator()  
    
    # 기본 사용  
    query = "최근 유가 동향에 대해 분석해주세요."  
    pdf_path = pdf_gen.create_report(query)  
    print(f"기본 보고서 생성됨: {pdf_path}")  
    
    # 템플릿 사용  
    template = """  
    다음 형식으로 응답해주세요:  
    1. 현황 분석  
    2. 주요 이슈  
    3. 향후 전망  
    4. 시사점  
    """  
    pdf_path = pdf_gen.create_report(  
        query=query,  
        template=template,  
        output_path="detailed_report.pdf"  
    )  
    print(f"템플릿 기반 보고서 생성됨: {pdf_path}")  

if __name__ == "__main__":  
    main()