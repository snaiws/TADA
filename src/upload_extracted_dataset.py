import os  
import concurrent.futures  
from tqdm.notebook import tqdm  
from dotenv import load_dotenv  
import multiprocessing  

from data_engineering.obj_storage.connector import MinIOClient  
from data_engineering.update_objectfile import upload_file_with_metadata  
from data_engineering.db.connector import Database  
from data_engineering.setting_DB import create_object_storage_table  



def get_uploaded_files():  
    """DB에서 이미 업로드된 파일 목록 가져오기"""  
    db = Database(  
        host=os.getenv('DB_HOST'),  
        port=int(os.getenv('DB_PORT')),  
        user=os.getenv('DB_USER'),  
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME')  
    )  
    
    query = "SELECT category, object_path FROM object_storage"  
    results = db.getter(query)  
    return {(record['category'], record['object_path']) for record in results}  


def upload_file(args):  
    """단일 파일 업로드 함수"""  
    file_path, category, object_key = args  
    try:  
        success = upload_file_with_metadata(  
            local_path=file_path,  
            category=category,  
            bucket=BUCKET_NAME,  
            object_path=object_key  
        )  
        return success, object_key  
    except Exception as e:  
        return False, f"Error uploading {object_key}: {str(e)}"  


def main():  
    # MinIO 클라이언트 초기화 및 버킷 확인  
    minio_client = MinIOClient()  
    if not minio_client.check_bucket_exists(BUCKET_NAME):  
        minio_client.create_bucket(BUCKET_NAME)  
        print(f"버킷 '{BUCKET_NAME}' 생성됨")  
    
    # DB 테이블 생성 확인  
    create_object_storage_table()  
    
    # 이미 업로드된 파일 목록 가져오기  
    uploaded_files = get_uploaded_files()  
    print(f"이미 업로드된 파일 수: {len(uploaded_files)}")  
    
    # 업로드할 파일 목록 생성  
    upload_tasks = []  
    for dir_path in DIRECTORIES:  
        extract_base = os.path.join(EXTRACT_PATH, dir_path)  
        if not os.path.exists(extract_base):  
            print(f"경로를 찾을 수 없음: {extract_base}")  
            continue  
            
        for root, _, files in os.walk(extract_base):  
            category_name = os.path.relpath(root, extract_base)  
            if category_name == '.':  
                category_name = ''  
            
            for filename in files:  
                if any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):  
                    file_path = os.path.join(root, filename)  
                    category = f"{dir_path}/{category_name}".rstrip('/')  
                    object_key = f"{category}/{filename}"  
                    
                    # 이미 업로드된 파일 제외  
                    if (category, object_key) not in uploaded_files:  
                        upload_tasks.append((file_path, category, object_key))  
    
    print(f"업로드할 총 파일 수: {len(upload_tasks)}")  
    
    # 병렬 업로드 실행  
    successful_uploads = 0  
    failed_uploads = 0  
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:  
        futures = [executor.submit(upload_file, task) for task in upload_tasks]  
        
        for future in tqdm(concurrent.futures.as_completed(futures),   
                         total=len(futures),   
                         desc="파일 업로드 중"):  
            success, result = future.result()  
            if success:  
                successful_uploads += 1  
            else:  
                failed_uploads += 1  
                print(result)  
    
    print(f"\n업로드 완료:")  
    print(f"성공: {successful_uploads}")  
    print(f"실패: {failed_uploads}")  
    
    # 최종 통계 출력  
    db = Database(  
        host=os.getenv('DB_HOST'),  
        port=int(os.getenv('DB_PORT')),  
        user=os.getenv('DB_USER'),  
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME')  
    )  
    
    query = """  
    SELECT category, COUNT(*) as count   
    FROM object_storage   
    GROUP BY category   
    ORDER BY count DESC  
    """  
    records = db.getter(query)  
    print("\n카테고리별 파일 수:")  
    for record in records:  
        print(f"- {record['category']}: {record['count']}개")  



if __name__ == "__main__":  
    # 환경 변수 로드  
    load_dotenv('.env')  
    # 설정  
    BUCKET_NAME = "tada"  
    EXTRACT_PATH = "../../IMG_upload/extracted_data"  
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}  
    MAX_WORKERS = multiprocessing.cpu_count()  # CPU 코어 수만큼 워커 설정  

    # 처리할 디렉토리 구조  
    DIRECTORIES = [  
        "Training/01.원천데이터",  
        "Training/02.라벨링데이터",  
        "Validation/01.원천데이터",  
        "Validation/02.라벨링데이터"  
    ]  
    main()