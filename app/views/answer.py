from flask import Blueprint, render_template, request, redirect, url_for, session 
from flask.views import MethodView
from models import Image, Answer, Question, ImageStatus, Option 
from config import db

# 블루프린트 정의
answer_bp = Blueprint('quiz', __name__)


from flask import Blueprint, render_template, request, redirect, url_for, session
from flask.views import MethodView
from models import Answer, Question
from config import db

# 블루프린트 정의
answer_bp = Blueprint('quiz', __name__)

class AnswerView(MethodView):
    def post(self, detail_question_id):
        """
        사용자의 답변을 저장하고, 다음 질문으로 이동
        """
        # 사용자가 선택한 답변 ID 가져오기
        answer_id = request.form.get('answer')  # 선택된 답변 ID
        user_id = session.get('user_id')  # 로그인한 사용자 ID를 세션에서 가져오기

        # 세션에 현재 질문 ID 저장
        session['detail_question_id'] = detail_question_id
        
        if not answer_id:
            return "답변이 선택되지 않았습니다.", 400  # 에러 메시지 반환

        # 데이터베이스에 답변 저장
        new_answer = Answer(user_id=user_id, detail_question_id=detail_question_id)
        db.session.add(new_answer)
        db.session.commit()

        # 다음 질문 찾기
        next_question = Question.query.filter(Question.sqe > detail_question_id).order_by(Question.sqe.asc()).first()

        if next_question:
            # 다음 질문으로 리디렉션
            return redirect(url_for('quiz.answer', detail_question_id=next_question.id))
        else:
            # 질문이 끝나면 결과 페이지로 이동
            return redirect(url_for('quiz.result'))

# 블루프린트에 메소드 뷰 등록
answer_bp.add_url_rule('/answer/<int:detail_question_id>', view_func=AnswerView.as_view('answer'))

# Result 페이지 (모든 질문 완료 후 통계 출력)
@answer_bp.route('/result', methods=['GET'])
def result():
    """
    결과 페이지를 렌더링
    """
    return render_template('result.html')


