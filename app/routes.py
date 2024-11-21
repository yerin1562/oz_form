from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from config import db
from app.models import User, Question, Detail_questions, Answer, Image

bp = Blueprint('main', __name__)

# 첫 번째 페이지: 설문조사 시작 페이지
@bp.route('/')
def index():
    main_image = Image.query.filter_by(type='main').first()
    return render_template('index.html', image_url=main_image.url if main_image else None)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json

        # 새로운 사용자 항상 생성
        user = User(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            mbti=data['mbti']
        )
        db.session.add(user)
        db.session.commit()

        message = "회원가입 완료! 설문을 시작합니다."

        return jsonify({'message': message, 'user_id': user.id})
    else:
        return render_template('signup.html')



# 세 번째부터 여섯 번째까지의 설문 페이지
@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    question = Question.query.get_or_404(question_id)
    choices = Detail_questions.query.filter_by(question_id=question_id).all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        selected_answer = request.form.get('answer')

        if user_id and selected_answer:
            answer = Answer(user_id=user_id, detail_question_id=selected_answer)
            db.session.add(answer)
            db.session.commit()

            # 다음 질문으로 이동 또는 결과 페이지로 리다이렉트
            next_question = Question.query.filter(Question.sqe > question.sqe).order_by(Question.sqe).first()
            if next_question:
                return redirect(url_for('main.question', question_id=next_question.id, user_id=user_id))
            else:
                return redirect(url_for('main.results', user_id=user_id))

    else:
        return render_template('question.html', question=question, choices=choices)

# 마지막 페이지: 통계 페이지
@bp.route('/results/<int:user_id>')
def results(user_id):
    # 통계 계산 예시: T와 F 비율
    total_users = User.query.count()
    t_users = User.query.filter(User.mbti.like('%T%')).count()
    f_users = User.query.filter(User.mbti.like('%F%')).count()

    question_charts = []
    for i in range(4):  # 4개의 질문에 대한 데이터
        question = Question.query.filter_by(sqe=i + 1).first()
        if question:
            choices = Detail_questions.query.filter_by(question_id=question.id).all()
            chart_data = {
                "labels": [choice.content for choice in choices],
                "values": [
                    Answer.query.filter_by(detail_question_id=choice.id).count()
                    for choice in choices
                ],
                "type": "pie",
                "name": f"Question {i + 1}"
            }
            question_charts.append(chart_data)

    return render_template(
        'results.html',
        t_percentage=round((t_users / total_users) * 100, 2) if total_users else 0,
        f_percentage=round((f_users / total_users) * 100, 2) if total_users else 0,
        question_charts=question_charts
    )

# # 통계 데이터 API
# @bp.route('/results/stats')
# def results_stats():
#     total_users = User.query.count()
#     t_users = User.query.filter(User.mbti.like('%T%')).count()
#     f_users = User.query.filter(User.mbti.like('%F%')).count()

#     same_result_chart = {
#         "labels": ["T", "F"],
#         "values": [t_users, f_users],
#         "type": "pie"
#     }

#     # 추가 통계 차트 데이터 구성
#     return jsonify({
#         "same_result_chart": same_result_chart,
#         "age_chart": {},  # 연령별 통계 데이터 구성
#         "gender_chart": {},  # 성별 통계 데이터 구성
#         "age_distribution_chart": {},  # 연령대 통계 데이터 구성
#         "question_charts": []  # 질문별 통계 데이터 구성
#     })
