from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os

text2sql_bp = Blueprint('text2sql', __name__)
# 텍스트 입력
@text2sql_bp.route('/', methods=['GET', 'POST'])
def text2sql():
    if request.method == 'POST':
        text = request.form.get('text2sql')
        # text2sql 기능###################

    return render_template('text2sql.html')