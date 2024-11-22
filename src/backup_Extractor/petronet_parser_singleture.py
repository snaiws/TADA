from selenium.webdriver.common.by import By  
import time  

def extract_table_data(driver):  
    """테이블 데이터 추출"""  
    table = driver.find_element(By.XPATH, '//*[@id="csvExportTable0"]')  
    
    # 헤더 추출  
    headers = []  
    header_rows = table.find_elements(By.TAG_NAME, "th")  
    for header in header_rows:  
        headers.append(header.text.strip())  
    
    # 데이터 행 추출  
    rows = table.find_elements(By.TAG_NAME, "tr")  
    data = []  
    
    for row in rows[1:]:  # 첫 번째 행(헤더)를 제외  
        cols = row.find_elements(By.TAG_NAME, "td")  
        if cols:  
            row_data = []  
            for col in cols:  
                row_data.append(col.text.strip())  
            data.append(row_data)  
    
    return headers, data  

def set_date_and_search(driver, start_date, end_date):  
    """날짜 설정 및 검색 실행"""  
    print(f"\n조회 기간: {start_date.year}.{start_date.month} ~ {end_date.year}.{end_date.month}")  
    
    # 시작 연도 설정  
    start_year = driver.find_element(By.XPATH, '//*[@id="select_days_01"]')  
    start_year.click()  
    start_year_option = driver.find_element(By.XPATH, f'//select[@id="select_days_01"]/option[@value="{start_date.year}"]')  
    start_year_option.click()  
    
    # 시작 월 설정  
    start_month = driver.find_element(By.XPATH, '//*[@id="select_days_03"]')  
    start_month.click()  
    start_month_option = driver.find_element(By.XPATH, f'//select[@id="select_days_03"]/option[@value="{start_date.month:02d}"]')  
    start_month_option.click()  
    
    # 마지막 연도 설정  
    end_year = driver.find_element(By.XPATH, '//*[@id="select_days_04"]')  
    end_year.click()  
    end_year_option = driver.find_element(By.XPATH, f'//select[@id="select_days_04"]/option[@value="{end_date.year}"]')  
    end_year_option.click()  
    
    # 마지막 월 설정  
    end_month = driver.find_element(By.XPATH, '//*[@id="select_days_06"]')  
    end_month.click()  
    end_month_option = driver.find_element(By.XPATH, f'//select[@id="select_days_06"]/option[@value="{end_date.month:02d}"]')  
    end_month_option.click()  
    
    time.sleep(1)  
    
    # 조회 버튼 클릭  
    search_button = driver.find_element(By.XPATH, '//*[@id="contents"]/fieldset/form/table/tbody/tr[4]/td/p/a/img')  
    driver.execute_script("arguments[0].click();", search_button)  
    
    time.sleep(3)