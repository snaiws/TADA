from functools import wraps  

import boto3
from botocore.client import Config  
from botocore.exceptions import ClientError  



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
    def __init__(self, endpoint_url, aws_access_key_id, aws_secret_access_key, region_name):  
        self.__endpoint_url = endpoint_url
        self.__aws_access_key_id = aws_access_key_id
        self.__aws_secret_access_key = aws_secret_access_key
        self.__signature_version = 's3v4'
        self.__region_name = region_name
        self.client = None
        self.connect()


    def connect(self):
        self.client = boto3.client(  
            's3',  
            endpoint_url = self.__endpoint_url,  
            aws_access_key_id = self.__aws_access_key_id,  
            aws_secret_access_key = self.__aws_secret_access_key,  
            config = Config(signature_version = self.__signature_version),  
            region_name = self.__region_name  
        )  


    def check_bucket_exists(self, bucket_name: str) -> bool:  
        """버킷 존재 여부 확인"""  
        try:  
            self.client.head_bucket(Bucket=bucket_name)  
            return True  
        except ClientError as e:
            print(e)
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
    

    def upload_file(self, bucket: str, local_path: str, object_path: str) -> bool:  
        """파일 업로드"""  
        try:  
            if not self.ensure_bucket_exists(bucket):  
                raise Exception(f"버킷 '{bucket}' 생성/확인 실패")  
            
            self.client.upload_file(local_path, bucket, object_path)  
            return True  
        except Exception as e:  
            print(f"Upload error: {str(e)}")  
            return False  
        
    
    def download_file(self, bucket: str, local_path: str, object_path: str) -> bool:  
        """파일 다운로드"""  
        try:  
            self.client.download_file(bucket, object_path, local_path)  
            return True  
        except Exception as e:  
            print(f"Download error: {str(e)}")  
            return False
        

if __name__ == "__main__":
    import os  

    from dotenv import load_dotenv  
    load_dotenv(verbose = False)
    
    kwargs = {
        "endpoint_url" : os.getenv('MINIO_ENDPOINT'),
        "aws_access_key_id" : os.getenv('MINIO_ACCESS_KEY'),
        "aws_secret_access_key" : os.getenv('MINIO_SECRET_KEY'),
        "region_name" : os.getenv('MINIO_REGION', 'us-east-1')  
    }
    object_storage = MinIOClient(**kwargs)

    print(object_storage.check_bucket_exists('tada'))