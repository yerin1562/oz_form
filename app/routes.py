from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import User, Question, Detail_questions, Answer, Image
import plotly.express as px
import plotly.io as pio

bp = Blueprint('bp', __name__)

# 인덱스 페이지에서 이미지 id=5 출력
@bp.route('/')
def index():
    image = Image.query.filter_by(id=5).first()
    # 이미지가 있으면 URL을 전달, 없으면 None을 전달
    image_url = image.url if image else None
    
    return render_template('index.html',image_url=image_url)


# 회원가입 페이지 (signup.html)
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()

        # 사용자 정보를 받아서 데이터베이스에 저장
        user = User(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            mbti=data['mbti']
        )

        db.session.add(user)
        db.session.commit()

        # 성공적으로 가입한 후 user_id를 반환
        return redirect(f'/question/1?user_id={user.id}')
    
    # GET 요청일 경우 signup.html 렌더링
    return render_template('signup.html')


# 질문 페이지 (question.html) - 질문 1부터 4까지 처리
@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    user_id = request.args.get('user_id')  # URL에서 user_id 받기
    question = Question.query.get(question_id)  # 현재 질문
    image = Image.query.filter_by(id=question.image_id).first()  # 해당 질문에 맞는 이미지

    # POST 요청일 경우 답변을 저장
    if request.method == 'POST':
        # 답변 처리
        detail_question_ids = request.form.getlist('detail_question_id')
        for detail_question_id in detail_question_ids:
            answer = Answer(user_id=user_id, detail_question_id=detail_question_id)
            db.session.add(answer)
        db.session.commit()

        # 마지막 질문이면 결과 페이지로 이동
        if question_id == 4:
            return redirect(url_for('bp.results', user_id=user_id))
        # 아니면 다음 질문으로 이동
        return redirect(url_for('bp.question', question_id=question_id + 1, user_id=user_id))

    # 해당 질문에 대한 detail_questions 가져오기
    detail_questions = Detail_questions.query.filter_by(question_id=question.id).all()

    return render_template('question.html', question=question, image=image, detail_questions=detail_questions, user_id=user_id)

# 결과 페이지 (result.html) - 답변 통계를 Plotly로 출력
@bp.route('/results/<int:user_id>', methods=['GET'])
def results(user_id):
    # 사용자에 해당하는 답변 가져오기
    answers = Answer.query.filter_by(user_id=user_id).all()

    # 답변 통계를 분석하기 위한 데이터 준비
    answer_data = {}
    for answer in answers:
        detail_question = Detail_questions.query.get(answer.detail_question_id)
        if detail_question.id not in answer_data:
            answer_data[detail_question.id] = 0
        answer_data[detail_question.id] += 1

    # Plotly 그래프 준비
    fig = px.bar(x=list(answer_data.keys()), y=list(answer_data.values()), labels={'x': 'Detail Question ID', 'y': 'Answer Count'})
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('results.html', graph_html=graph_html)
