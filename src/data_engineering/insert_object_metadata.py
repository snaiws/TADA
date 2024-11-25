import os  
from typing import Tuple  

from .db.connector import Database  



def get_file_metadata(local_path: str, category: str, bucket_name: str, object_path: str) -> Tuple:  
    """파일 메타데이터 추출"""  
    file_stats = os.stat(local_path)  
    file_name = os.path.basename(local_path)  
    file_ext = os.path.splitext(file_name)[1][1:]  
    
    return (  
        category,  
        bucket_name,  
        object_path,  
        file_name,  
        file_ext,  
        file_stats.st_size,  
        "1.0"  # 초기 버전  
    )  

def insert_file_metadata(db: Database, local_path: str, category: str,   
                        bucket_name: str, object_path: str) -> bool:  
    """DB에 파일 메타데이터 삽입"""  
    try:  
        metadata = get_file_metadata(local_path, category, bucket_name, object_path)  
        
        query = """  
        INSERT INTO object_storage   
        (category, bucket_name, object_path, file_name, ext, size, version)  
        VALUES (%s, %s, %s, %s, %s, %s, %s)  
        """  
        
        db.setter(query, metadata)  
        return True  
        
    except Exception as e:  
        print(f"Metadata insert error: {str(e)}")  
        return False