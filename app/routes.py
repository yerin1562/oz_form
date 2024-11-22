from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from config import db
from app.models import User, Question, Detail_questions, Answer, Image
import plotly.express as px


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



# 결과 통계 페이지
@bp.route('/results/<int:user_id>')
def results(user_id):
    # 사용자 데이터를 불러오는 예시 (예를 들어 사용자가 설문조사에 응답한 결과)
    user = User.query.get(user_id)
    # 예시 데이터는 실제 모델에 맞게 변경 필요
    results = {"MBTI": user.mbti, "age": user.age, "gender": user.gender}
    
    # Plotly 그래프 예시: MBTI F/T 비율
    t_users = User.query.filter(User.mbti.like('%T%')).count()
    f_users = User.query.filter(User.mbti.like('%F%')).count()
    mbti_data = {
        "labels": ["T", "F"],
        "values": [t_users, f_users],
        "type": "pie"
    }
    mbti_chart = px.pie(names=mbti_data["labels"], values=mbti_data["values"])

    # 나이별 선택자 비율
    age_groups = {
        "teen": User.query.filter(User.age == 'teen').count(),
        "twenty": User.query.filter(User.age == 'twenty').count(),
        "thirty": User.query.filter(User.age == 'thirty').count(),
        "fourty": User.query.filter(User.age == 'fourty').count(),
        "fifty": User.query.filter(User.age == 'fifty').count()
    }
    age_chart = px.bar(x=list(age_groups.keys()), y=list(age_groups.values()), title="Age Distribution")

    # 성별별 선택자 비율
    gender_groups = {
        "male": User.query.filter(User.gender == 'male').count(),
        "female": User.query.filter(User.gender == 'female').count()
    }
    gender_chart = px.bar(x=list(gender_groups.keys()), y=list(gender_groups.values()), title="Gender Distribution")

    # 모든 MBTI 비율
    mbti_count = {}
    for mbti_type in ['INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP','ISTH','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP']:  # 여기에 실제 MBTI 타입을 다 넣으세요.
        mbti_count[mbti_type] = User.query.filter(User.mbti == mbti_type).count()
    mbti_dist_chart = px.bar(x=list(mbti_count.keys()), y=list(mbti_count.values()), title="MBTI Distribution")

    # 결과 페이지에서 차트 표시
    return render_template('results.html', 
                           user_results=results,
                           mbti_chart=mbti_chart.to_html(full_html=False),
                           age_chart=age_chart.to_html(full_html=False),
                           gender_chart=gender_chart.to_html(full_html=False),
                           mbti_dist_chart=mbti_dist_chart.to_html(full_html=False))


