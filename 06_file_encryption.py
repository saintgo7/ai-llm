"""
06. File Encryption - 파일 암호화/복호화 시스템
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class FileEncryption:
    def __init__(self, password=None):
        """
        파일 암호화 클래스 초기화

        Args:
            password: 암호화에 사용할 비밀번호 (없으면 자동 생성)
        """
        if password:
            self.key = self._generate_key_from_password(password)
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def _generate_key_from_password(self, password, salt=None):
        """비밀번호로부터 암호화 키 생성"""
        if salt is None:
            salt = b'default_salt_change_this'  # 실제로는 랜덤 salt 사용 권장

        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def save_key(self, filename='encryption.key'):
        """암호화 키를 파일로 저장"""
        with open(filename, 'wb') as key_file:
            key_file.write(self.key)
        print(f"Encryption key saved to {filename}")

    def load_key(self, filename='encryption.key'):
        """파일에서 암호화 키 로드"""
        with open(filename, 'rb') as key_file:
            self.key = key_file.read()
        self.cipher = Fernet(self.key)
        print(f"Encryption key loaded from {filename}")

    def encrypt_file(self, input_file, output_file=None):
        """파일 암호화"""
        try:
            # 입력 파일 읽기
            with open(input_file, 'rb') as f:
                file_data = f.read()

            # 데이터 암호화
            encrypted_data = self.cipher.encrypt(file_data)

            # 출력 파일명 설정
            if output_file is None:
                output_file = input_file + '.encrypted'

            # 암호화된 데이터 저장
            with open(output_file, 'wb') as f:
                f.write(encrypted_data)

            print(f"File encrypted: {input_file} -> {output_file}")
            return output_file
        except Exception as e:
            print(f"Encryption failed: {e}")
            return None

    def decrypt_file(self, input_file, output_file=None):
        """파일 복호화"""
        try:
            # 암호화된 파일 읽기
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()

            # 데이터 복호화
            decrypted_data = self.cipher.decrypt(encrypted_data)

            # 출력 파일명 설정
            if output_file is None:
                if input_file.endswith('.encrypted'):
                    output_file = input_file[:-10]  # .encrypted 제거
                else:
                    output_file = input_file + '.decrypted'

            # 복호화된 데이터 저장
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)

            print(f"File decrypted: {input_file} -> {output_file}")
            return output_file
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None

    def encrypt_text(self, text):
        """텍스트 암호화"""
        encrypted_text = self.cipher.encrypt(text.encode())
        return encrypted_text.decode()

    def decrypt_text(self, encrypted_text):
        """텍스트 복호화"""
        decrypted_text = self.cipher.decrypt(encrypted_text.encode())
        return decrypted_text.decode()

if __name__ == '__main__':
    # 예제 사용
    print("=== File Encryption Demo ===\n")

    # 1. 암호화 객체 생성
    encryptor = FileEncryption(password="my_secure_password")

    # 2. 테스트 파일 생성
    test_file = 'test_data.txt'
    with open(test_file, 'w') as f:
        f.write("This is sensitive data that needs to be encrypted!\n")
        f.write("It contains confidential information.")
    print(f"Created test file: {test_file}")

    # 3. 파일 암호화
    encrypted_file = encryptor.encrypt_file(test_file)

    # 4. 키 저장
    encryptor.save_key('my_encryption.key')

    # 5. 새로운 encryptor로 키 로드 및 복호화
    new_encryptor = FileEncryption()
    new_encryptor.load_key('my_encryption.key')
    decrypted_file = new_encryptor.decrypt_file(encrypted_file)

    # 6. 텍스트 암호화 예제
    print("\n=== Text Encryption Demo ===")
    original_text = "Secret message!"
    encrypted = encryptor.encrypt_text(original_text)
    print(f"Original: {original_text}")
    print(f"Encrypted: {encrypted[:50]}...")
    print(f"Decrypted: {encryptor.decrypt_text(encrypted)}")
