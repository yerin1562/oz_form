from flask import Blueprint, render_template, request, redirect, url_for, session 
from flask.views import MethodView
from app.models import Image, Answer, Question, ImageStatus
from config import db

# 블루프린트 정의
index_bp = Blueprint('index', __name__)

# Index 페이지
@index_bp.route('/', methods=['GET'])
def index():
    """
    메인 페이지를 렌더링
    - main 타입의 이미지를 데이터베이스에서 가져옴
    """
    main_image = Image.query.filter_by(id=5).first()
    return render_template('index.html', main_image=main_image)



