"""
05. Email Sender - SMTP를 이용한 이메일 발송 시스템
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

class EmailSender:
    def __init__(self, smtp_server, smtp_port, username, password):
        """
        이메일 발송 클래스 초기화

        Args:
            smtp_server: SMTP 서버 주소 (예: smtp.gmail.com)
            smtp_port: SMTP 포트 (보통 587 for TLS)
            username: 이메일 계정
            password: 이메일 비밀번호 또는 앱 비밀번호
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_simple_email(self, to_email, subject, body):
        """간단한 텍스트 이메일 발송"""
        try:
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_html_email(self, to_email, subject, html_body):
        """HTML 이메일 발송"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"HTML email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send HTML email: {e}")
            return False

    def send_email_with_attachment(self, to_email, subject, body, file_path):
        """첨부파일이 있는 이메일 발송"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

            # 본문 추가
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 첨부파일 추가
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                with open(file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {filename}')
                msg.attach(part)
            else:
                print(f"Attachment file not found: {file_path}")
                return False

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"Email with attachment sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email with attachment: {e}")
            return False

    def send_bulk_email(self, recipients, subject, body):
        """여러 수신자에게 이메일 발송"""
        success_count = 0
        fail_count = 0

        for recipient in recipients:
            if self.send_simple_email(recipient, subject, body):
                success_count += 1
            else:
                fail_count += 1

        print(f"\nBulk email complete: {success_count} sent, {fail_count} failed")
        return success_count, fail_count

if __name__ == '__main__':
    # 예제 사용 (실제 사용시 환경변수 등으로 관리)
    sender = EmailSender(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        username='your-email@gmail.com',
        password='your-app-password'
    )

    # 간단한 이메일 발송 예제
    # sender.send_simple_email(
    #     to_email='recipient@example.com',
    #     subject='Test Email',
    #     body='This is a test email from Python!'
    # )

    # HTML 이메일 발송 예제
    html_content = """
    <html>
        <body>
            <h1>Hello!</h1>
            <p>This is an <strong>HTML email</strong> sent from Python.</p>
        </body>
    </html>
    """
    # sender.send_html_email(
    #     to_email='recipient@example.com',
    #     subject='HTML Test Email',
    #     html_body=html_content
    # )

    print("Email sender initialized. Update credentials to use.")
