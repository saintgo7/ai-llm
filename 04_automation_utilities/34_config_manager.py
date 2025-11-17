"""
34. Config Manager - 설정 관리 시스템
"""
import json
import os
from pathlib import Path
import configparser

class ConfigManager:
    """JSON 기반 설정 관리"""

    def __init__(self, config_file='config.json', defaults=None):
        self.config_file = config_file
        self.config = defaults or {}
        self.load()

    def load(self):
        """설정 로드"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
            print(f"Config loaded from {self.config_file}")
        else:
            print(f"Config file not found, using defaults")

    def save(self):
        """설정 저장"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"Config saved to {self.config_file}")

    def get(self, key, default=None):
        """값 가져오기 (점 표기법 지원)"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def set(self, key, value):
        """값 설정 (점 표기법 지원)"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def delete(self, key):
        """키 삭제"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                return False
            config = config[k]

        if keys[-1] in config:
            del config[keys[-1]]
            return True

        return False

    def has(self, key):
        """키 존재 여부"""
        return self.get(key) is not None

    def to_dict(self):
        """딕셔너리로 반환"""
        return self.config.copy()

class INIConfig:
    """INI 파일 기반 설정"""

    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load()

    def load(self):
        """INI 파일 로드"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            print(f"INI config loaded from {self.config_file}")
        else:
            print("INI config file not found")

    def save(self):
        """INI 파일 저장"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
        print(f"INI config saved to {self.config_file}")

    def get(self, section, key, fallback=None):
        """값 가져오기"""
        return self.config.get(section, key, fallback=fallback)

    def set(self, section, key, value):
        """값 설정"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def get_section(self, section):
        """섹션 전체 가져오기"""
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}

class EnvConfig:
    """환경 변수 기반 설정"""

    @staticmethod
    def get(key, default=None, prefix='APP_'):
        """환경 변수 가져오기"""
        full_key = f"{prefix}{key}"
        return os.environ.get(full_key, default)

    @staticmethod
    def set(key, value, prefix='APP_'):
        """환경 변수 설정"""
        full_key = f"{prefix}{key}"
        os.environ[full_key] = str(value)

    @staticmethod
    def load_from_file(file_path='.env'):
        """파일에서 환경 변수 로드"""
        if not os.path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

        print(f"Environment variables loaded from {file_path}")

class Settings:
    """애플리케이션 설정 (싱글톤)"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = ConfigManager()
        return cls._instance

    def __getattr__(self, name):
        return self.config.get(name)

    def __setattr__(self, name, value):
        if name == 'config':
            super().__setattr__(name, value)
        else:
            self.config.set(name, value)

# 사용 예제
if __name__ == '__main__':
    print("=== JSON Config Manager ===")

    # 기본값 설정
    defaults = {
        'app': {
            'name': 'MyApp',
            'version': '1.0.0'
        },
        'database': {
            'host': 'localhost',
            'port': 5432
        }
    }

    config = ConfigManager('app_config.json', defaults)

    # 값 읽기
    print(f"App name: {config.get('app.name')}")
    print(f"DB host: {config.get('database.host')}")

    # 값 설정
    config.set('app.debug', True)
    config.set('database.username', 'admin')

    # 저장
    config.save()

    print("\n=== INI Config ===")

    # INI 설정
    ini_config = INIConfig('app.ini')
    ini_config.set('Server', 'host', 'localhost')
    ini_config.set('Server', 'port', '8080')
    ini_config.set('Logging', 'level', 'INFO')
    ini_config.save()

    print(f"Server section: {ini_config.get_section('Server')}")

    print("\n=== Environment Variables ===")

    # .env 파일 생성
    with open('.env', 'w') as f:
        f.write('APP_NAME=MyApp\n')
        f.write('APP_DEBUG=true\n')
        f.write('APP_SECRET_KEY=super-secret-key\n')

    # 환경 변수 로드
    EnvConfig.load_from_file('.env')
    print(f"APP_NAME: {EnvConfig.get('NAME')}")
    print(f"APP_DEBUG: {EnvConfig.get('DEBUG')}")

    print("\n=== Settings Singleton ===")

    settings = Settings()
    settings.theme = 'dark'
    settings.language = 'en'

    print(f"Theme: {settings.theme}")
    print(f"Language: {settings.language}")
