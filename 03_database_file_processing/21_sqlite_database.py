"""
21. SQLite Database - SQLite 데이터베이스 관리
"""
import sqlite3
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_name='app.db'):
        """데이터베이스 매니저 초기화"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """데이터베이스 연결"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {self.db_name}")

    def disconnect(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def create_users_table(self):
        """사용자 테이블 생성"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        self.conn.commit()
        print("Users table created successfully")

    def create_posts_table(self):
        """게시물 테이블 생성"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()
        print("Posts table created successfully")

    def insert_user(self, username, email, password):
        """사용자 추가"""
        try:
            self.cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, password)
            )
            self.conn.commit()
            print(f"User '{username}' added successfully")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error adding user: {e}")
            return None

    def get_user(self, user_id=None, username=None):
        """사용자 조회"""
        if user_id:
            self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        elif username:
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        else:
            return None

        return self.cursor.fetchone()

    def get_all_users(self):
        """모든 사용자 조회"""
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def update_user(self, user_id, **kwargs):
        """사용자 정보 업데이트"""
        set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]

        query = f'UPDATE users SET {set_clause} WHERE id = ?'
        self.cursor.execute(query, values)
        self.conn.commit()
        print(f"User {user_id} updated successfully")

    def delete_user(self, user_id):
        """사용자 삭제"""
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        print(f"User {user_id} deleted successfully")

    def insert_post(self, user_id, title, content):
        """게시물 추가"""
        self.cursor.execute(
            'INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)',
            (user_id, title, content)
        )
        self.conn.commit()
        print(f"Post '{title}' added successfully")
        return self.cursor.lastrowid

    def get_posts_by_user(self, user_id):
        """특정 사용자의 게시물 조회"""
        self.cursor.execute(
            '''SELECT p.*, u.username
               FROM posts p
               JOIN users u ON p.user_id = u.id
               WHERE p.user_id = ?
               ORDER BY p.created_at DESC''',
            (user_id,)
        )
        return self.cursor.fetchall()

    def search_posts(self, keyword):
        """게시물 검색"""
        self.cursor.execute(
            '''SELECT p.*, u.username
               FROM posts p
               JOIN users u ON p.user_id = u.id
               WHERE p.title LIKE ? OR p.content LIKE ?
               ORDER BY p.created_at DESC''',
            (f'%{keyword}%', f'%{keyword}%')
        )
        return self.cursor.fetchall()

    def execute_custom_query(self, query, params=None):
        """사용자 정의 쿼리 실행"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        if query.strip().upper().startswith('SELECT'):
            return self.cursor.fetchall()
        else:
            self.conn.commit()
            return self.cursor.rowcount

    def backup_database(self, backup_file):
        """데이터베이스 백업"""
        backup_conn = sqlite3.connect(backup_file)
        self.conn.backup(backup_conn)
        backup_conn.close()
        print(f"Database backed up to {backup_file}")

    def export_to_json(self, table_name, output_file):
        """테이블을 JSON으로 내보내기"""
        self.cursor.execute(f'SELECT * FROM {table_name}')
        columns = [description[0] for description in self.cursor.description]
        rows = self.cursor.fetchall()

        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Table '{table_name}' exported to {output_file}")

    def get_table_info(self, table_name):
        """테이블 정보 조회"""
        self.cursor.execute(f'PRAGMA table_info({table_name})')
        return self.cursor.fetchall()

    def __enter__(self):
        """Context manager 진입"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 종료"""
        self.disconnect()

if __name__ == '__main__':
    # Context manager 사용
    with DatabaseManager('example.db') as db:
        # 테이블 생성
        db.create_users_table()
        db.create_posts_table()

        # 사용자 추가
        user1_id = db.insert_user('john_doe', 'john@example.com', 'hashed_password_1')
        user2_id = db.insert_user('jane_smith', 'jane@example.com', 'hashed_password_2')

        # 게시물 추가
        if user1_id:
            db.insert_post(user1_id, 'First Post', 'This is my first post!')
            db.insert_post(user1_id, 'Python Tutorial', 'Learn Python programming')

        if user2_id:
            db.insert_post(user2_id, 'Web Development', 'Building modern websites')

        # 사용자 조회
        print("\n=== All Users ===")
        users = db.get_all_users()
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")

        # 게시물 조회
        if user1_id:
            print(f"\n=== Posts by user {user1_id} ===")
            posts = db.get_posts_by_user(user1_id)
            for post in posts:
                print(f"Title: {post[2]}, Content: {post[3]}")

        # 검색
        print("\n=== Search posts with 'Python' ===")
        results = db.search_posts('Python')
        for result in results:
            print(f"Title: {result[2]}, Author: {result[6]}")

        # 백업
        db.backup_database('example_backup.db')

        # JSON 내보내기
        db.export_to_json('users', 'users_export.json')
