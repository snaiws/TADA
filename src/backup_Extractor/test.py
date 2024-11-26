from datetime import datetime  
from dateutil.relativedelta import relativedelta  
import time  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

from core.selenium import setup_driver, handle_popups  
from parser.petronet_parser import extract_table_data, set_date_and_search  
from loader.db import DatabaseLoader  



# 테스트 코드  
loader1 = DatabaseLoader()  
loader2 = DatabaseLoader()  
print(loader1 is loader2)  # True가 출력되어야 함