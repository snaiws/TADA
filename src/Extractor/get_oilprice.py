from datetime import datetime  
from dateutil.relativedelta import relativedelta  
import time  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

from core.selenium import setup_driver, handle_popups  
from parser.petronet_parser import extract_table_data, set_date_and_search  
from loader.db import DatabaseLoader  

def main():  
    driver = None  
    db_loader = None  
    try:  
        driver = setup_driver()  
        db_loader = DatabaseLoader()  

        print("메인 페이지 접속...")  
        driver.get("https://www.petronet.co.kr")  

        handle_popups(driver)  

        wait = WebDriverWait(driver, 5)  
        menu = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='국내가격총괄']")))  
        driver.execute_script("arguments[0].click();", menu)  
        time.sleep(2)  

        driver.switch_to.frame("left")  
        sidebar_menu = driver.find_element(By.XPATH, "//*[@id='img01_2']")  
        driver.execute_script("arguments[0].click();", sidebar_menu)  
        driver.switch_to.default_content()  
        driver.switch_to.frame("body")  

        # 날짜 범위 설정 - 현재부터 거꾸로  
        end_date = datetime.now()  
        start_date = datetime(2008, 6, 1)  # 최종 시작일  
        current_end = end_date  
        
        while True:  
            current_start = current_end - relativedelta(months=35)  
            
            # 마지막 구간에서 2008년 6월 이전으로 가면 조정  
            if current_start < start_date:  
                current_start = start_date  
            
            try:  
                print(f"\n처리 기간: {current_start.strftime('%Y-%m')} ~ {current_end.strftime('%Y-%m')}")  
                set_date_and_search(driver, current_start, current_end)  
                
                headers, data = extract_table_data(driver, current_start)  # current_start 전달  
                print(f"추출된 데이터 행 수: {len(data)}")  
            
                # 데이터 저장  
                db_loader.insert_oil_price_data(data, headers)  
                print(f"기간 {current_start.strftime('%Y.%m')} ~ {current_end.strftime('%Y.%m')} 데이터 저장 완료")  

                # 다음 처리할 기간 설정  
                if current_start <= start_date:  
                    break  
                    
                current_end = current_start - relativedelta(days=1)  
                time.sleep(2)  

            except Exception as e:  
                print(f"데이터 추출 중 오류 발생: {str(e)}")  
                break  

        print("\n전체 데이터 수집 완료")  

    except Exception as e:  
        print(f"전체 프로세스 오류: {str(e)}")  

    finally:  
        if db_loader:  
            db_loader.close_connection()  
        if driver:  
            driver.quit()  

if __name__ == "__main__":  
    main()