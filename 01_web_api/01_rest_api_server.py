"""
01. REST API Server - Flask 기반 간단한 REST API
Environment Variables, Input Validation, Logging 추가
"""
import sys
import os
import logging
from datetime import datetime

# 상위 디렉토리의 config 모듈 import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request

try:
    from config import Config
except ImportError:
    # config.py가 없는 경우 기본값 사용
    class Config:
        SECRET_KEY = 'dev-secret-key'
        API_PORT = 5000
        LOG_LEVEL = 'INFO'

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# 메모리 데이터베이스
tasks = []
task_id_counter = 1

def validate_task_data(data, require_title=True):
    """
    작업 데이터 검증

    Args:
        data: 검증할 데이터
        require_title: 제목 필수 여부

    Returns:
        (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"

    # 제목 검증
    if require_title:
        title = data.get('title', '').strip()
        if not title:
            return False, "Title is required and cannot be empty"

        if len(title) > 200:
            return False, "Title must be less than 200 characters"

    # 설명 검증
    description = data.get('description', '')
    if description and len(description) > 1000:
        return False, "Description must be less than 1000 characters"

    # 완료 상태 검증
    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return False, "Completed must be a boolean value"

    return True, None

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """모든 작업 조회"""
    logger.info(f"GET /api/tasks - Fetching all tasks")

    # 쿼리 파라미터로 필터링 지원
    status = request.args.get('status')
    filtered_tasks = tasks

    if status:
        if status == 'completed':
            filtered_tasks = [t for t in tasks if t['completed']]
        elif status == 'pending':
            filtered_tasks = [t for t in tasks if not t['completed']]

    logger.info(f"Returning {len(filtered_tasks)} tasks")
    return jsonify({
        'tasks': filtered_tasks,
        'count': len(filtered_tasks),
        'total': len(tasks)
    })

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """특정 작업 조회"""
    logger.info(f"GET /api/tasks/{task_id} - Fetching task")

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        logger.info(f"Task {task_id} found")
        return jsonify(task)

    logger.warning(f"Task {task_id} not found")
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """새 작업 생성"""
    global task_id_counter

    logger.info("POST /api/tasks - Creating new task")

    # Content-Type 검증
    if not request.is_json:
        logger.error("Invalid content type")
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    # 입력 검증
    is_valid, error_message = validate_task_data(data, require_title=True)
    if not is_valid:
        logger.error(f"Validation error: {error_message}")
        return jsonify({'error': error_message}), 400

    task = {
        'id': task_id_counter,
        'title': data.get('title', '').strip(),
        'description': data.get('description', '').strip(),
        'completed': data.get('completed', False),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    tasks.append(task)
    task_id_counter += 1

    logger.info(f"Task created successfully: ID={task['id']}, Title={task['title']}")
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """작업 업데이트"""
    logger.info(f"PUT /api/tasks/{task_id} - Updating task")

    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        logger.warning(f"Task {task_id} not found")
        return jsonify({'error': 'Task not found'}), 404

    # Content-Type 검증
    if not request.is_json:
        logger.error("Invalid content type")
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    # 입력 검증 (제목은 선택사항)
    is_valid, error_message = validate_task_data(data, require_title=False)
    if not is_valid:
        logger.error(f"Validation error: {error_message}")
        return jsonify({'error': error_message}), 400

    # 업데이트
    if 'title' in data:
        task['title'] = data['title'].strip()
    if 'description' in data:
        task['description'] = data['description'].strip()
    if 'completed' in data:
        task['completed'] = data['completed']

    task['updated_at'] = datetime.now().isoformat()

    logger.info(f"Task {task_id} updated successfully")
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """작업 삭제"""
    global tasks

    logger.info(f"DELETE /api/tasks/{task_id} - Deleting task")

    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]

    if len(tasks) == initial_count:
        logger.warning(f"Task {task_id} not found")
        return jsonify({'error': 'Task not found'}), 404

    logger.info(f"Task {task_id} deleted successfully")
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tasks_count': len(tasks)
    })

@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = getattr(Config, 'API_PORT', 5000)
    logger.info(f"REST API Server starting on http://localhost:{port}")
    logger.info("Available endpoints:")
    logger.info("  GET    /api/tasks          - Get all tasks")
    logger.info("  GET    /api/tasks/<id>     - Get task by ID")
    logger.info("  POST   /api/tasks          - Create new task")
    logger.info("  PUT    /api/tasks/<id>     - Update task")
    logger.info("  DELETE /api/tasks/<id>     - Delete task")
    logger.info("  GET    /api/health         - Health check")

    app.run(debug=True, port=port)
