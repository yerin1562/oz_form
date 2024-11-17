from flask import Blueprint, request, jsonify
from config import db
from app.models import DetailQuestion

bp = Blueprint("detail_questions", __name__, url_prefix="/detail-questions")

# 모든 상세 질문 조회
@bp.route("/", methods=["GET"])
def get_detail_questions():
    detail_questions = DetailQuestion.query.all()
    return jsonify([dq.to_dict() for dq in detail_questions]), 200

# 특정 상세 질문 조회
@bp.route("/<int:detail_questions_id>", methods=["GET"])
def get_detail_questions(detail_questions_id):
    detail_questions = DetailQuestion.query.get(detail_questions_id)
    if not detail_questions:
        return jsonify({"error": "DetailQuestion not found"}), 404
    return jsonify(detail_questions.to_dict()), 200

# 새로운 상세 질문생성
@bp.route("/", methods=["POST"])
def create_detail_questions():
    data = request.get_json()

    content = data.get("content")
    sqe = data.get("sqe")
    questions_id = data.get("questions_id")
    is_active = data.get("is_active")

    if not content or not sqe or not questions_id:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_detail_questions = DetailQuestion(
        content = content,
        sqe = sqe,
        questions_id = questions_id,
        is_active = is_active
    )

    db.session.add(new_detail_questions)
    db.session.commit()

    return jsonify(new_detail_questions.to_dict()), 201