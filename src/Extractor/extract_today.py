from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from datetime import datetime  
from loader.db.connector import Database  
from loader.db.query import query_creat_table_daily_oil, query_update_daily_oilprice  

def get_oilprice_now(dbinfo):  
    options = webdriver.ChromeOptions()  
    options.add_argument('--headless')  
    options.add_argument('--no-sandbox')  
    options.add_argument('--disable-dev-shm-usage')  

    try:  
        # WebDriver 초기화  
        driver = webdriver.Chrome(options=options)  
        
        # 페이지 로드  
        url = 'https://www.opinet.co.kr/user/main/mainView.do'  
        driver.get(url)  
        
        # 요소가 로드될 때까지 대기 (최대 10초)  
        wait = WebDriverWait(driver, 10)  
        price_element = wait.until(  
            EC.presence_of_element_located((By.XPATH, '//*[@id="oilcon1"]/div/dl[1]/dd/span[1]'))  
        )  
        
        if price_element:  
            price = float(price_element.text.replace(',', ''))  
            print(f"Found price: {price}")  
            
            # 데이터베이스 연결  
            db = Database(  
                host=dbinfo["host"],  
                port=dbinfo["port"],  
                user=dbinfo["user"],  
                password=dbinfo["password"],  
                database=dbinfo["database"]  
            )  
            
            # 테이블 생성 확인  
            db.setter(query_creat_table_daily_oil())  
            
            # 현재 날짜  
            today = datetime.now().strftime('%Y-%m-%d')  
            
            # 데이터 삽입 (날짜와 가격만 전달)  
            data = [today, price]  
            insert_query = query_update_daily_oilprice(data)  
            db.setter(insert_query)  
            
            print(f"Successfully updated daily oil price: {price} for date: {today}")  
            
            # 데이터베이스 연결 종료  
            db.close()  
            
        else:  
            print("Price element not found")  
            
    except Exception as e:  
        print(f"Error processing data: {e}")  
        
    finally:  
        # 브라우저 종료  
        driver.quit()  

if __name__ == "__main__":  
    import os  
    from dotenv import load_dotenv  
    
    load_dotenv(override=True)  
    
    dbinfo = {  
        "host": os.environ.get('DB_HOST'),  
        "port": int(os.environ.get('DB_PORT')),  
        "user": os.environ.get('DB_USER'),  
        "password": os.environ.get('DB_PASSWORD'),  
        "database": os.environ.get('DB_NAME')  
    }  
    
    get_oilprice_now(dbinfo)