"""
Configuration Management - 환경 변수 및 설정 관리
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """애플리케이션 설정 클래스"""

    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'app.db')

    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '5000'))

    # JWT Settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))

    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

    # Security
    PASSWORD_HASH_ALGORITHM = os.getenv('PASSWORD_HASH_ALGORITHM', 'sha256')
    ENABLE_RATE_LIMITING = os.getenv('ENABLE_RATE_LIMITING', 'True').lower() == 'true'
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    ENABLE_FILE_LOGGING = os.getenv('ENABLE_FILE_LOGGING', 'True').lower() == 'true'

    # Web Scraping
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))

    # Selenium
    SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'True').lower() == 'true'
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')

    # File Storage
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif,pdf,txt,csv').split(',')

    # Encryption
    ENCRYPTION_KEY_SIZE = int(os.getenv('ENCRYPTION_KEY_SIZE', '32'))

    # Backup
    BACKUP_DIRECTORY = os.getenv('BACKUP_DIRECTORY', './backups')
    BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))

    # Development
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'

    @classmethod
    def get(cls, key, default=None):
        """설정 값 가져오기"""
        return getattr(cls, key, default)

    @classmethod
    def is_production(cls):
        """프로덕션 환경 여부"""
        return cls.FLASK_ENV == 'production'

    @classmethod
    def is_development(cls):
        """개발 환경 여부"""
        return cls.FLASK_ENV == 'development'

# 전역 config 인스턴스
config = Config()

if __name__ == '__main__':
    print("=== Configuration Settings ===")
    print(f"Environment: {Config.FLASK_ENV}")
    print(f"Debug Mode: {Config.DEBUG_MODE}")
    print(f"Secret Key: {'*' * len(Config.SECRET_KEY)}")
    print(f"Database: {Config.DATABASE_URL}")
    print(f"API Port: {Config.API_PORT}")
    print(f"Log Level: {Config.LOG_LEVEL}")
    print(f"Is Production: {Config.is_production()}")
