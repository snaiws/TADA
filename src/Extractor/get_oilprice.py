from datetime import datetime  
from dateutil.relativedelta import relativedelta  
import time  
import csv  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

from core.selenium import setup_driver, handle_popups  
from parser.petronet_parser import extract_table_data, set_date_and_search  

def main():  
    driver = None  
    try:  
        # WebDriver 설정  
        driver = setup_driver()  

        # 웹사이트 접속  
        print("메인 페이지 접속...")  
        driver.get("https://www.petronet.co.kr")  

        # 팝업창 처리  
        handle_popups(driver)  

        # 메인 메뉴 클릭  
        wait = WebDriverWait(driver, 5)  
        menu = wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='국내가격총괄']")))  
        driver.execute_script("arguments[0].click();", menu)  
        time.sleep(2)  

        # 프레임 전환  
        driver.switch_to.frame("left")  
        sidebar_menu = driver.find_element(By.XPATH, "//*[@id='img01_2']")  
        driver.execute_script("arguments[0].click();", sidebar_menu)  
        driver.switch_to.default_content()  
        driver.switch_to.frame("body")  

        # 날짜 범위 설정  
        end_date = datetime.now()  
        start_date = datetime(2007, 6, 1)  
        current_end = end_date  
        current_start = current_end - relativedelta(months=35)  

        # CSV 파일 설정  
        filename = f"petronet_prices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"  
        headers_written = False  

        while current_start >= start_date:  
            try:  
                # 날짜 설정 및 검색  
                set_date_and_search(driver, current_start, current_end)  
                
                # 데이터 추출  
                headers, data = extract_table_data(driver)  
                print(f"추출된 데이터 행 수: {len(data)}")  

                # CSV 파일에 저장  
                mode = 'a' if headers_written else 'w'  
                with open(filename, mode, newline='', encoding='utf-8-sig') as f:  
                    writer = csv.writer(f)  
                    if not headers_written:  
                        writer.writerow(headers)  
                        headers_written = True  
                    writer.writerows(data)  

                print(f"기간 {current_start.year}.{current_start.month} ~ {current_end.year}.{current_end.month} 데이터 저장 완료")  

                # 다음 기간 설정  
                current_end = current_start - relativedelta(months=1)  
                current_start = current_end - relativedelta(months=35)  

                if current_start < start_date:  
                    current_start = start_date  

                time.sleep(2)  

            except Exception as e:  
                print(f"데이터 추출 중 오류 발생: {str(e)}")  
                break  

        print(f"\n전체 데이터 수집 완료. 파일명: {filename}")  

    except Exception as e:  
        print(f"전체 프로세스 오류: {str(e)}")  

    finally:  
        if driver:  
            driver.quit()  

if __name__ == "__main__":  
    main()