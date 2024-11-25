from flask import Flask, render_template, request, redirect, url_for
from loguru import logger

from web.routes.main import main_bp
from web.routes.auth import auth_bp
from web.routes.datasets import datasets_bp
from web.routes.upload import upload_bp, cleanup_large_folder
from web.routes.text2sql import text2sql_bp


app = Flask(
    __name__,
    template_folder="web/templates",  # 템플릿 디렉토리 경로
    static_folder="web/static"      # 정적 파일 디렉토리 경로
)

app.secret_key = 'your_secret_key'  # 랜덤 문자열로 설정

app.register_blueprint(main_bp, url_prefix='/main')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(datasets_bp, url_prefix='/datasets')
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(text2sql_bp, url_prefix='/text2sql')

with app.app_context():
    cleanup_large_folder('upload', max_folder_size_in_bytes=100 * 1024 * 1024)  # 100MB

if __name__ == "__main__":
    logger.add("app.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip")
    app.run(debug=True)
    

