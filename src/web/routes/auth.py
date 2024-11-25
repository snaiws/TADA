from flask import Blueprint, request, redirect, url_for, render_template, session

from loguru import logger



auth_bp = Blueprint('auth', __name__)


# 로그인 페이지
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session.clear()
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 인증 로직 추가(유저DB)###################
        if username == 'test' and password == 'password':  # 예시
            session['user'] = username
            return redirect(url_for('main.main')) # 수정
        return "Invalid credentials", 401


# 쿠키 인증 확인
@auth_bp.before_app_request
def check_login():
    allowed_routes = ['auth.login']
    if request.endpoint and request.endpoint.startswith('static'):  # 정적 파일 요청 무시
        return
    if request.endpoint in allowed_routes:
        return
    if 'user' not in session:
        return redirect(url_for('auth.login'))