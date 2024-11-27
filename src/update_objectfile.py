from pathlib import Path

from data_engineering.obj_storage.boto3 import MinIOClient  # 수정된 import 경로  
from data_engineering.db.insert_object_metadata import insert_file_metadata  
from data_engineering.db.connector import Database  
import os  
from dotenv import load_dotenv  

def upload_file_with_metadata(local_path, category, bucket, object_path, db):  
    """파일 업로드 및 메타데이터 저장을 트랜잭션처럼 처리"""  
    try:  
        # 1. DB 트랜잭션 시작  
        db.begin_transaction()  

        # 2. 임시 상태로 DB에 먼저 기록 (status: 'uploading')  
        insert_query = """  
            INSERT INTO object_storage   
            (category, object_path, status, created_at)   
            VALUES (%s, %s, 'uploading', NOW())  
            RETURNING id  
        """  
        result = db.setter(insert_query, (category, object_path))  
        record_id = result[0]['id'] if result else None  

        if not record_id:  
            raise Exception("DB 임시 레코드 생성 실패")  

        # 3. MinIO에 파일 업로드 시도  
        try:  
            file_size = os.path.getsize(local_path)  
            file_extension = os.path.splitext(local_path)[1]  
            
            with open(local_path, 'rb') as file_data:  
                minio_client.put_object(  
                    bucket,  
                    object_path,  
                    file_data,  
                    file_size  
                )  
        except Exception as e:  
            # MinIO 업로드 실패시 DB 롤백  
            db.rollback()  
            raise Exception(f"MinIO 업로드 실패: {str(e)}")  

        # 4. 업로드 성공 시 DB 레코드 업데이트  
        update_query = """  
            UPDATE object_storage   
            SET status = 'completed',  
                file_size = %s,  
                file_extension = %s,  
                updated_at = NOW()  
            WHERE id = %s  
        """  
        db.setter(update_query, (file_size, file_extension, record_id))  

        # 5. 모든 작업이 성공하면 커밋  
        db.commit()  
        return True  

    except Exception as e:  
        # 어떤 단계에서든 실패하면 롤백  
        try:  
            db.rollback()  
            # MinIO에 업로드된 객체가 있다면 삭제  
            if minio_client.exists(bucket, object_path):  
                minio_client.remove_object(bucket, object_path)  
        except:  
            pass  # 롤백 중 발생하는 추가 에러는 무시  
        
        print(f"업로드 실패 ({object_path}): {str(e)}")  
        return False  
