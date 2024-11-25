import os

from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './upload'  # 업로드 폴더 경로
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

upload_bp = Blueprint('upload', __name__)



# 업로드 페이지
@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # 오브젝트 스토리지 등록 추가 필요 ###################

        return f"File {filename} uploaded successfully!"
    return render_template('upload.html')


def get_folder_size(folder_path):
    """
    폴더의 총 크기를 계산

    Args:
        folder_path (str): 폴더 경로

    Returns:
        int: 폴더 크기 (바이트 단위)
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def cleanup_large_folder(folder_path, max_folder_size_in_bytes):
    """
    폴더 크기가 제한을 초과하면 오래된 파일부터 삭제

    Args:
        folder_path (str): 폴더 경로
        max_folder_size_in_bytes (int): 폴더 최대 크기 (바이트 단위)
    """
    if get_folder_size(folder_path) <= max_folder_size_in_bytes:
        return  # 제한 이하인 경우 종료

    # 파일 목록을 수정 시간 기준으로 정렬
    files = sorted(
        (os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))),
        key=os.path.getmtime
    )

    for file_path in files:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
        if get_folder_size(folder_path) <= max_folder_size_in_bytes:
            break


