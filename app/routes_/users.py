from flask import request, jsonify, render_template, redirect, url_for
from flask.views import MethodView
from flask_smorest import Blueprint
from app.models import User
from config import db

user_bp = Blueprint('Users', 'users', description='Operations on users')


# 함수 기반 뷰: 회원가입 페이지 렌더링 및 처리
@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = request.get_json()

        new_user = User(name=user_data["name"], age=user_data["age"], gender=user_data["gender"], mbti=user_data["mbti"])
        db.session.add(new_user)
        db.session.commit()

        # 성공 메시지와 함께 페이지를 새로고침
        # return jsonify("User created successfully!"), 201
        return jsonify({
            "message": "User created successfully!",
            "user_id": new_user.id
        }), 201 # ===> 수정됨(효)

    else: 
        return render_template("signup.html")


# 클래스 기반 뷰: 특정 사용자 결과 조회
@user_bp.route('/result/<int:user_id>')
class Users(MethodView):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "mbti": user.mbti
        }