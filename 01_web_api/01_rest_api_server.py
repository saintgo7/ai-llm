"""
01. REST API Server - Flask 기반 간단한 REST API
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# 메모리 데이터베이스
tasks = []
task_id_counter = 1

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """모든 작업 조회"""
    return jsonify({'tasks': tasks, 'count': len(tasks)})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """특정 작업 조회"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """새 작업 생성"""
    global task_id_counter
    data = request.get_json()

    task = {
        'id': task_id_counter,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'completed': False
    }
    tasks.append(task)
    task_id_counter += 1

    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """작업 업데이트"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['completed'] = data.get('completed', task['completed'])

    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """작업 삭제"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    print("REST API Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)
