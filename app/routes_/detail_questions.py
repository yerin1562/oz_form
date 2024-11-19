from flask import Blueprint, request, jsonify  # Flask에서 필요한 Blueprint, request, jsonify를 가져온다.
from config import db  # 데이터베이스 연결 객체 db를 가져온다. 이 객체는 데이터베이스와 상호작용하는 데 사용된다.
from app.models import Detail_questions, Answer  # 데이터베이스의 Detail_questions 및 Answer 테이블과 매핑된 모델 클래스.

# Flask에서 기능을 모듈화하기 위해 Blueprint를 사용한다.
# "detail_questions"라는 이름의 Blueprint를 생성하고, /detail-questions 경로로 연결한다.
detail_questions_bp = Blueprint("detail_questions", __name__, url_prefix="/questions")

# 모든 상세 질문 조회
@detail_questions_bp.route("/", methods=["GET"])  # GET 요청에 반응하는 엔드포인트를 정의한다.
def get_detail_questions():  

    # 데이터베이스에서 Detail_questions 테이블의 모든 레코드를 조회한다.
    detail_questions = Detail_questions.query.all()  

    # 조회된 레코드들을 JSON 형식으로 변환하여 반환한다.
    return jsonify([dq.to_dict() for dq in detail_questions]), 200  

# 특정 상세 질문 조회
@detail_questions_bp.route("/<int:detail_questions_id>", methods=["GET"])  # URL 경로에 숫자형 ID를 포함해 요청을 처리한다.
def get_detail_question(detail_questions_id):  

    # 데이터베이스에서 입력받은 ID에 해당하는 레코드를 검색한다.
    detail_question = Detail_questions.query.get(detail_questions_id)  
    
    # 해당 ID의 레코드가 없을 경우, 404 상태 코드와 에러 메시지를 반환한다.
    if not detail_question:
        return jsonify({"error": "Detail_questions not found"}), 404  
    
    # 검색된 레코드를 JSON 형식으로 반환한다. 성공 시 200 상태 코드 반환.
    return jsonify(detail_question.to_dict()), 200  

# 특정 조건에 맞는 상세 질문 조회
@detail_questions_bp.route("/filtered", methods=["GET"])  # GET 요청에 반응하는 새로운 엔드포인트를 정의한다.
def get_filtered_detail_questions():

    # 데이터베이스에서 조건(sqe: 1~4, is_active: True)에 맞는 레코드를 필터링한다.
    filtered_questions = Detail_questions.query.filter(
        Detail_questions.sqe.between(1, 4),  # sqe가 1과 4 사이인 레코드
        Detail_questions.is_active == True  # 활성화된 레코드만 포함
    ).order_by(Detail_questions.sqe).all()  # sqe 기준으로 정렬

    # 조회된 데이터를 JSON 형식으로 반환한다.
    return jsonify([dq.to_dict() for dq in filtered_questions]), 200


# 새로운 상세 질문 생성
@detail_questions_bp.route("/", methods=["POST"])  # POST 요청을 처리하는 엔드포인트를 정의한다.
def create_detail_questions():  

    # 요청에서 JSON 데이터를 추출한다.
    data = request.get_json()  

    # 요청 데이터에서 필드(content, sqe, questions_id)를 가져온다.
    content = data.get("content")  # 질문 내용
    sqe = data.get("sqe")  # 질문의 순서
    questions_id = data.get("questions_id")  # 상위 질문의 ID
    is_active = data.get("is_active", True)  # 활성 상태 여부. 기본값은 True.

    # 필수 데이터가 누락된 경우, 400 상태 코드와 함께 에러 메시지를 반환한다.
    if not content or not sqe or not questions_id:
        return jsonify({"error": "Missing required fields"}), 400  

    # 새로운 Detail_questions 객체를 생성한다.
    new_detail_questions = Detail_questions(
        content=content,  # 질문 내용
        sqe=sqe,  # 질문 순서
        questions_id=questions_id,  # 상위 질문 ID
        is_active=is_active  # 활성 상태 여부
    )
    
    # 생성된 객체를 데이터베이스 세션에 추가한다.
    db.session.add(new_detail_questions)
    # 변경사항을 데이터베이스에 커밋하여 저장한다.
    db.session.commit()

    # 새로 생성된 객체를 JSON 형식으로 반환한다. 201 상태 코드는 성공적으로 리소스가 생성되었음을 의미한다.
    return jsonify({
        "detail_questions": new_detail_questions.to_dict()
    }), 201  