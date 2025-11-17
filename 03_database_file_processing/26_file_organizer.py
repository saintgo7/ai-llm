"""
26. File Organizer - 파일 자동 정리 도구
"""
import os
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

class FileOrganizer:
    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.php', '.rb', '.go'],
            'Executables': ['.exe', '.msi', '.app', '.deb', '.rpm']
        }

    def organize_by_type(self, dry_run=False):
        """파일 유형별로 정리"""
        if not self.source_dir.exists():
            print(f"Directory not found: {self.source_dir}")
            return

        moved_files = 0

        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                category = self._get_category(file_ext)

                if category:
                    dest_dir = self.source_dir / category
                    if not dry_run:
                        dest_dir.mkdir(exist_ok=True)
                        shutil.move(str(file_path), str(dest_dir / file_path.name))
                    print(f"{'[DRY RUN] ' if dry_run else ''}Moved {file_path.name} -> {category}/")
                    moved_files += 1

        print(f"\nTotal files {'would be' if dry_run else ''} moved: {moved_files}")

    def _get_category(self, file_ext):
        """파일 확장자로 카테고리 찾기"""
        for category, extensions in self.file_types.items():
            if file_ext in extensions:
                return category
        return 'Others'

    def organize_by_date(self, dry_run=False):
        """날짜별로 정리"""
        for file_path in self.source_dir.iterdir():
            if file_path.is_file():
                # 수정 날짜 가져오기
                mtime = os.path.getmtime(file_path)
                date = datetime.fromtimestamp(mtime)
                date_folder = date.strftime('%Y-%m')

                dest_dir = self.source_dir / date_folder
                if not dry_run:
                    dest_dir.mkdir(exist_ok=True)
                    shutil.move(str(file_path), str(dest_dir / file_path.name))
                print(f"{'[DRY RUN] ' if dry_run else ''}Moved {file_path.name} -> {date_folder}/")

    def remove_duplicates(self, dry_run=False):
        """중복 파일 제거 (해시 기반)"""
        hashes = {}
        duplicates = []

        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                file_hash = self._calculate_hash(file_path)

                if file_hash in hashes:
                    duplicates.append(file_path)
                    if not dry_run:
                        file_path.unlink()
                    print(f"{'[DRY RUN] ' if dry_run else ''}Removed duplicate: {file_path.name}")
                else:
                    hashes[file_hash] = file_path

        print(f"\nTotal duplicates found: {len(duplicates)}")
        return duplicates

    def _calculate_hash(self, file_path):
        """파일 해시 계산"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def rename_files(self, pattern, dry_run=False):
        """파일 일괄 이름 변경"""
        count = 1
        for file_path in sorted(self.source_dir.iterdir()):
            if file_path.is_file():
                new_name = pattern.format(count=count, original=file_path.stem, ext=file_path.suffix)
                new_path = file_path.parent / new_name

                if not dry_run:
                    file_path.rename(new_path)
                print(f"{'[DRY RUN] ' if dry_run else ''}Renamed: {file_path.name} -> {new_name}")
                count += 1

    def get_statistics(self):
        """디렉토리 통계"""
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_type': {}
        }

        for item in self.source_dir.rglob('*'):
            if item.is_file():
                stats['total_files'] += 1
                stats['total_size'] += item.stat().st_size

                ext = item.suffix.lower()
                category = self._get_category(ext)
                stats['by_type'][category] = stats['by_type'].get(category, 0) + 1
            elif item.is_dir():
                stats['total_dirs'] += 1

        return stats

    def print_statistics(self):
        """통계 출력"""
        stats = self.get_statistics()

        print(f"\n=== Directory Statistics ===")
        print(f"Total Files: {stats['total_files']}")
        print(f"Total Directories: {stats['total_dirs']}")
        print(f"Total Size: {stats['total_size'] / (1024*1024):.2f} MB")

        print(f"\n--- Files by Type ---")
        for category, count in sorted(stats['by_type'].items()):
            print(f"{category}: {count}")

if __name__ == '__main__':
    # 테스트 디렉토리 생성
    test_dir = Path('test_organize')
    test_dir.mkdir(exist_ok=True)

    # 테스트 파일 생성
    test_files = [
        'document1.pdf', 'image1.jpg', 'video1.mp4',
        'script.py', 'data.csv', 'photo.png'
    ]

    for filename in test_files:
        (test_dir / filename).touch()

    # 파일 정리
    organizer = FileOrganizer(test_dir)

    print("=== Before Organization ===")
    organizer.print_statistics()

    print("\n=== Organizing files (dry run) ===")
    organizer.organize_by_type(dry_run=True)

    print("\n=== Organizing files ===")
    organizer.organize_by_type(dry_run=False)

    print("\n=== After Organization ===")
    organizer.print_statistics()
