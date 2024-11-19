from flask import Blueprint, request, jsonify
from config import db
from app.models import Detail_questions, Answer, Question

detail_questions_bp = Blueprint("detail_questions", __name__, url_prefix="/questions")

@detail_questions_bp.route("/", methods=["GET"])
def get_detail_questions():
    detail_questions = Detail_questions.query.all()
    return jsonify([dq.to_dict() for dq in detail_questions]), 200

@detail_questions_bp.route("/<int:detail_questions_id>", methods=["GET"])
def get_detail_question(detail_questions_id):
    detail_question = Detail_questions.query.get(detail_questions_id)
    if not detail_question:
        return jsonify({"error": "Detail_questions not found"}), 404
    return jsonify(detail_question.to_dict()), 200

# @detail_questions_bp.route("/filtered", methods=["GET"])
# def get_filtered_detail_questions():
#     filtered_questions = Detail_questions.query.filter(
#         Detail_questions.sqe.between(1, 4),
#         Detail_questions.is_active == True
#     ).order_by(Detail_questions.sqe).all()
#     return jsonify([dq.to_dict() for dq in filtered_questions]), 200

# 수정 (효)
@detail_questions_bp.route("/filtered", methods=["GET"])
def get_filtered_detail_questions():
    question_id = request.args.get("question_id")
    if not question_id:
        return jsonify({"error": "question_id is required"}), 400

    filtered_questions = Detail_questions.query.filter(
        Detail_questions.questions_id == question_id,
        Detail_questions.sqe.between(1, 4),
        Detail_questions.is_active == True
    ).order_by(Detail_questions.sqe).all()
    return jsonify([dq.to_dict() for dq in filtered_questions]), 200



# @detail_questions_bp.route("/", methods=["POST"])
# def create_detail_questions():
#     data = request.get_json()
#     content = data.get("content")
#     sqe = data.get("sqe")
#     questions_id = data.get("questions_id")
#     is_active = data.get("is_active", True)

#     if not content or not sqe or not questions_id:
#         return jsonify({"error": "Missing required fields"}), 400

#     new_detail_questions = Detail_questions(
#         content=content,
#         sqe=sqe,
#         questions_id=questions_id,
#         is_active=is_active
#     )
    
#     db.session.add(new_detail_questions)
#     db.session.commit()

#     return jsonify({
#         "detail_questions": new_detail_questions.to_dict()
#     }), 201

# 수정 (효)
@detail_questions_bp.route("/", methods=["POST"])
def create_detail_questions():
    data = request.get_json()
    content = data.get("content")
    sqe = data.get("sqe")
    question_id = data.get("questions_id")  # 필드명 수정: questions_id -> question_id
    is_active = data.get("is_active", True)

    if not content or not sqe or not question_id:
        return jsonify({"error": "Missing required fields"}), 400

    new_detail_question = Detail_questions(
        content=content,
        sqe=sqe,
        questions_id=question_id,  # 필드명 수정: questions_id -> question_id
        is_active=is_active
    )

    db.session.add(new_detail_question)
    db.session.commit()

    return jsonify({
        "detail_questions": new_detail_question.to_dict()
    }), 201
