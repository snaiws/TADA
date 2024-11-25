import os  

from dotenv import load_dotenv  

from .obj_storage.connector import MinIOClient
from .db.connector import Database  
from .insert_object_metadata import insert_file_metadata  



def upload_file_with_metadata(local_path: str, category: str, bucket: str,   
                            object_path: str = None) -> bool:  
    """파일 업로드 및 메타데이터 저장"""  
    try:  
        load_dotenv()

        # 인증
        configs_minio = {
            "endpoint_url" : os.getenv('MINIO_ENDPOINT'),
            "aws_access_key_id" : os.getenv('MINIO_ACCESS_KEY'),
            "aws_secret_access_key" : os.getenv('MINIO_SECRET_KEY'),
            "region_name" : os.getenv('MINIO_REGION', 'us-east-1')  
        }
        
        configs_minio = {
            "host" : os.getenv('DB_HOST'),
            "port" : os.getenv('DB_PORT'),
            "user" : os.getenv('DB_USER'),
            "password" : os.getenv('DB_PASSWORD'),
            "database" : os.getenv('DB_NAME'),
        }

        minio_client = MinIOClient(**configs_minio)  
        db = Database(**configs_minio)  


        # object_path가 지정되지 않은 경우 파일명 사용  
        if object_path is None:  
            object_path = os.path.basename(local_path)  
        
        # 파일 업로드  
        if not minio_client.upload_file(local_path, bucket, object_path):  
            return False  
        
        # 메타데이터 DB 저장  
        if not insert_file_metadata(db, local_path, category, bucket, object_path):  
            return False  
            
        return True  
        
    except Exception as e:  
        print(f"Upload and metadata update error: {str(e)}")  
        return False