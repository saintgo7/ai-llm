"""
04. JWT Authentication - JWT 토큰 기반 인증 시스템
"""
import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# 가상 사용자 데이터베이스
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'user': {'password': 'user123', 'role': 'user'}
}

def generate_token(username, role):
    """JWT 토큰 생성"""
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """토큰 인증 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Authorization 헤더에서 토큰 추출
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        # 토큰 검증
        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401

        # 현재 사용자 정보를 kwargs에 추가
        return f(payload, *args, **kwargs)

    return decorated

def admin_required(f):
    """관리자 권한 데코레이터"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    """로그인 엔드포인트"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(username, user['role'])

    return jsonify({
        'token': token,
        'username': username,
        'role': user['role']
    })

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    """보호된 라우트 (인증 필요)"""
    return jsonify({
        'message': 'This is a protected route',
        'user': current_user['username'],
        'role': current_user['role']
    })

@app.route('/api/admin', methods=['GET'])
@admin_required
def admin_route(current_user):
    """관리자 전용 라우트"""
    return jsonify({
        'message': 'This is an admin-only route',
        'user': current_user['username'],
        'role': current_user['role']
    })

if __name__ == '__main__':
    print("JWT Authentication Server starting...")
    print("Test credentials: admin/admin123 or user/user123")
    app.run(debug=True, port=5001)
