from flask import Blueprint, render_template



main_bp = Blueprint('main', __name__)

# 로그인 페이지
@main_bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')