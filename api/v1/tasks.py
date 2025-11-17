"""
API v1 - Tasks Endpoints
"""
from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create API v1 blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# In-memory storage (would be database in production)
tasks = []
task_id_counter = 1

@api_v1.route('/tasks', methods=['GET'])
def get_tasks_v1():
    """Get all tasks (v1)"""
    logger.info("GET /api/v1/tasks")

    status = request.args.get('status')
    filtered_tasks = tasks

    if status:
        if status == 'completed':
            filtered_tasks = [t for t in tasks if t['completed']]
        elif status == 'pending':
            filtered_tasks = [t for t in tasks if not t['completed']]

    return jsonify({
        'version': 'v1',
        'tasks': filtered_tasks,
        'count': len(filtered_tasks)
    })

@api_v1.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_v1(task_id):
    """Get task by ID (v1)"""
    logger.info(f"GET /api/v1/tasks/{task_id}")

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)

    return jsonify({'error': 'Task not found'}), 404

@api_v1.route('/tasks', methods=['POST'])
def create_task_v1():
    """Create new task (v1)"""
    global task_id_counter

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    task = {
        'id': task_id_counter,
        'title': data.get('title', '').strip(),
        'description': data.get('description', '').strip(),
        'completed': data.get('completed', False),
        'created_at': datetime.now().isoformat()
    }

    tasks.append(task)
    task_id_counter += 1

    return jsonify(task), 201

@api_v1.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_v1(task_id):
    """Update task (v1)"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    if 'title' in data:
        task['title'] = data['title'].strip()
    if 'description' in data:
        task['description'] = data['description'].strip()
    if 'completed' in data:
        task['completed'] = data['completed']

    return jsonify(task)

@api_v1.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_v1(task_id):
    """Delete task (v1)"""
    global tasks

    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]

    if len(tasks) == initial_count:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task deleted successfully'})
