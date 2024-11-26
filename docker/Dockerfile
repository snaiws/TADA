FROM python:3.12-slim  

WORKDIR /app  

# Chrome 및 필요한 패키지 설치  
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    curl \
    unzip \
    xvfb \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*  

# ChromeDriver 설치 (Chrome 버전과 일치하는 버전 사용)  
RUN CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | cut -d "." -f1) \
    && echo "Chrome Version: $CHROME_VERSION" \
    && wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/131.0.6778.85/linux64/chromedriver-linux64.zip -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/*  

# 환경변수 설정  
ENV PYTHONUNBUFFERED=1  
ENV DISPLAY=:99  
ENV DOCKER_ENV=true  
ENV CHROME_DRIVER_PATH=/usr/local/bin/chromedriver  

# 스크립트 생성  
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &\n\
\n\
# pip 업그레이드\n\
pip install --upgrade pip\n\
\n\
# 프로젝트 requirements 설치\n\
pip install -r requirements.txt\n\
\n\
# Extractor 폴더의 requirements 설치\n\
cd Extractor && pip install -r requirements.txt && cd ..\n\
\n\
# 파이썬 스크립트 실행\n\
python oil_scheduler.py\n\
\n\
# 프로세스 유지\n\
tail -f /dev/null' > /app/extractor.sh  

RUN chmod +x /app/extractor.sh  

CMD ["/app/extractor.sh"]