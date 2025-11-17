"""
33. CLI Tool - 명령줄 인터페이스 도구
"""
import argparse
import sys
from typing import Callable

class CLI:
    def __init__(self, name='app', description='Command line tool'):
        """CLI 도구 초기화"""
        self.name = name
        self.parser = argparse.ArgumentParser(
            prog=name,
            description=description
        )
        self.subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        self.commands = {}

    def command(self, name, help_text=''):
        """커맨드 데코레이터"""
        def decorator(func: Callable):
            # 서브파서 생성
            subparser = self.subparsers.add_parser(name, help=help_text)

            # 함수 저장
            self.commands[name] = {
                'func': func,
                'parser': subparser
            }

            # 함수에 인자 추가 메서드 연결
            func.add_argument = subparser.add_argument

            return func

        return decorator

    def run(self, argv=None):
        """CLI 실행"""
        args = self.parser.parse_args(argv)

        if not args.command:
            self.parser.print_help()
            return

        # 커맨드 실행
        command_info = self.commands.get(args.command)
        if command_info:
            try:
                command_info['func'](args)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

class ProgressBar:
    """진행 표시줄"""

    def __init__(self, total, prefix='', length=50):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.current = 0

    def update(self, amount=1):
        """진행 업데이트"""
        self.current += amount
        self.display()

    def display(self):
        """진행률 표시"""
        percent = self.current / self.total
        filled = int(self.length * percent)
        bar = '█' * filled + '-' * (self.length - filled)
        print(f'\r{self.prefix} |{bar}| {percent*100:.1f}%', end='', flush=True)

        if self.current >= self.total:
            print()  # 완료 시 줄바꿈

class Table:
    """테이블 출력"""

    @staticmethod
    def print(data, headers=None):
        """테이블 형식으로 출력"""
        if not data:
            return

        # 헤더 처리
        if headers is None and isinstance(data[0], dict):
            headers = list(data[0].keys())
            rows = [[str(row.get(h, '')) for h in headers] for row in data]
        else:
            rows = [[str(cell) for cell in row] for row in data]

        # 각 열의 최대 너비 계산
        if headers:
            col_widths = [len(h) for h in headers]
        else:
            col_widths = [0] * len(rows[0])

        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))

        # 구분선
        separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

        # 출력
        print(separator)

        if headers:
            header_row = '|' + '|'.join(f' {h:<{col_widths[i]}} ' for i, h in enumerate(headers)) + '|'
            print(header_row)
            print(separator)

        for row in rows:
            data_row = '|' + '|'.join(f' {cell:<{col_widths[i]}} ' for i, cell in enumerate(row)) + '|'
            print(data_row)

        print(separator)

# 사용 예제
if __name__ == '__main__':
    # CLI 생성
    cli = CLI(name='mytool', description='A sample CLI tool')

    # 커맨드 정의
    @cli.command('hello', help_text='Say hello')
    def hello(args):
        name = args.name or 'World'
        print(f"Hello, {name}!")

    hello.add_argument('--name', type=str, help='Name to greet')

    @cli.command('list', help_text='List items')
    def list_items(args):
        items = ['Item 1', 'Item 2', 'Item 3']

        if args.format == 'table':
            Table.print([[i+1, item] for i, item in enumerate(items)], ['#', 'Item'])
        else:
            for i, item in enumerate(items, 1):
                print(f"{i}. {item}")

    list_items.add_argument('--format', choices=['list', 'table'], default='list', help='Output format')

    @cli.command('progress', help_text='Show progress bar demo')
    def show_progress(args):
        import time

        total = args.steps
        progress = ProgressBar(total, prefix='Processing:', length=40)

        for i in range(total):
            time.sleep(0.1)
            progress.update()

    show_progress.add_argument('--steps', type=int, default=50, help='Number of steps')

    # CLI 실행
    print("=== CLI Tool Demo ===\n")
    print("Try these commands:")
    print("  python 33_cli_tool.py hello --name Alice")
    print("  python 33_cli_tool.py list --format table")
    print("  python 33_cli_tool.py progress --steps 30")
    print()

    # 데모
    cli.run(['hello', '--name', 'CLI User'])
    print()
    cli.run(['list', '--format', 'table'])
    print()
    cli.run(['progress', '--steps', '20'])
