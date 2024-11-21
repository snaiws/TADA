from datetime import datetime  
from bs4 import BeautifulSoup  
from core.soup import get_html  
from loader.db.connector import Database  
from loader.db.query import query_creat_table_oil, query_update_oilprice  

def get_oilprice_now(dbinfo):  
    # URL 설정  
    url = 'https://www.opinet.co.kr/user/main/mainView.do'  
    
    # HTML 가져오기  
    html = get_html(url)  
    if not html:  
        print("Failed to fetch data from website")  
        return  
    
    # BeautifulSoup 객체 생성  
    soup = BeautifulSoup(html, 'html.parser')  
    
    try:  
        # XPath에 해당하는 요소 찾기 (BeautifulSoup에서는 CSS 선택자 사용)  
        price_element = soup.select_one('#oilcon1 > div > dl:nth-child(1) > dd > span:nth-child(1)')  
        if price_element:  
            price = float(price_element.text.replace(',', ''))  
            
            # 데이터베이스 연결  
            db = Database(  
                host=dbinfo["host"],  
                port=dbinfo["port"],  
                user=dbinfo["user"],  
                password=dbinfo["password"],  
                database=dbinfo["database"]  
            )  
            
            # 테이블 생성 확인  
            db.setter(query_creat_table_oil())  
            
            # 현재 날짜  
            today = datetime.now().strftime('%Y-%m-%d')  
            
            # 데이터 삽입  
            data = [[today, '0', str(price), '0', '0', '0', '0', '0', '0']]  
            insert_query = query_update_oilprice(data)  
            db.setter(insert_query)  
            
            print(f"Successfully updated oil price: {price} for date: {today}")  
            
            # 데이터베이스 연결 종료  
            db.close()  
        else:  
            print("Price element not found")  
            
    except Exception as e:  
        print(f"Error processing data: {e}")  

if __name__ == "__main__":  
    import os  
    from dotenv import load_dotenv  

    # .env 파일 로드  
    load_dotenv(override=True)  
    
   # .env 파일 로드  
    load_dotenv()  
    
    dbinfo = {  
        "host": os.environ.get('DB_HOST'),  
        "port": int(os.environ.get('DB_PORT')),  
        "user": os.environ.get('DB_USER'),  
        "password": os.environ.get('DB_PASSWORD'),  
        "database": os.environ.get('DB_NAME')  
    }  
    get_oilprice_now(dbinfo)