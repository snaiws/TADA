import requests  
from bs4 import BeautifulSoup  

def get_html(url):  
    try:  
        headers = {  
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'  
        }  
        response = requests.get(url, headers=headers)  
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생  
        return response.text  
    except requests.RequestException as e:  
        print(f"Error fetching URL: {e}")  
        return None