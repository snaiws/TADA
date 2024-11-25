# src/utils/pdf.py  
from reportlab.lib import colors 
from reportlab.lib.pagesizes import A4  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont  



class PDFGenerator:  
    def __init__(self):
        self.configs_doc = {
            "pagesize":A4,  
            "rightMargin":72,  
            "leftMargin":72,  
            "topMargin":72,  
            "bottomMargin":72  
        }
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

    def create_report(self, title:str, datetime:str, text:str, output_path=None):  
        """  
        ChatGPT 응답을 받아 PDF 보고서 생성  
        
        Args:  
            query (str): ChatGPT에 물어볼 질문  
            template (str, optional): 응답 형식 템플릿  
            output_path (str, optional): PDF 저장 경로. 없으면 자동 생성  
        
        Returns:  
            str: 생성된 PDF 파일 경로  
        """  

        # PDF 문서 설정
        kwargs = self.configs_doc + {'output_path':output_path}
        doc = SimpleDocTemplate(**kwargs)

        # PDF 구성 요소  
        elements = []  

        # 제목 추가  
        title = Paragraph("분석 보고서", self.styles['Title'])  
        elements.append(title)  
        elements.append(Spacer(1, 30))  

        # 날짜 추가  
        date = Paragraph(  
            f"작성일자: {datetime}",  
            self.styles['Korean']  
        )  
        elements.append(date)  
        elements.append(Spacer(1, 20))  

        # 응답 내용 추가
        for paragraph in text.split('\n'):  
            if paragraph.strip():  
                p = Paragraph(paragraph, self.styles['Korean'])  
                elements.append(p)  
                elements.append(Spacer(1, 12))  

        # PDF 생성  
        doc.build(elements)  
        return output_path  
