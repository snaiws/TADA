import pkg_resources  
from dotenv import load_dotenv, find_dotenv  
import os  
from pathlib import Path  

# 버전 확인  
dotenv_version = pkg_resources.get_distribution('python-dotenv').version  
print(f"python-dotenv version: {dotenv_version}")  

# dotenv 상세 디버깅  
env_path = find_dotenv()  
print(f"\nFound .env at: {env_path}")  

# 현재 환경변수 상태 출력  
print("\nBefore loading - Current environment variables:")  
for key in ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']:  
    print(f"{key}: {os.environ.get(key, 'not set')}")  

# load_dotenv 실행 시 override 옵션 추가  
print("\nLoading with load_dotenv...")  
result = load_dotenv(override=True, verbose=True)  
print(f"load_dotenv result: {result}")  

# 로드 후 환경변수 상태 출력  
print("\nAfter loading - Environment variables:")  
for key in ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']:  
    print(f"{key}: {os.environ.get(key, 'not set')}")  

# 파일 내용 직접 확인  
print("\nDirect file content check:")  
with open('.env', 'rb') as f:  # 바이너리 모드로 열어서 확인  
    content = f.read()  
    print(f"Raw content (hex):", content.hex())  
    print(f"Raw content (str):", content)