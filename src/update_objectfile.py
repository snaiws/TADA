from pathlib import Path

from data_engineering.obj_storage.boto3 import MinIOClient  # 수정된 import 경로  
from data_engineering.db.insert_object_metadata import insert_file_metadata  
from data_engineering.db.connector import Database  
import os  
from dotenv import load_dotenv  

def upload_file_with_metadata(local_path: str, category: str, bucket: str,   
                            object_path: str = None) -> bool:  
    """파일 업로드 및 메타데이터 저장"""  
    try:  
        # MinIO 클라이언트 초기화 (싱글톤)  
        minio_client = MinIOClient()  
        
        # object_path가 지정되지 않은 경우 파일명 사용  
        if object_path is None:  
            object_path = os.path.basename(local_path)  
        
        # 파일 업로드  
        if not minio_client.upload_file(local_path, bucket, object_path):  
            return False  
        
        # DB 연결 (싱글톤)  
        #load_dotenv()  
        load_dotenv(Path(__file__).parent / '.env')
        
        db = Database(  
            host=os.getenv('DB_HOST'),  
            port=int(os.getenv('DB_PORT')),  
            user=os.getenv('DB_USER'),  
            password=os.getenv('DB_PASSWORD'),  
            database=os.getenv('DB_NAME')  
        )  
        
        # 메타데이터 DB 저장  
        if not insert_file_metadata(db, local_path, category, bucket, object_path):  
            return False  
            
        return True  
        
    except Exception as e:  
        print(f"Upload and metadata update error: {str(e)}")  
        return False