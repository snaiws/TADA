import os  
from pathlib import Path

from dotenv import load_dotenv  

from data_engineering.db.connector import Database  



def create_object_storage_table():  
    #load_dotenv()  
    load_dotenv(Path(__file__).parent.parent / '.env')

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