from flask import render_template, redirect, url_for, abort
from app import app, db
from app.models import Question

@app.route('/question/<int:question_id>', methods=['GET'])
def question(question_id):
    # 데이터베이스에서 주어진 question_id에 해당하는 활성화된 질문 검색
    question = Question.query.filter_by(id=question_id, is_active=True).first()

    # question_id가 유효하지 않거나 비활성화된 경우, 첫 번째 활성화된 질문으로 redirection.
    if not question:
        first_active_question = Question.query.filter_by(is_active=True).order_by(Question.sqe).first()
        if first_active_question:
            return redirect(url_for('question', question_id=first_active_question.id))
        else:
            # 활성화된 질문이 없으면 404 error 반환
            abort(404, description="No active questions available")

    # 마지막 질문에 도달하면 results 페이지로 redirection.
    if question.sqe == 4:
        return redirect(url_for('results'))

    # 질문 렌더링
    return render_template('question.html', question=question.to_dict())
