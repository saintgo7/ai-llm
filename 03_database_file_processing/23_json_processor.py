"""
23. JSON Processor - JSON 데이터 처리
"""
import json
import os
from collections import OrderedDict

class JSONProcessor:
    def __init__(self, file_path=None):
        """JSON 프로세서 초기화"""
        self.file_path = file_path
        self.data = None

    def load(self, file_path=None):
        """JSON 파일 로드"""
        file_path = file_path or self.file_path

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        print(f"Loaded JSON from {file_path}")
        return self.data

    def save(self, data=None, file_path=None, indent=2):
        """JSON 파일 저장"""
        data = data or self.data
        file_path = file_path or self.file_path

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        print(f"Saved JSON to {file_path}")

    def pretty_print(self, data=None):
        """JSON 데이터를 보기 좋게 출력"""
        data = data or self.data
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def get_value(self, path, data=None):
        """
        경로로 값 가져오기

        Args:
            path: 점(.)으로 구분된 경로 (예: "user.address.city")
            data: 검색할 데이터 (None이면 self.data 사용)

        Returns:
            찾은 값 또는 None
        """
        data = data or self.data
        keys = path.split('.')

        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            elif isinstance(data, list) and key.isdigit():
                index = int(key)
                data = data[index] if 0 <= index < len(data) else None
            else:
                return None

            if data is None:
                return None

        return data

    def set_value(self, path, value, data=None):
        """
        경로로 값 설정

        Args:
            path: 점(.)으로 구분된 경로
            value: 설정할 값
            data: 수정할 데이터
        """
        data = data or self.data
        keys = path.split('.')

        for key in keys[:-1]:
            if key not in data:
                data[key] = {}
            data = data[key]

        data[keys[-1]] = value

    def delete_key(self, path, data=None):
        """경로로 키 삭제"""
        data = data or self.data
        keys = path.split('.')

        for key in keys[:-1]:
            if key in data:
                data = data[key]
            else:
                return False

        if keys[-1] in data:
            del data[keys[-1]]
            return True

        return False

    def search(self, key, data=None):
        """
        재귀적으로 키 검색

        Returns:
            모든 일치하는 값의 리스트
        """
        data = data or self.data
        results = []

        def search_recursive(obj, target_key):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == target_key:
                        results.append(v)
                    search_recursive(v, target_key)
            elif isinstance(obj, list):
                for item in obj:
                    search_recursive(item, target_key)

        search_recursive(data, key)
        return results

    def merge(self, other_data):
        """JSON 데이터 병합"""
        def merge_recursive(dict1, dict2):
            result = dict1.copy()

            for key, value in dict2.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_recursive(result[key], value)
                else:
                    result[key] = value

            return result

        self.data = merge_recursive(self.data, other_data)
        return self.data

    def flatten(self, data=None, parent_key='', sep='_'):
        """
        중첩된 JSON을 평탄화

        Returns:
            평탄화된 딕셔너리
        """
        data = data or self.data
        items = []

        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self.flatten(item, f"{new_key}{sep}{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}{sep}{i}", item))
            else:
                items.append((new_key, v))

        return dict(items)

    def unflatten(self, flat_data, sep='_'):
        """
        평탄화된 딕셔너리를 중첩 구조로 변환

        Args:
            flat_data: 평탄화된 딕셔너리
            sep: 구분자

        Returns:
            중첩된 딕셔너리
        """
        result = {}

        for key, value in flat_data.items():
            parts = key.split(sep)
            current = result

            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            current[parts[-1]] = value

        return result

    def validate_schema(self, schema):
        """
        간단한 스키마 검증

        Args:
            schema: 필수 키들의 딕셔너리 (예: {"name": str, "age": int})

        Returns:
            검증 성공 여부
        """
        def validate_recursive(data, schema):
            if not isinstance(data, dict):
                return False

            for key, expected_type in schema.items():
                if key not in data:
                    print(f"Missing key: {key}")
                    return False

                if not isinstance(data[key], expected_type):
                    print(f"Invalid type for {key}: expected {expected_type}, got {type(data[key])}")
                    return False

            return True

        return validate_recursive(self.data, schema)

    def filter_keys(self, keys_to_keep):
        """특정 키만 유지"""
        def filter_recursive(data):
            if isinstance(data, dict):
                return {k: filter_recursive(v) for k, v in data.items() if k in keys_to_keep}
            elif isinstance(data, list):
                return [filter_recursive(item) for item in data]
            else:
                return data

        self.data = filter_recursive(self.data)
        return self.data

    def transform(self, transformer_func):
        """
        변환 함수 적용

        Args:
            transformer_func: 딕셔너리를 받아 변환된 딕셔너리를 반환하는 함수
        """
        self.data = transformer_func(self.data)
        return self.data

    def to_csv(self, output_file):
        """JSON을 CSV로 변환 (평탄한 구조만)"""
        import csv

        if not isinstance(self.data, list):
            raise ValueError("Data must be a list of objects")

        if not self.data:
            print("No data to export")
            return

        # 평탄화
        flat_data = [self.flatten(item) for item in self.data]

        # CSV 작성
        headers = set()
        for item in flat_data:
            headers.update(item.keys())

        headers = sorted(headers)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(flat_data)

        print(f"JSON exported to CSV: {output_file}")

if __name__ == '__main__':
    # 샘플 JSON 데이터
    sample_data = {
        "company": "TechCorp",
        "employees": [
            {
                "name": "Alice",
                "age": 30,
                "position": "Developer",
                "address": {
                    "city": "New York",
                    "country": "USA"
                }
            },
            {
                "name": "Bob",
                "age": 25,
                "position": "Designer",
                "address": {
                    "city": "San Francisco",
                    "country": "USA"
                }
            }
        ],
        "founded": 2010
    }

    # JSON 저장 및 로드
    jp = JSONProcessor('sample.json')
    jp.save(sample_data)

    # 로드
    jp.load('sample.json')
    print("=== Original Data ===")
    jp.pretty_print()

    # 값 가져오기
    print("\n=== Get Value ===")
    print(f"Company: {jp.get_value('company')}")
    print(f"First employee name: {jp.get_value('employees.0.name')}")
    print(f"First employee city: {jp.get_value('employees.0.address.city')}")

    # 값 설정
    jp.set_value('company', 'NewTechCorp')
    jp.set_value('employees.0.salary', 75000)
    print("\n=== After Setting Values ===")
    print(f"Company: {jp.get_value('company')}")
    print(f"First employee salary: {jp.get_value('employees.0.salary')}")

    # 검색
    print("\n=== Search for 'name' ===")
    names = jp.search('name')
    print(f"Found names: {names}")

    # 평탄화
    print("\n=== Flattened Data ===")
    flat = jp.flatten()
    for key, value in list(flat.items())[:5]:
        print(f"{key}: {value}")

    # 병합
    additional_data = {
        "revenue": 1000000,
        "employees": [{"bonus": 5000}]
    }
    jp.merge(additional_data)
    print("\n=== After Merge ===")
    print(f"Revenue: {jp.get_value('revenue')}")
