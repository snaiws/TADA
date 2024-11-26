#!/bin/bash  

# 작업 디렉토리로 이동  
cd /app  

# venv 환경 생성 (없는 경우에만)  
if [ ! -d "venv" ]; then  
    python -m venv venv  
fi  

# venv 활성화  
source venv/bin/activate  

pip install --upgrade pip

# 프로젝트 requirements 설치  
pip install -r requirements.txt  

# 패키지 설치  
pip install -r Extractor/requirements.txt  

# 파이썬 스크립트 실행 (oil_scheduler.py 예시)  
python oil_scheduler.py  

# 프로세스가 계속 실행되도록 유지  
tail -f /dev/null