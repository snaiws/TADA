from selenium.webdriver.common.by import By  
import time  

def extract_table_data(driver, current_start_date):  
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
    current_year = current_start_date.year  # 검색 시작 연도로 초기화  
    
    for row in rows[1:]:  # 첫 번째 행(헤더)를 제외  
        cols = row.find_elements(By.TAG_NAME, "td")  
        if cols:  
            row_data = []  
            for idx, col in enumerate(cols):  
                value = col.text.strip()  
                
                # 첫 번째 컬럼(날짜) 처리  
                if idx == 0:  
                    # "년" 문자가 있는 경우 (예: "09년 01월")  
                    if "년" in value:  
                        year_str = value.split("년")[0]  
                        month_str = value.split("월")[0][-2:]  
                        current_year = 2000 + int(year_str)  # 2000년대로 가정  
                    else:  
                        # 월만 있는 경우 (예: "06월")  
                        month_str = value.split("월")[0]  
                    
                    # 날짜 형식으로 변환  
                    date_str = f"{current_year}-{month_str.zfill(2)}-01"  
                    row_data.append(date_str)  
                else:  
                    row_data.append(value)  
            
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