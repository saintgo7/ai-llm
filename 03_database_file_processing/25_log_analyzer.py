"""
25. Log Analyzer - 로그 파일 분석기
"""
import re
from collections import Counter, defaultdict
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.logs = []
        self.patterns = {
            'apache': r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)',
            'nginx': r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"',
            'error': r'\[(\w+)\] \[(.*?)\] (.*)'
        }

    def load_logs(self, file_path=None):
        """로그 파일 로드"""
        file_path = file_path or self.log_file

        with open(file_path, 'r') as f:
            self.logs = f.readlines()

        print(f"Loaded {len(self.logs)} log entries")
        return self.logs

    def parse_apache_log(self, log_line):
        """Apache 로그 파싱"""
        match = re.match(self.patterns['apache'], log_line)
        if match:
            return {
                'ip': match.group(1),
                'timestamp': match.group(2),
                'request': match.group(3),
                'status': int(match.group(4)),
                'size': int(match.group(5))
            }
        return None

    def count_status_codes(self):
        """HTTP 상태 코드별 카운트"""
        status_codes = Counter()

        for log in self.logs:
            parsed = self.parse_apache_log(log)
            if parsed:
                status_codes[parsed['status']] += 1

        return dict(status_codes)

    def count_ips(self):
        """IP 주소별 요청 수"""
        ips = Counter()

        for log in self.logs:
            parsed = self.parse_apache_log(log)
            if parsed:
                ips[parsed['ip']] += 1

        return dict(ips.most_common(10))

    def find_errors(self, status_code=500):
        """에러 로그 찾기"""
        errors = []

        for log in self.logs:
            parsed = self.parse_apache_log(log)
            if parsed and parsed['status'] >= status_code:
                errors.append(parsed)

        return errors

    def analyze_bandwidth(self):
        """대역폭 사용량 분석"""
        total_bytes = 0
        count = 0

        for log in self.logs:
            parsed = self.parse_apache_log(log)
            if parsed:
                total_bytes += parsed['size']
                count += 1

        return {
            'total_bytes': total_bytes,
            'total_mb': total_bytes / (1024 * 1024),
            'average_bytes': total_bytes / count if count > 0 else 0
        }

    def get_popular_endpoints(self, top_n=10):
        """인기 엔드포인트"""
        endpoints = Counter()

        for log in self.logs:
            parsed = self.parse_apache_log(log)
            if parsed:
                request_parts = parsed['request'].split()
                if len(request_parts) >= 2:
                    endpoints[request_parts[1]] += 1

        return dict(endpoints.most_common(top_n))

    def generate_report(self):
        """종합 리포트 생성"""
        report = []
        report.append("=== LOG ANALYSIS REPORT ===\n")
        report.append(f"Total Logs: {len(self.logs)}\n")

        # Status codes
        report.append("\n--- Status Codes ---")
        for code, count in self.count_status_codes().items():
            report.append(f"{code}: {count}")

        # Top IPs
        report.append("\n--- Top 5 IPs ---")
        for ip, count in list(self.count_ips().items())[:5]:
            report.append(f"{ip}: {count} requests")

        # Bandwidth
        bandwidth = self.analyze_bandwidth()
        report.append(f"\n--- Bandwidth ---")
        report.append(f"Total: {bandwidth['total_mb']:.2f} MB")
        report.append(f"Average: {bandwidth['average_bytes']:.2f} bytes")

        # Popular endpoints
        report.append("\n--- Top 5 Endpoints ---")
        for endpoint, count in list(self.get_popular_endpoints(5).items()):
            report.append(f"{endpoint}: {count}")

        return '\n'.join(report)

if __name__ == '__main__':
    # 샘플 로그 데이터 생성
    sample_logs = [
        '192.168.1.1 - - [01/Jan/2024:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024',
        '192.168.1.2 - - [01/Jan/2024:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 2048',
        '192.168.1.1 - - [01/Jan/2024:10:00:02 +0000] "POST /api/login HTTP/1.1" 200 512',
        '192.168.1.3 - - [01/Jan/2024:10:00:03 +0000] "GET /api/data HTTP/1.1" 404 256',
        '192.168.1.1 - - [01/Jan/2024:10:00:04 +0000] "GET /index.html HTTP/1.1" 200 1024',
    ]

    with open('sample.log', 'w') as f:
        f.write('\n'.join(sample_logs))

    # 분석
    analyzer = LogAnalyzer('sample.log')
    analyzer.load_logs()

    print(analyzer.generate_report())
