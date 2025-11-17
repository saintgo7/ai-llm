"""
API v2 - Tasks Endpoints (Enhanced)
Added: Priority, Tags, Due dates, Pagination
"""
from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create API v2 blueprint
api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

# In-memory storage
tasks = []
task_id_counter = 1

@api_v2.route('/tasks', methods=['GET'])
def get_tasks_v2():
    """Get all tasks with pagination and filtering (v2)"""
    logger.info("GET /api/v2/tasks")

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Filtering
    status = request.args.get('status')
    priority = request.args.get('priority')
    tag = request.args.get('tag')

    filtered_tasks = tasks

    if status:
        if status == 'completed':
            filtered_tasks = [t for t in filtered_tasks if t['completed']]
        elif status == 'pending':
            filtered_tasks = [t for t in filtered_tasks if not t['completed']]

    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority]

    if tag:
        filtered_tasks = [t for t in filtered_tasks if tag in t.get('tags', [])]

    # Pagination logic
    total = len(filtered_tasks)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = filtered_tasks[start:end]

    return jsonify({
        'version': 'v2',
        'tasks': paginated_tasks,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        },
        'filters': {
            'status': status,
            'priority': priority,
            'tag': tag
        }
    })

@api_v2.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_v2(task_id):
    """Get task by ID with full details (v2)"""
    logger.info(f"GET /api/v2/tasks/{task_id}")

    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify({
            'version': 'v2',
            'task': task
        })

    return jsonify({'error': 'Task not found'}), 404

@api_v2.route('/tasks', methods=['POST'])
def create_task_v2():
    """Create new task with enhanced fields (v2)"""
    global task_id_counter

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    # Validate priority
    priority = data.get('priority', 'medium')
    if priority not in ['low', 'medium', 'high', 'urgent']:
        return jsonify({'error': 'Invalid priority value'}), 400

    task = {
        'id': task_id_counter,
        'title': data.get('title', '').strip(),
        'description': data.get('description', '').strip(),
        'completed': data.get('completed', False),
        'priority': priority,
        'tags': data.get('tags', []),
        'due_date': data.get('due_date'),
        'assignee': data.get('assignee'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    tasks.append(task)
    task_id_counter += 1

    logger.info(f"Task created: ID={task['id']}, Priority={task['priority']}")

    return jsonify({
        'version': 'v2',
        'task': task
    }), 201

@api_v2.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_v2(task_id):
    """Update task with enhanced fields (v2)"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    # Update fields
    if 'title' in data:
        task['title'] = data['title'].strip()
    if 'description' in data:
        task['description'] = data['description'].strip()
    if 'completed' in data:
        task['completed'] = data['completed']
    if 'priority' in data:
        if data['priority'] in ['low', 'medium', 'high', 'urgent']:
            task['priority'] = data['priority']
    if 'tags' in data:
        task['tags'] = data['tags']
    if 'due_date' in data:
        task['due_date'] = data['due_date']
    if 'assignee' in data:
        task['assignee'] = data['assignee']

    task['updated_at'] = datetime.now().isoformat()

    return jsonify({
        'version': 'v2',
        'task': task
    })

@api_v2.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_v2(task_id):
    """Delete task (v2)"""
    global tasks

    initial_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]

    if len(tasks) == initial_count:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({
        'version': 'v2',
        'message': 'Task deleted successfully'
    })

@api_v2.route('/tasks/stats', methods=['GET'])
def get_task_stats_v2():
    """Get task statistics (v2 only)"""
    total = len(tasks)
    completed = sum(1 for t in tasks if t['completed'])
    by_priority = {}

    for task in tasks:
        priority = task.get('priority', 'medium')
        by_priority[priority] = by_priority.get(priority, 0) + 1

    return jsonify({
        'version': 'v2',
        'statistics': {
            'total': total,
            'completed': completed,
            'pending': total - completed,
            'by_priority': by_priority
        }
    })
