"""
04. JWT Authentication - JWT 토큰 기반 인증 시스템
Environment Variables, Logging, Enhanced Security
"""
import sys
import os
import jwt
import datetime
import hashlib
import logging
from functools import wraps
from flask import Flask, request, jsonify

# 상위 디렉토리의 config 모듈 import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import Config
except ImportError:
    class Config:
        JWT_SECRET_KEY = 'dev-jwt-secret-key'
        JWT_EXPIRATION_HOURS = 24
        LOG_LEVEL = 'INFO'

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.JWT_SECRET_KEY

def hash_password(password):
    """비밀번호를 SHA256으로 해싱"""
    return hashlib.sha256(password.encode()).hexdigest()

# 가상 사용자 데이터베이스 (비밀번호는 해시값으로 저장)
# 원본: admin123, user123
users = {
    'admin': {
        'password': hash_password('admin123'),
        'role': 'admin',
        'email': 'admin@example.com'
    },
    'user': {
        'password': hash_password('user123'),
        'role': 'user',
        'email': 'user@example.com'
    }
}

def generate_token(username, role):
    """JWT 토큰 생성"""
    expiration_hours = getattr(Config, 'JWT_EXPIRATION_HOURS', 24)
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    logger.info(f"Token generated for user: {username}")
    return token

def verify_token(token):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        logger.debug(f"Token verified for user: {payload.get('username')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
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
                logger.error("Invalid authorization header format")
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            logger.warning("Missing authorization token")
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
            logger.warning(f"Access denied for user: {current_user.get('username')}")
            return jsonify({'message': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    """로그인 엔드포인트"""
    logger.info("POST /api/login - Login attempt")

    # Content-Type 검증
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 400

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    # 입력 검증
    if not username or not password:
        logger.warning("Login failed: missing credentials")
        return jsonify({'message': 'Username and password required'}), 400

    if len(username) > 50:
        return jsonify({'message': 'Username too long'}), 400

    user = users.get(username)
    # 비밀번호를 해시하여 비교 (보안 개선)
    if not user or user['password'] != hash_password(password):
        logger.warning(f"Login failed for username: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(username, user['role'])
    logger.info(f"User logged in successfully: {username}")

    return jsonify({
        'token': token,
        'username': username,
        'role': user['role'],
        'email': user.get('email', '')
    })

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    """보호된 라우트 (인증 필요)"""
    logger.info(f"Protected route accessed by: {current_user['username']}")
    return jsonify({
        'message': 'This is a protected route',
        'user': current_user['username'],
        'role': current_user['role'],
        'timestamp': datetime.datetime.utcnow().isoformat()
    })

@app.route('/api/admin', methods=['GET'])
@admin_required
def admin_route(current_user):
    """관리자 전용 라우트"""
    logger.info(f"Admin route accessed by: {current_user['username']}")
    return jsonify({
        'message': 'This is an admin-only route',
        'user': current_user['username'],
        'role': current_user['role'],
        'users_count': len(users)
    })

@app.route('/api/verify', methods=['GET'])
@token_required
def verify_token_route(current_user):
    """토큰 검증 엔드포인트"""
    return jsonify({
        'valid': True,
        'user': current_user['username'],
        'role': current_user['role'],
        'expires_at': datetime.datetime.fromtimestamp(current_user['exp']).isoformat()
    })

if __name__ == '__main__':
    logger.info("JWT Authentication Server starting on port 5001")
    logger.info("Test credentials: admin/admin123 or user/user123")
    logger.info("Available endpoints:")
    logger.info("  POST /api/login     - Login and get JWT token")
    logger.info("  GET  /api/protected - Protected endpoint (requires token)")
    logger.info("  GET  /api/admin     - Admin-only endpoint")
    logger.info("  GET  /api/verify    - Verify JWT token")

    app.run(debug=True, port=5001)
