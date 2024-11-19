from flask import Blueprint, render_template, request, redirect, url_for, session 
from app.models import Image, Answer, Question, ImageStatus
from config import db

# 블루프린트 정의
index_bp = Blueprint('index', __name__)

# Index 페이지
@index_bp.route('/')
def index():
    # id가 5인 이미지를 가져옵니다.
    image = Image.query.filter_by(id=5).first()

    # 이미지가 있으면 URL을 전달, 없으면 None을 전달
    image_url = image.url if image else None
    
    return render_template('index.html',image_url=image_url)


