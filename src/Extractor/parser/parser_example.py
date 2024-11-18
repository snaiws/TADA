from selenium.webdriver.common.by import By

def get_headlines_naver_it(driver, url):
    # 데이터 저장을 위한 리스트 초기화
    news = []

    # news
    driver.get(url)

    # 더보기 있으면 클릭
    button_more = driver.find_elements(By.XPATH, "//*[@id='newsct']/div[1]/div[2]/a")
    if button_more:
        button_more[0].click()
        # time.sleep(0.5)

    # elements마다
    headlines = driver.find_elements(By.CSS_SELECTOR, "li.sa_item._SECTION_HEADLINE")
    for headline in headlines:
        element = headline.find_element(By.CSS_SELECTOR, "a.sa_text_title._NLOG_IMPRESSION")
        url = element.get_attribute("href")
        news.append(url)

    return news