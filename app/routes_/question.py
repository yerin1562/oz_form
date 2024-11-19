from flask import Blueprint, render_template, redirect, url_for, abort, request
# from flask.views import MethodView
from app.models import Question, Detail_questions

question_bp = Blueprint('question_bp', __name__, url_prefix='/question')


@question_bp.route('/<int:question_id>', methods=['GET'])
def question(question_id):
    # 데이터베이스에서 주어진 question_id에 해당하는 활성화된 질문 검색
    question = Question.query.filter_by(id=question_id, is_active=True).first()

    # question_id가 유효하지 않거나 비활성화된 경우, 첫 번째 활성화된 질문으로 redirection.
    if not question:
        first_active_question = Question.query.filter_by(is_active=True).order_by(Question.sqe).first()
        if first_active_question:
            return redirect(url_for('question_bp.question', question_id=first_active_question.id))
        else:
            # 활성화된 질문이 없으면 404 error 반환
            abort(404, description="No active questions available")

    # user_id를 URL의 쿼리 파라미터에서 읽기 ==> 추가됨 (효)
    user_id = request.args.get('user_id')
    if not user_id:
        abort(400, description="User ID is required")

    # 해당 question에 연결된 detail_questions 4개를 가져오기 ==> 추가됨 (효)
    detail_questions = Detail_questions.query.filter_by(question_id=question_id).all()


    # question.html redering. ==> 뒤에 user_id=user_id 추가됨 (효), 2nd 추가 (효) ==> detail_questions=detail_questions
    return render_template('question.html', question=question.to_dict(), user_id=user_id, detail_questions=detail_questions)

# # URL을 MethodView로 연결
# question_bp.add_url_rule('/<int:question_id>', view_func=QuestionView.as_view('question'))
