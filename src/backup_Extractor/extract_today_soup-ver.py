from datetime import datetime  
from bs4 import BeautifulSoup  
from core.soup import get_html  
from loader.db.connector import Database  
from loader.db.query import query_creat_table_oil, query_update_oilprice  

def get_oilprice_now(dbinfo):  
    url = 'https://www.opinet.co.kr/user/main/mainView.do'  
    
    # HTML 가져오기  
    html = get_html(url)  
    if not html:  
        print("Failed to fetch data from website")  
        return  
    
    print("\nReceived HTML content:")  
    print(html[:500])  # 처음 500자만 출력  
    
    soup = BeautifulSoup(html, 'html.parser')  
    
    try:  
        print("\nPage title:", soup.title.text if soup.title else "No title found")  
        print("\nAll div ids found:")  
        for div in soup.find_all('div', id=True):  
            print(f"- {div['id']}")  
            
        price_element = soup.select_one('#oilcon1 > div > dl:nth-child(1) > dd > span.text-3')  
        if price_element:  
            price = float(price_element.text.replace(',', ''))  
            print(f"\nFound price: {price}")  
        else:  
            print("\nPrice element not found")  
            
    except Exception as e:  
        print(f"\nError processing data: {e}")  
        
    print("\nChecking request headers:")  
    print(get_html.headers if hasattr(get_html, 'headers') else "Headers not available")  


if __name__ == "__main__":  
    import os  
    from dotenv import load_dotenv  

    # .env 파일 로드  
    load_dotenv(override=True)  
    
    dbinfo = {  
        "host": os.environ.get('DB_HOST'),  
        "port": int(os.environ.get('DB_PORT')),  
        "user": os.environ.get('DB_USER'),  
        "password": os.environ.get('DB_PASSWORD'),  
        "database": os.environ.get('DB_NAME')  
    }  
    
    get_oilprice_now(dbinfo)