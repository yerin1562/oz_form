from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, User, Question, Detail_questions, Answer, Image
from sqlalchemy.orm import joinedload

bp = Blueprint('bp', __name__)

# 인덱스 페이지에서 이미지 id=5 출력
@bp.route('/')
def index():
    image = Image.query.filter_by(id=5).first()

    # 이미지가 있으면 URL을 전달, 없으면 None을 전달
    image_url = image.url if image else None
    
    return render_template('index.html',image_url=image_url)

# 회원가입 후 question 페이지로 이동
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        mbti = request.form['mbti']

        user = User(name=name, age=age, gender=gender, mbti=mbti)
        db.session.add(user)
        db.session.commit()

        # 사용자가 등록된 후, 첫 번째 질문으로 리디렉션
        return redirect(url_for('bp.question', question_id=1, user_id=user.id))

    return render_template('signup.html')

# 질문 페이지, 이미지와 질문 출력
@bp.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    user_id = request.args.get('user_id')
    question = Question.query.filter_by(id=question_id).first()
    image = question.image  # 해당 질문에 대한 이미지
    detail_questions = Detail_questions.query.filter_by(question_id=question_id).all()

    if request.method == 'POST':
        # 사용자가 선택한 답변 저장
        for dq in detail_questions:
            answer = request.form.get(str(dq.id))  # answer는 폼 데이터에서 가져옴
            if answer:
                user_answer = Answer(user_id=user_id, detail_question_id=dq.id)
                db.session.add(user_answer)

        db.session.commit()

        # 다음 질문으로 리디렉션
        if question_id < 4:
            return redirect(url_for('bp.question', question_id=question_id + 1, user_id=user_id))
        else:
            return redirect(url_for('bp.results', user_id=user_id))

    return render_template('question.html', question=question, image=image, detail_questions=detail_questions)

# 결과 페이지 - 통계 생성
@bp.route('/results')
def results():
    user_id = request.args.get('user_id')
    
    # 사용자의 모든 답변 가져오기
    answers = Answer.query.filter_by(user_id=user_id).all()

    # 답변 통계 처리 (예: 각 질문에 대한 답변 빈도수 계산)
    result_data = {}
    for answer in answers:
        dq = Detail_questions.query.filter_by(id=answer.detail_question_id).first()
        if dq.question_id not in result_data:
            result_data[dq.question_id] = {}
        result_data[dq.question_id][dq.content] = result_data[dq.question_id].get(dq.content, 0) + 1

    # Plotly 그래프를 위한 데이터 준비
    import plotly.graph_objects as go

    fig = go.Figure()

    for question_id, answers in result_data.items():
        for content, count in answers.items():
            fig.add_trace(go.Bar(
                x=[content], y=[count],
                name=f'Question {question_id}: {content}'
            ))

    graph_html = fig.to_html(full_html=False)
    return render_template('results.html', graph_html=graph_html)
