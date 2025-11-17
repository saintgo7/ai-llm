"""
39. Notification System - 알림 시스템
"""
import os
import platform
import subprocess
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DesktopNotification:
    """데스크톱 알림"""

    @staticmethod
    def show(title, message, duration=5):
        """OS별 데스크톱 알림 표시"""
        system = platform.system()

        try:
            if system == 'Darwin':  # macOS
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(['osascript', '-e', script])

            elif system == 'Linux':
                subprocess.run(['notify-send', title, message])

            elif system == 'Windows':
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=duration)
                except ImportError:
                    print(f"[{title}] {message}")
                    print("Install win10toast: pip install win10toast")

            print(f"Desktop notification sent: {title}")
            return True

        except Exception as e:
            print(f"Failed to send desktop notification: {e}")
            return False

class EmailNotification:
    """이메일 알림"""

    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, to_email, subject, body, html=False):
        """이메일 알림 발송"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject

            if html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')

            msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            print(f"Email notification sent to {to_email}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

class SlackNotification:
    """Slack 알림"""

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, message, channel=None, username='Bot'):
        """Slack 알림 발송"""
        try:
            import requests

            payload = {
                'text': message,
                'username': username
            }

            if channel:
                payload['channel'] = channel

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("Slack notification sent")
                return True
            else:
                print(f"Slack notification failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"Failed to send Slack notification: {e}")
            return False

class NotificationManager:
    """통합 알림 관리자"""

    def __init__(self):
        self.channels = {
            'desktop': DesktopNotification(),
            'email': None,
            'slack': None
        }
        self.notifications_log = []

    def add_email_channel(self, smtp_server, smtp_port, username, password):
        """이메일 채널 추가"""
        self.channels['email'] = EmailNotification(smtp_server, smtp_port, username, password)

    def add_slack_channel(self, webhook_url):
        """Slack 채널 추가"""
        self.channels['slack'] = SlackNotification(webhook_url)

    def send(self, title, message, channels=['desktop'], **kwargs):
        """여러 채널로 알림 발송"""
        results = {}

        for channel in channels:
            if channel not in self.channels or self.channels[channel] is None:
                print(f"Channel '{channel}' not configured")
                continue

            if channel == 'desktop':
                results[channel] = self.channels[channel].show(title, message)

            elif channel == 'email':
                to_email = kwargs.get('to_email')
                if to_email:
                    results[channel] = self.channels[channel].send(
                        to_email, title, message,
                        html=kwargs.get('html', False)
                    )

            elif channel == 'slack':
                results[channel] = self.channels[channel].send(
                    f"*{title}*\n{message}",
                    channel=kwargs.get('slack_channel'),
                    username=kwargs.get('slack_username', 'Bot')
                )

        # 로그 저장
        self.notifications_log.append({
            'timestamp': datetime.now(),
            'title': title,
            'message': message,
            'channels': channels,
            'results': results
        })

        return results

    def get_log(self, limit=10):
        """알림 로그 조회"""
        return self.notifications_log[-limit:]

class AlertManager:
    """조건 기반 알림"""

    def __init__(self, notifier):
        self.notifier = notifier
        self.alerts = {}

    def add_alert(self, name, condition, title, message, channels=['desktop']):
        """알림 규칙 추가"""
        self.alerts[name] = {
            'condition': condition,
            'title': title,
            'message': message,
            'channels': channels,
            'triggered': False
        }

    def check_alerts(self, context=None):
        """알림 조건 체크"""
        triggered_alerts = []

        for name, alert in self.alerts.items():
            try:
                # 조건 함수 실행
                if callable(alert['condition']):
                    if context:
                        result = alert['condition'](context)
                    else:
                        result = alert['condition']()

                    if result and not alert['triggered']:
                        self.notifier.send(
                            alert['title'],
                            alert['message'],
                            channels=alert['channels']
                        )
                        alert['triggered'] = True
                        triggered_alerts.append(name)
                    elif not result:
                        alert['triggered'] = False

            except Exception as e:
                print(f"Error checking alert '{name}': {e}")

        return triggered_alerts

# 사용 예제
if __name__ == '__main__':
    print("=== Notification System Demo ===\n")

    # 데스크톱 알림
    print("1. Desktop Notification")
    DesktopNotification.show(
        "Test Notification",
        "This is a test message from the notification system!"
    )

    # 알림 관리자
    print("\n2. Notification Manager")
    manager = NotificationManager()

    # 데스크톱 알림
    manager.send(
        "Welcome",
        "Notification system is ready!",
        channels=['desktop']
    )

    # 이메일 채널 설정 (예제)
    # manager.add_email_channel(
    #     smtp_server='smtp.gmail.com',
    #     smtp_port=587,
    #     username='your-email@gmail.com',
    #     password='your-app-password'
    # )
    #
    # manager.send(
    #     "Alert",
    #     "This is an email alert!",
    #     channels=['desktop', 'email'],
    #     to_email='recipient@example.com'
    # )

    # Slack 채널 설정 (예제)
    # manager.add_slack_channel('https://hooks.slack.com/services/YOUR/WEBHOOK/URL')
    # manager.send(
    #     "Deployment",
    #     "Application deployed successfully!",
    #     channels=['desktop', 'slack']
    # )

    # 조건 기반 알림
    print("\n3. Alert Manager (Condition-based)")
    alert_mgr = AlertManager(manager)

    # CPU 사용률 알림 (데모)
    def check_cpu():
        import psutil
        return psutil.cpu_percent(interval=1) > 50

    alert_mgr.add_alert(
        'high_cpu',
        check_cpu,
        'High CPU Usage',
        'CPU usage exceeded 50%',
        channels=['desktop']
    )

    # 알림 체크
    print("Checking alerts...")
    triggered = alert_mgr.check_alerts()
    if triggered:
        print(f"Triggered alerts: {triggered}")
    else:
        print("No alerts triggered")

    # 알림 로그
    print("\n4. Notification Log")
    log = manager.get_log()
    for entry in log:
        print(f"[{entry['timestamp'].strftime('%H:%M:%S')}] {entry['title']}: {entry['message']}")

    print("\nNote: Install requirements:")
    print("  pip install win10toast (Windows)")
    print("  pip install requests (for Slack)")
