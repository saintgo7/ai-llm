"""
22. CSV Handler - CSV 파일 처리
"""
import csv
import json
from collections import defaultdict
import statistics

class CSVHandler:
    def __init__(self, filename=None):
        """CSV 핸들러 초기화"""
        self.filename = filename
        self.data = []
        self.headers = []

    def read(self, filename=None):
        """CSV 파일 읽기"""
        filename = filename or self.filename

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            self.data = list(reader)

        print(f"Loaded {len(self.data)} rows from {filename}")
        return self.data

    def write(self, data, filename, headers=None):
        """CSV 파일 쓰기"""
        if not data:
            print("No data to write")
            return

        if headers is None:
            headers = data[0].keys() if isinstance(data[0], dict) else None

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if headers:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(f)
                writer.writerows(data)

        print(f"Wrote {len(data)} rows to {filename}")

    def append_row(self, row):
        """행 추가"""
        if isinstance(row, dict):
            self.data.append(row)
        else:
            print("Row must be a dictionary")

    def filter_rows(self, condition):
        """
        조건에 맞는 행 필터링

        Args:
            condition: 함수 (행을 인자로 받아 bool 반환)
        """
        return [row for row in self.data if condition(row)]

    def sort_by_column(self, column, reverse=False):
        """특정 컬럼으로 정렬"""
        try:
            # 숫자로 변환 시도
            self.data.sort(key=lambda x: float(x[column]), reverse=reverse)
        except (ValueError, KeyError):
            # 문자열로 정렬
            self.data.sort(key=lambda x: x.get(column, ''), reverse=reverse)

        return self.data

    def get_column(self, column_name):
        """특정 컬럼의 모든 값 가져오기"""
        return [row.get(column_name) for row in self.data]

    def get_column_stats(self, column_name):
        """컬럼 통계 정보"""
        values = self.get_column(column_name)

        try:
            # 숫자 데이터로 변환
            numeric_values = [float(v) for v in values if v]

            return {
                'count': len(numeric_values),
                'mean': statistics.mean(numeric_values),
                'median': statistics.median(numeric_values),
                'stdev': statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0,
                'min': min(numeric_values),
                'max': max(numeric_values)
            }
        except (ValueError, TypeError):
            # 문자열 데이터
            return {
                'count': len(values),
                'unique': len(set(values)),
                'most_common': max(set(values), key=values.count)
            }

    def group_by(self, column):
        """컬럼으로 그룹화"""
        groups = defaultdict(list)

        for row in self.data:
            key = row.get(column)
            groups[key].append(row)

        return dict(groups)

    def aggregate(self, group_column, agg_column, func='sum'):
        """집계 함수 적용"""
        groups = self.group_by(group_column)
        result = {}

        for key, rows in groups.items():
            values = [float(row.get(agg_column, 0)) for row in rows if row.get(agg_column)]

            if func == 'sum':
                result[key] = sum(values)
            elif func == 'mean':
                result[key] = statistics.mean(values) if values else 0
            elif func == 'count':
                result[key] = len(values)
            elif func == 'min':
                result[key] = min(values) if values else 0
            elif func == 'max':
                result[key] = max(values) if values else 0

        return result

    def add_calculated_column(self, new_column, calculation_func):
        """계산된 컬럼 추가"""
        for row in self.data:
            row[new_column] = calculation_func(row)

        if new_column not in self.headers:
            self.headers.append(new_column)

    def remove_column(self, column_name):
        """컬럼 제거"""
        for row in self.data:
            if column_name in row:
                del row[column_name]

        if column_name in self.headers:
            self.headers.remove(column_name)

    def remove_duplicates(self, key_columns=None):
        """중복 행 제거"""
        if key_columns is None:
            # 모든 컬럼 기준
            seen = set()
            unique_data = []

            for row in self.data:
                row_tuple = tuple(sorted(row.items()))
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    unique_data.append(row)

            self.data = unique_data
        else:
            # 특정 컬럼 기준
            seen = set()
            unique_data = []

            for row in self.data:
                key = tuple(row.get(col) for col in key_columns)
                if key not in seen:
                    seen.add(key)
                    unique_data.append(row)

            self.data = unique_data

        print(f"Removed duplicates. {len(self.data)} unique rows remaining")

    def to_json(self, output_file):
        """JSON으로 변환"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        print(f"Data exported to {output_file}")

    def from_json(self, json_file):
        """JSON에서 로드"""
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        if self.data:
            self.headers = list(self.data[0].keys())

        print(f"Loaded {len(self.data)} rows from {json_file}")

    def print_summary(self):
        """데이터 요약 출력"""
        print(f"\n=== CSV Summary ===")
        print(f"Rows: {len(self.data)}")
        print(f"Columns: {len(self.headers)}")
        print(f"Headers: {', '.join(self.headers)}")

        if self.data:
            print("\nFirst 3 rows:")
            for i, row in enumerate(self.data[:3]):
                print(f"  Row {i+1}: {row}")

if __name__ == '__main__':
    # 예제 데이터 생성
    sample_data = [
        {'name': 'Alice', 'age': '30', 'city': 'New York', 'salary': '75000'},
        {'name': 'Bob', 'age': '25', 'city': 'San Francisco', 'salary': '85000'},
        {'name': 'Charlie', 'age': '35', 'city': 'New York', 'salary': '95000'},
        {'name': 'David', 'age': '28', 'city': 'Boston', 'salary': '70000'},
        {'name': 'Eve', 'age': '32', 'city': 'San Francisco', 'salary': '90000'},
    ]

    # CSV 쓰기
    csv_handler = CSVHandler()
    csv_handler.write(sample_data, 'employees.csv')

    # CSV 읽기
    csv_handler.read('employees.csv')
    csv_handler.print_summary()

    # 통계
    print("\n=== Salary Statistics ===")
    stats = csv_handler.get_column_stats('salary')
    for key, value in stats.items():
        print(f"{key}: {value}")

    # 그룹화
    print("\n=== Employees by City ===")
    groups = csv_handler.group_by('city')
    for city, employees in groups.items():
        print(f"{city}: {len(employees)} employees")

    # 집계
    print("\n=== Average Salary by City ===")
    avg_salaries = csv_handler.aggregate('city', 'salary', 'mean')
    for city, avg in avg_salaries.items():
        print(f"{city}: ${avg:,.2f}")

    # 계산된 컬럼 추가
    csv_handler.add_calculated_column('senior', lambda row: 'Yes' if int(row['age']) >= 30 else 'No')

    # 필터링
    seniors = csv_handler.filter_rows(lambda row: row['senior'] == 'Yes')
    print(f"\n=== Senior Employees ({len(seniors)}) ===")
    for emp in seniors:
        print(f"{emp['name']}, Age: {emp['age']}")

    # JSON 내보내기
    csv_handler.to_json('employees.json')
