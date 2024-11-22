import sys  
import os  
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.jobstores.base import JobLookupError  
from datetime import datetime  
from dotenv import load_dotenv  

# Extractor 폴더 경로를 시스템 경로에 추가  
current_dir = os.path.dirname(os.path.abspath(__file__))  
extractor_path = os.path.join(current_dir, 'Extractor')  
sys.path.append(extractor_path)  

from extract_today import get_oilprice_now  

# 전역 설정 변수들  
JOB_ID = 'daily_oil_price_job'  # 작업 식별자  
SCHEDULE_INTERVAL = 5  # 테스트용: 5분 간격  
# 운영용 설정  
# SCHEDULE_TYPE = 'daily'  # 실행 타입: 'interval' 또는 'daily'  
# SCHEDULE_TIME = '09:00'  # 매일 실행할 시각 (24시간 형식)  

# oil_scheduler.py 수정  
def init_db_info():  
    """데이터베이스 연결 정보 초기화"""  
    # Extractor 폴더 내의 .env 파일 경로를 명시적으로 지정  
    env_path = os.path.join(extractor_path, '.env')  
    load_dotenv(env_path, override=True)  
    
    return {  
        "host": os.environ.get('DB_HOST'),  
        "port": int(os.environ.get('DB_PORT')),  
        "user": os.environ.get('DB_USER'),  
        "password": os.environ.get('DB_PASSWORD'),  
        "database": os.environ.get('DB_NAME')  
    }

def schedule_job():  
    """실제 실행될 작업"""  
    print(f"\n[{datetime.now()}] 유가 정보 수집 시작...")  
    try:  
        dbinfo = init_db_info()  
        get_oilprice_now(dbinfo)  
        print(f"[{datetime.now()}] 유가 정보 수집 완료")  
    except Exception as e:  
        print(f"[{datetime.now()}] 오류 발생: {str(e)}")  

def create_scheduler():  
    """스케줄러 생성 및 설정"""  
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')  
    
    # 기존 작업이 있다면 제거  
    try:  
        scheduler.remove_job(JOB_ID)  
    except JobLookupError:  
        pass  

    # 테스트용 설정 (5분 간격)  
    scheduler.add_job(  
        schedule_job,  
        'interval',  
        minutes=SCHEDULE_INTERVAL,  
        id=JOB_ID  
    )  
    
    # 운영용 설정 (매일 특정 시각)  
    # if SCHEDULE_TYPE == 'daily':  
    #     hour, minute = map(int, SCHEDULE_TIME.split(':'))  
    #     scheduler.add_job(  
    #         schedule_job,  
    #         'interval',  
    #         days=1,  
    #         start_date=datetime.now().replace(  
    #             hour=hour,   
    #             minute=minute,   
    #             second=0,   
    #             microsecond=0  
    #         ),  
    #         id=JOB_ID  
    #     )  
    
    return scheduler  

def run_scheduler():  
    """스케줄러 실행"""  
    scheduler = create_scheduler()  
    
    try:  
        print(f"[{datetime.now()}] 스케줄러 시작...")  
        print(f"설정: {SCHEDULE_INTERVAL}분 간격으로 실행")  
        scheduler.start()  
        
        # 프로그램 계속 실행  
        try:  
            while True:  
                pass  
        except KeyboardInterrupt:  
            print("\n스케줄러 종료 요청 감지")  
            scheduler.shutdown()  
            print("스케줄러가 안전하게 종료되었습니다.")  
            
    except Exception as e:  
        print(f"스케줄러 실행 중 오류 발생: {str(e)}")  
        scheduler.shutdown()  

if __name__ == "__main__":  
    run_scheduler()