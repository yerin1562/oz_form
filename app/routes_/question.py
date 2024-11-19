from flask import Blueprint, render_template, redirect, url_for, abort
from flask.views import MethodView
from app.models import Question

question_bp = Blueprint('question_bp', __name__, url_prefix='/question')

class QuestionView(MethodView):
    def get(self, question_id):
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

        # question.html redering.
        return render_template('question.html', question=question.to_dict())

# URL을 MethodView로 연결
question_bp.add_url_rule('/<int:question_id>', view_func=QuestionView.as_view('question'))
