"""
10. Password Manager - 비밀번호 관리 시스템
"""
import json
import hashlib
import secrets
import string
from datetime import datetime
from cryptography.fernet import Fernet
from getpass import getpass
import os

class PasswordManager:
    def __init__(self, master_password):
        """
        비밀번호 관리자 초기화

        Args:
            master_password: 마스터 비밀번호
        """
        self.master_password = master_password
        self.key = self._generate_key(master_password)
        self.cipher = Fernet(self.key)
        self.password_file = 'passwords.encrypted'
        self.passwords = self._load_passwords()

    def _generate_key(self, password):
        """마스터 비밀번호로부터 암호화 키 생성"""
        # SHA256 해시를 사용하여 키 생성
        key = hashlib.sha256(password.encode()).digest()
        # Fernet 키 형식으로 변환
        from base64 import urlsafe_b64encode
        return urlsafe_b64encode(key)

    def _load_passwords(self):
        """저장된 비밀번호 로드"""
        if not os.path.exists(self.password_file):
            return {}

        try:
            with open(self.password_file, 'rb') as f:
                encrypted_data = f.read()

            if not encrypted_data:
                return {}

            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading passwords: {e}")
            return {}

    def _save_passwords(self):
        """비밀번호를 파일에 저장"""
        try:
            json_data = json.dumps(self.passwords, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())

            with open(self.password_file, 'wb') as f:
                f.write(encrypted_data)

            return True
        except Exception as e:
            print(f"Error saving passwords: {e}")
            return False

    def generate_password(self, length=16, use_special=True):
        """
        강력한 랜덤 비밀번호 생성

        Args:
            length: 비밀번호 길이
            use_special: 특수문자 포함 여부
        """
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += string.punctuation

        # 최소 요구사항 보장
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
        ]

        if use_special:
            password.append(secrets.choice(string.punctuation))

        # 나머지 길이 채우기
        remaining_length = length - len(password)
        password.extend(secrets.choice(characters) for _ in range(remaining_length))

        # 섞기
        secrets.SystemRandom().shuffle(password)

        return ''.join(password)

    def add_password(self, service, username, password=None, notes=''):
        """
        새 비밀번호 추가

        Args:
            service: 서비스 이름 (예: 'gmail', 'github')
            username: 사용자명/이메일
            password: 비밀번호 (None이면 자동 생성)
            notes: 추가 메모
        """
        if password is None:
            password = self.generate_password()
            print(f"Generated password: {password}")

        self.passwords[service] = {
            'username': username,
            'password': password,
            'notes': notes,
            'created_at': str(datetime.now()),
            'modified_at': str(datetime.now())
        }

        if self._save_passwords():
            print(f"Password for {service} saved successfully!")
            return True
        return False

    def get_password(self, service):
        """비밀번호 조회"""
        if service in self.passwords:
            return self.passwords[service]
        return None

    def update_password(self, service, password=None, username=None, notes=None):
        """비밀번호 업데이트"""
        if service not in self.passwords:
            print(f"Service '{service}' not found!")
            return False

        if password:
            self.passwords[service]['password'] = password
        if username:
            self.passwords[service]['username'] = username
        if notes is not None:
            self.passwords[service]['notes'] = notes

        self.passwords[service]['modified_at'] = str(datetime.now())

        if self._save_passwords():
            print(f"Password for {service} updated successfully!")
            return True
        return False

    def delete_password(self, service):
        """비밀번호 삭제"""
        if service in self.passwords:
            del self.passwords[service]
            if self._save_passwords():
                print(f"Password for {service} deleted successfully!")
                return True
        else:
            print(f"Service '{service}' not found!")
        return False

    def list_services(self):
        """모든 서비스 목록"""
        return list(self.passwords.keys())

    def search_passwords(self, query):
        """비밀번호 검색"""
        results = {}
        query_lower = query.lower()

        for service, data in self.passwords.items():
            if (query_lower in service.lower() or
                query_lower in data['username'].lower() or
                query_lower in data.get('notes', '').lower()):
                results[service] = data

        return results

    def check_password_strength(self, password):
        """비밀번호 강도 검사"""
        score = 0
        feedback = []

        # 길이 체크
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("비밀번호가 너무 짧습니다 (최소 8자 권장)")

        # 대문자 포함
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("대문자를 포함하세요")

        # 소문자 포함
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("소문자를 포함하세요")

        # 숫자 포함
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("숫자를 포함하세요")

        # 특수문자 포함
        if any(c in string.punctuation for c in password):
            score += 1
        else:
            feedback.append("특수문자를 포함하세요")

        # 강도 평가
        if score >= 6:
            strength = "강함"
        elif score >= 4:
            strength = "보통"
        else:
            strength = "약함"

        return {
            'score': score,
            'strength': strength,
            'feedback': feedback
        }

    def export_passwords(self, filename='passwords_backup.json'):
        """비밀번호 백업 (평문 - 주의!)"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.passwords, f, indent=2)
            print(f"Passwords exported to {filename}")
            print("WARNING: This file contains unencrypted passwords!")
            return True
        except Exception as e:
            print(f"Error exporting passwords: {e}")
            return False

def main():
    """CLI 인터페이스"""
    print("=== Password Manager ===\n")

    # 마스터 비밀번호 입력
    master_password = getpass("Enter master password: ")

    if not master_password:
        print("Master password cannot be empty!")
        return

    pm = PasswordManager(master_password)

    while True:
        print("\n=== Menu ===")
        print("1. Add password")
        print("2. Get password")
        print("3. Update password")
        print("4. Delete password")
        print("5. List all services")
        print("6. Search passwords")
        print("7. Generate password")
        print("8. Check password strength")
        print("9. Export passwords")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == '1':
            service = input("Service name: ").strip()
            username = input("Username/Email: ").strip()
            password = getpass("Password (leave empty to generate): ").strip()
            notes = input("Notes (optional): ").strip()

            pm.add_password(
                service,
                username,
                password if password else None,
                notes
            )

        elif choice == '2':
            service = input("Service name: ").strip()
            data = pm.get_password(service)

            if data:
                print(f"\nService: {service}")
                print(f"Username: {data['username']}")
                print(f"Password: {data['password']}")
                print(f"Notes: {data.get('notes', 'N/A')}")
            else:
                print(f"Service '{service}' not found!")

        elif choice == '3':
            service = input("Service name: ").strip()
            if pm.get_password(service):
                password = getpass("New password (leave empty to skip): ").strip()
                username = input("New username (leave empty to skip): ").strip()
                notes = input("New notes (leave empty to skip): ").strip()

                pm.update_password(
                    service,
                    password if password else None,
                    username if username else None,
                    notes if notes else None
                )
            else:
                print(f"Service '{service}' not found!")

        elif choice == '4':
            service = input("Service name: ").strip()
            confirm = input(f"Delete password for '{service}'? (y/n): ").lower()
            if confirm == 'y':
                pm.delete_password(service)

        elif choice == '5':
            services = pm.list_services()
            if services:
                print(f"\nStored services ({len(services)}):")
                for service in sorted(services):
                    print(f"  - {service}")
            else:
                print("No passwords stored yet!")

        elif choice == '6':
            query = input("Search query: ").strip()
            results = pm.search_passwords(query)

            if results:
                print(f"\nFound {len(results)} results:")
                for service in results:
                    print(f"  - {service}")
            else:
                print("No results found!")

        elif choice == '7':
            length = int(input("Password length (default 16): ") or "16")
            special = input("Include special characters? (y/n, default y): ").lower() != 'n'
            password = pm.generate_password(length, special)
            print(f"\nGenerated password: {password}")

        elif choice == '8':
            password = getpass("Password to check: ")
            result = pm.check_password_strength(password)
            print(f"\nStrength: {result['strength']} (Score: {result['score']}/7)")
            if result['feedback']:
                print("Suggestions:")
                for suggestion in result['feedback']:
                    print(f"  - {suggestion}")

        elif choice == '9':
            filename = input("Export filename (default: passwords_backup.json): ").strip()
            pm.export_passwords(filename if filename else 'passwords_backup.json')

        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid option!")

if __name__ == '__main__':
    main()
