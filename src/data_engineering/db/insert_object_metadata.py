import os  
from typing import Tuple  
import sys
from pathlib import Path
from data_engineering.db.connector import Database  

# 프로젝트 루트 경로 추가  
project_root = Path(__file__).parent.parent.parent  
sys.path.append(str(project_root)) 


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


        print("\nDebug Info:")  
        print(f"local_path: {local_path}")  
        print(f"Metadata values:")  
        print(f"- category: {metadata[0]}")  
        print(f"- bucket_name: {metadata[1]}")  
        print(f"- object_path: {metadata[2]}")  
        print(f"- file_name: {metadata[3]}")  
        print(f"- ext: {metadata[4]}")  
        print(f"- size: {metadata[5]}")  
        print(f"- version: {metadata[6]}")  

        
        query = """  
        INSERT INTO object_storage   
        (category, bucket_name, object_path, file_name, ext, size, version)  
        VALUES (%s, %s, %s, %s, %s, %s, %s)  
        """  
        
        db.setter(query, metadata)  
        return True  
        
    except Exception as e:  
        print(f"\nError Details:")  
        print(f"Error type: {type(e)}")  
        print(f"Error message: {str(e)}")  
        if hasattr(e, 'args'):  
            print(f"Error args: {e.args}")  
        return False 