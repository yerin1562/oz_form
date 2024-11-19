from flask import Blueprint, request, jsonify
from app.models import db, Answer, User, Detail_questions

answer_bp = Blueprint('answer_bp', __name__)

# 1. 응답 저장 (사용자가 설문 응답을 제출할 때)
@answer_bp.route('/submit_answer', methods=['POST'])
def submit_answer():
    """
    사용자가 설문에 응답을 제출하는 라우트
    요청 본문에서 사용자 ID, 질문 ID 및 응답을 받아 데이터베이스에 저장
    """
    data = request.get_json()  # 요청 본문에서 JSON 데이터 받기
    
    # 필수 데이터가 모두 있는지 확인
    if not all(key in data for key in ('user_id', 'detail_question_id')):
        return jsonify({"message": "Missing required fields"}), 400
    
    user_id = data['user_id']
    detail_question_id = data['detail_question_id']
    
    # 응답을 데이터베이스에 저장
    new_answer = Answer(
        user_id=user_id,
        detail_question_id=detail_question_id
    )
    
    db.session.add(new_answer)
    db.session.commit()
    
    return jsonify({"message": "Answer submitted successfully", "answer_id": new_answer.id}), 201


# 2. 특정 사용자의 응답 조회
@answer_bp.route('/user_answers/<int:user_id>', methods=['GET'])
def get_user_answers(user_id):
    """
    특정 사용자가 제출한 모든 응답을 조회하는 라우트
    user_id에 해당하는 사용자가 응답한 모든 질문에 대한 응답을 반환
    """
    answers = Answer.query.filter_by(user_id=user_id).all()  # 해당 사용자에 대한 모든 응답 조회
    
    # 사용자가 응답한 결과가 없으면
    if not answers:
        return jsonify({"message": "No answers found for this user"}), 404
    
    # 응답 리스트 반환
    answers_list = [answer.to_dict() for answer in answers]
    return jsonify({"answers": answers_list}), 200


# 3. 특정 질문에 대한 응답 조회 (여러 응답을 묶어서 반환)
@answer_bp.route('/question_answers/<int:question_id>', methods=['GET'])
def get_question_answers(question_id):
    """
    특정 질문에 대한 모든 응답을 조회하는 라우트
    detail_question_id에 해당하는 질문에 대한 모든 응답을 반환
    """
    answers = Answer.query.filter_by(detail_question_id=question_id).all()  # 해당 질문에 대한 모든 응답 조회
    
    # 질문에 대한 응답이 없으면
    if not answers:
        return jsonify({"message": "No answers found for this question"}), 404
    
    # 응답 리스트 반환
    answers_list = [answer.to_dict() for answer in answers]
    return jsonify({"answers": answers_list}), 200



