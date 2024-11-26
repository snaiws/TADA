
import os  
from dotenv import load_dotenv  
from dotenv import dotenv_values

from pathlib import Path

from data_engineering.db.connector import Database  


def create_object_storage_table():  
    #load_dotenv()  
    
    env_path = Path(__file__).parent.parent.parent / '.env'  
    print(f"\n.env 파일 경로: {env_path}")  
    print(f"파일 존재 여부: {env_path.exists()}")  
    print(f"절대 경로: {env_path.absolute()}\n")  

    #oad_dotenv(env_path)

    env_path = Path(__file__).parent.parent.parent / '.env'  
    
    # dotenv_values 사용  
    config = dotenv_values(env_path)  
    print("\n=== dotenv_values 결과 ===")  
    print(config)  
    
    # 직접 환경변수 설정  
    for key, value in config.items():  
        os.environ[key] = value  



    # 디버깅용 출력  
    print("Environment variables:")  
    print(f"DB_HOST: {os.getenv('DB_HOST')}")  
    print(f"DB_PORT: {os.getenv('DB_PORT')}")  
    print(f"DB_USER: {os.getenv('DB_USER')}")  
    print(f"DB_NAME: {os.getenv('DB_NAME')}")  
    print(f"PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', ''))}")  

    db = Database(  
        host=os.getenv('DB_HOST'),  
        port=int(os.getenv('DB_PORT')),  
        user=os.getenv('DB_USER'),  
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME')  
    )  
    
    create_table_query = """  
    CREATE TABLE IF NOT EXISTS object_storage (  
        id_os INT AUTO_INCREMENT PRIMARY KEY,  
        category VARCHAR(255) NOT NULL,  
        bucket_name VARCHAR(255) NOT NULL,  
        object_path TEXT NOT NULL,  
        file_name VARCHAR(255) NOT NULL,  
        ext VARCHAR(10) NOT NULL,  
        size BIGINT NOT NULL,  
        version VARCHAR(50) DEFAULT NULL,  
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;  
    """  
    
    try:  
        db.setter(create_table_query)  
        print("object_storage 테이블이 성공적으로 생성되었습니다.")  
        return True  
    except Exception as e:  
        print(f"테이블 생성 실패: {str(e)}")  
        return False  

if __name__ == "__main__":  
    create_object_storage_table()