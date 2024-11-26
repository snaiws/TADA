import os  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from datetime import datetime  
from data_engineering.db.connector import Database  
from Extractor.loader.db.query import query_creat_table_daily_oil, query_update_daily_oilprice  
from webdriver_manager.chrome import ChromeDriverManager  
import logging  

# 로깅 설정  
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')  
logger = logging.getLogger(__name__)  

def get_oilprice_now(dbinfo):  
    driver = None  
    db = None  
    
    # Chrome 옵션 설정  
    options = Options()  
    
    # Docker 환경인지 확인  
    is_docker = os.environ.get('DOCKER_ENV', False)  
    
    if is_docker:  
        # Docker 환경에서의 설정  
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox')  
        options.add_argument('--disable-dev-shm-usage')  
        options.add_argument('--disable-gpu')  
        options.add_argument('--window-size=1920,1080')  
        chrome_driver_path = os.environ.get('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')  
        logger.info(f"Using ChromeDriver at: {chrome_driver_path}")  
    else:  
        # 로컬 환경에서의 설정  
        options.add_argument('--start-maximized')  
        chrome_driver_path = ChromeDriverManager().install()  


    try:  
        # WebDriver 초기화  
        logger.info("WebDriver 초기화 시작...")  
        service = Service(executable_path=chrome_driver_path)  
        
        driver = webdriver.Chrome(service=service, options=options)  
        driver.set_page_load_timeout(30)  
        driver.implicitly_wait(20)  
        
        # 페이지 로드  
        logger.info("페이지 로딩 시작...")  
        url = 'https://www.opinet.co.kr/user/main/mainView.do'  
        driver.get(url)  
        
        # 요소가 로드될 때까지 대기  
        logger.info("가격 정보 추출 중...")  
        wait = WebDriverWait(driver, 10)  
        price_element = wait.until(  
            EC.presence_of_element_located((By.XPATH, '//*[@id="oilcon1"]/div/dl[1]/dd/span[1]'))  
        )  
        
        if not price_element:  
            raise Exception("Price element not found")  
            
        price = float(price_element.text.replace(',', ''))  
        logger.info(f"Found price: {price}")  
        
        # 데이터베이스 연결  
        logger.info("데이터베이스 연결 중...")  
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
        
        # 데이터 삽입  
        data = [today, price]  
        insert_query = query_update_daily_oilprice(data)  
        db.setter(insert_query)  
        
        logger.info(f"Successfully updated daily oil price: {price} for date: {today}")  
        return price  
            
    except Exception as e:  
        logger.error(f"Error processing data: {e}")  
        raise e  
        
    finally:  
        # 브라우저 종료  
        if driver:  
            try:  
                driver.quit()  
            except Exception as e:  
                logger.error(f"Error closing browser: {e}")  
                
        # 데이터베이스 연결 종료  
        if db:  
            try:  
                db.close()  
            except Exception as e:  
                logger.error(f"Error closing database connection: {e}")  

if __name__ == "__main__":  
    from dotenv import load_dotenv  
    
    load_dotenv(override=True)  
    
    dbinfo = {  
        "host": os.environ.get('DB_HOST'),  
        "port": int(os.environ.get('DB_PORT')),  
        "user": os.environ.get('DB_USER'),  
        "password": os.environ.get('DB_PASSWORD'),  
        "database": os.environ.get('DB_NAME')  
    }  
    
    try:  
        get_oilprice_now(dbinfo)  
    except Exception as e:  
        logger.error(f"프로그램 실행 중 오류 발생: {e}")