import os  
from pathlib import Path

import boto3  
from botocore.client import Config  
from botocore.exceptions import ClientError  
import os  
from dotenv import load_dotenv  
from functools import wraps  

def singleton(cls):  
    instances = {}  
    
    @wraps(cls)  
    def get_instance(*args, **kwargs):  
        if cls not in instances:  
            instances[cls] = cls(*args, **kwargs)  
        return instances[cls]  
    
    return get_instance  

@singleton  
class MinIOClient:  
    def __init__(self):  
        # .env 파일 로드  
        #load_dotenv()  
        load_dotenv(Path(__file__).parent.parent / '.env')
        
        self.client = boto3.client(  
            's3',  
            endpoint_url=os.getenv('MINIO_ENDPOINT'),  
            aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),  
            aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),  
            config=Config(signature_version='s3v4'),  
            region_name=os.getenv('MINIO_REGION', 'us-east-1')  
        )  
    
    def check_bucket_exists(self, bucket_name: str) -> bool:  
        """버킷 존재 여부 확인"""  
        try:  
            self.client.head_bucket(Bucket=bucket_name)  
            return True  
        except ClientError:  
            return False  
    
    def create_bucket(self, bucket_name: str) -> bool:  
        """버킷 생성"""  
        try:  
            self.client.create_bucket(Bucket=bucket_name)  
            return True  
        except ClientError as e:  
            print(f"버킷 생성 실패: {str(e)}")  
            return False  
    
    def ensure_bucket_exists(self, bucket_name: str) -> bool:  
        """버킷이 없으면 생성"""  
        if not self.check_bucket_exists(bucket_name):  
            return self.create_bucket(bucket_name)  
        return True  
    
    def upload_file(self, local_path: str, bucket: str, object_path: str) -> bool:  
        """파일 업로드"""  
        try:  
            if not self.ensure_bucket_exists(bucket):  
                raise Exception(f"버킷 '{bucket}' 생성/확인 실패")  
            
            self.client.upload_file(local_path, bucket, object_path)  
            return True  
        except Exception as e:  
            print(f"Upload error: {str(e)}")  
            return False  
    
    def download_file(self, bucket: str, object_path: str, local_path: str) -> bool:  
        """파일 다운로드"""  
        try:  
            self.client.download_file(bucket, object_path, local_path)  
            return True  
        except Exception as e:  
            print(f"Download error: {str(e)}")  
            return False