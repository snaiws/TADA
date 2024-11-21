from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  

def setup_driver():  
    """Chrome WebDriver 설정 및 반환"""  
    chrome_options = Options()  
    chrome_options.add_argument('--start-maximized')  
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  
    chrome_options.add_experimental_option('useAutomationExtension', False)  

    service = Service()  
    driver = webdriver.Chrome(service=service, options=chrome_options)  
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  
    
    return driver  

def handle_popups(driver):  
    """팝업 창 처리"""  
    main_window = driver.current_window_handle  
    for window in driver.window_handles:  
        if window != main_window:  
            driver.switch_to.window(window)  
            driver.close()  
    driver.switch_to.window(main_window)