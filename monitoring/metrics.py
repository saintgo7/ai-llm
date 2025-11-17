"""
Prometheus Metrics for Flask Applications
"""
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import request, Response
import time
from functools import wraps

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

REQUEST_IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests in progress',
    ['method', 'endpoint']
)

TASK_COUNT = Gauge(
    'tasks_total',
    'Total number of tasks'
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

def setup_metrics(app):
    """Flask 앱에 metrics 설정"""

    @app.before_request
    def before_request():
        """요청 전 처리"""
        request._start_time = time.time()
        REQUEST_IN_PROGRESS.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).inc()

    @app.after_request
    def after_request(response):
        """요청 후 처리"""
        request_duration = time.time() - request._start_time

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).observe(request_duration)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()

        REQUEST_IN_PROGRESS.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).dec()

        return response

    @app.route('/metrics')
    def metrics():
        """Prometheus metrics 엔드포인트"""
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app

def track_time(metric):
    """시간 추적 데코레이터"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start
            metric.observe(duration)
            return result
        return wrapper
    return decorator

# 사용 예제:
# from monitoring.metrics import setup_metrics, TASK_COUNT
#
# app = Flask(__name__)
# setup_metrics(app)
#
# # 비즈니스 메트릭 업데이트
# TASK_COUNT.set(len(tasks))
