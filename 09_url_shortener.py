"""
09. URL Shortener - URL 단축 서비스
"""
import string
import random
from flask import Flask, request, jsonify, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

class URLShortener:
    def __init__(self, db_name='urls.db'):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def generate_short_code(self, length=6):
        """랜덤 단축 코드 생성"""
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(length))

            # 중복 확인
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT short_code FROM urls WHERE short_code = ?', (short_code,))

            if cursor.fetchone() is None:
                conn.close()
                return short_code

            conn.close()

    def create_short_url(self, original_url, custom_code=None):
        """URL 단축"""
        try:
            # URL 유효성 검사
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'https://' + original_url

            # 단축 코드 생성 또는 사용
            short_code = custom_code if custom_code else self.generate_short_code()

            # 데이터베이스에 저장
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
                (short_code, original_url)
            )

            conn.commit()
            conn.close()

            return {
                'success': True,
                'short_code': short_code,
                'original_url': original_url,
                'short_url': f'http://localhost:5002/{short_code}'
            }

        except sqlite3.IntegrityError:
            return {
                'success': False,
                'error': 'Custom code already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_original_url(self, short_code):
        """단축 코드로 원본 URL 조회"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT original_url FROM urls WHERE short_code = ?',
            (short_code,)
        )

        result = cursor.fetchone()

        if result:
            # 클릭 수 증가
            cursor.execute(
                'UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?',
                (short_code,)
            )
            conn.commit()

        conn.close()

        return result[0] if result else None

    def get_stats(self, short_code):
        """단축 URL 통계 조회"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT short_code, original_url, created_at, clicks
               FROM urls WHERE short_code = ?''',
            (short_code,)
        )

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'short_code': result[0],
                'original_url': result[1],
                'created_at': result[2],
                'clicks': result[3]
            }
        return None

    def get_all_urls(self, limit=100):
        """모든 단축 URL 조회"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(
            '''SELECT short_code, original_url, created_at, clicks
               FROM urls ORDER BY created_at DESC LIMIT ?''',
            (limit,)
        )

        results = cursor.fetchall()
        conn.close()

        return [
            {
                'short_code': row[0],
                'original_url': row[1],
                'created_at': row[2],
                'clicks': row[3]
            }
            for row in results
        ]

# Flask 앱 설정
shortener = URLShortener()

@app.route('/')
def index():
    """홈페이지"""
    return jsonify({
        'service': 'URL Shortener',
        'endpoints': {
            'create': 'POST /api/shorten',
            'redirect': 'GET /<short_code>',
            'stats': 'GET /api/stats/<short_code>',
            'list': 'GET /api/urls'
        }
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """URL 단축 API"""
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    original_url = data['url']
    custom_code = data.get('custom_code')

    result = shortener.create_short_url(original_url, custom_code)

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """단축 URL로 리다이렉트"""
    original_url = shortener.get_original_url(short_code)

    if original_url:
        return redirect(original_url)
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/api/stats/<short_code>')
def get_url_stats(short_code):
    """URL 통계 조회"""
    stats = shortener.get_stats(short_code)

    if stats:
        return jsonify(stats)
    else:
        return jsonify({'error': 'URL not found'}), 404

@app.route('/api/urls')
def list_urls():
    """모든 URL 목록"""
    urls = shortener.get_all_urls()
    return jsonify({'urls': urls, 'count': len(urls)})

if __name__ == '__main__':
    print("URL Shortener starting on http://localhost:5002")
    print("\nExample usage:")
    print("curl -X POST http://localhost:5002/api/shorten -H 'Content-Type: application/json' -d '{\"url\":\"https://example.com\"}'")
    app.run(debug=True, port=5002)
