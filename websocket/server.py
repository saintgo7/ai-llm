"""
WebSocket Server - Real-time communication
"""
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins="*")

# Connected users
connected_users = {}

@socketio.on('connect')
def handle_connect():
    """클라이언트 연결"""
    client_id = request.sid
    connected_users[client_id] = {
        'connected_at': datetime.now().isoformat(),
        'rooms': []
    }

    logger.info(f"Client connected: {client_id}")

    emit('connection_response', {
        'status': 'connected',
        'client_id': client_id,
        'timestamp': datetime.now().isoformat()
    })

    # Broadcast to all
    emit('user_count', {
        'count': len(connected_users)
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    """클라이언트 연결 해제"""
    client_id = request.sid

    if client_id in connected_users:
        del connected_users[client_id]

    logger.info(f"Client disconnected: {client_id}")

    emit('user_count', {
        'count': len(connected_users)
    }, broadcast=True)

@socketio.on('join')
def handle_join(data):
    """방 참가"""
    room = data.get('room')
    username = data.get('username', 'Anonymous')
    client_id = request.sid

    join_room(room)

    if client_id in connected_users:
        connected_users[client_id]['rooms'].append(room)

    logger.info(f"Client {client_id} ({username}) joined room: {room}")

    emit('join_response', {
        'room': room,
        'message': f'{username} has joined the room'
    }, room=room)

    # Send room info
    emit('room_info', {
        'room': room,
        'members': len([u for u in connected_users.values() if room in u['rooms']])
    }, room=room)

@socketio.on('leave')
def handle_leave(data):
    """방 나가기"""
    room = data.get('room')
    username = data.get('username', 'Anonymous')
    client_id = request.sid

    leave_room(room)

    if client_id in connected_users and room in connected_users[client_id]['rooms']:
        connected_users[client_id]['rooms'].remove(room)

    logger.info(f"Client {client_id} ({username}) left room: {room}")

    emit('leave_response', {
        'room': room,
        'message': f'{username} has left the room'
    }, room=room)

@socketio.on('message')
def handle_message(data):
    """메시지 전송"""
    room = data.get('room')
    message = data.get('message')
    username = data.get('username', 'Anonymous')

    logger.info(f"Message from {username} in {room}: {message}")

    emit('new_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'room': room
    }, room=room)

@socketio.on('task_update')
def handle_task_update(data):
    """작업 업데이트 알림"""
    task_id = data.get('task_id')
    action = data.get('action')  # created, updated, deleted
    task_data = data.get('task')

    logger.info(f"Task {action}: {task_id}")

    emit('task_notification', {
        'action': action,
        'task_id': task_id,
        'task': task_data,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    """타이핑 표시"""
    room = data.get('room')
    username = data.get('username')
    is_typing = data.get('is_typing', True)

    emit('user_typing', {
        'username': username,
        'is_typing': is_typing
    }, room=room, include_self=False)

@socketio.on('ping')
def handle_ping():
    """Ping-pong for connection check"""
    emit('pong', {
        'timestamp': datetime.now().isoformat()
    })

def init_websocket(app):
    """Initialize WebSocket with Flask app"""
    socketio.init_app(app)
    return socketio

# Usage:
# from websocket.server import init_websocket, socketio
#
# app = Flask(__name__)
# socketio = init_websocket(app)
#
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000)
