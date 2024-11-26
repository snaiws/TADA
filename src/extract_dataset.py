import os  
import zipfile  
from tqdm.notebook import tqdm  

# 설정  
DATASET_PATH = "G:/Dropbox/OssmMath/52_AI-Project/DataSet"  
EXTRACT_PATH = "G:/Dropbox/OssmMath/52_AI-Project/ExtractedDataSet"  # 압축 해제될 경로  

# 처리할 디렉토리 구조  
DIRECTORIES = [  
    "Training/01.원천데이터",  
    "Training/02.라벨링데이터",  
    "Validation/01.원천데이터",  
    "Validation/02.라벨링데이터"  
]  

def extract_all_zips():  
    """모든 ZIP 파일을 미리 압축 해제"""  
    total_files = 0  
    extracted_files = 0  
    
    # 전체 ZIP 파일 수 계산  
    for dir_path in DIRECTORIES:  
        current_path = os.path.join(DATASET_PATH, dir_path)  
        zip_files = [f for f in os.listdir(current_path) if f.endswith('.zip')]  
        total_files += len(zip_files)  
    
    print(f"총 처리할 ZIP 파일 수: {total_files}")  
    
    for dir_path in DIRECTORIES:  
        current_path = os.path.join(DATASET_PATH, dir_path)  
        extract_path = os.path.join(EXTRACT_PATH, dir_path)  
        
        # 추출 디렉토리 생성  
        os.makedirs(extract_path, exist_ok=True)  
        
        # ZIP 파일 목록 가져오기  
        zip_files = [f for f in os.listdir(current_path) if f.endswith('.zip')]  
        
        for zip_filename in tqdm(zip_files, desc=f"압축 해제 중: {dir_path}"):  
            zip_path = os.path.join(current_path, zip_filename)  
            category_path = os.path.join(extract_path, os.path.splitext(zip_filename)[0])  
            
            # 이미 압축 해제된 경우 스킵  
            if os.path.exists(category_path):  
                print(f"이미 압축 해제됨: {category_path}")  
                extracted_files += 1  
                continue  
                
            try:  
                os.makedirs(category_path, exist_ok=True)  
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
                    total_members = len(zip_ref.namelist())  
                    print(f"\n{zip_filename} 압축 해제 중 (총 {total_members}개 파일)")  
                    zip_ref.extractall(category_path)  
                extracted_files += 1  
                print(f"압축 해제 완료: {category_path}")  
            except Exception as e:  
                print(f"오류 발생 ({zip_filename}): {str(e)}")  
    
    print(f"\n압축 해제 완료: {extracted_files}/{total_files} 파일 처리됨")  
    
    # 추출된 파일 통계  
    total_extracted = 0  
    for dir_path in DIRECTORIES:  
        extract_path = os.path.join(EXTRACT_PATH, dir_path)  
        for root, _, files in os.walk(extract_path):  
            total_extracted += len(files)  
    
    print(f"총 추출된 파일 수: {total_extracted}")  

if __name__ == "__main__":  
    extract_all_zips()