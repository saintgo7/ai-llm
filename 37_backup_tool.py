"""
37. Backup Tool - 파일 백업 도구
"""
import os
import shutil
import zipfile
import tarfile
from datetime import datetime
from pathlib import Path
import hashlib
import json

class BackupTool:
    def __init__(self, source_dir, backup_dir='backups'):
        """
        백업 도구 초기화

        Args:
            source_dir: 백업할 디렉토리
            backup_dir: 백업 저장 디렉토리
        """
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_zip_backup(self, backup_name=None):
        """ZIP 백업 생성"""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.zip"

        backup_path = self.backup_dir / backup_name

        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.source_dir)
                    zipf.write(file_path, arcname)

        print(f"ZIP backup created: {backup_path}")
        return backup_path

    def create_tar_backup(self, backup_name=None, compression='gz'):
        """TAR 백업 생성 (gz, bz2, xz 압축 지원)"""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.tar.{compression}"

        backup_path = self.backup_dir / backup_name
        mode = f'w:{compression}'

        with tarfile.open(backup_path, mode) as tar:
            tar.add(self.source_dir, arcname=self.source_dir.name)

        print(f"TAR backup created: {backup_path}")
        return backup_path

    def create_incremental_backup(self, manifest_file='backup_manifest.json'):
        """증분 백업 생성"""
        manifest_path = self.backup_dir / manifest_file
        old_manifest = self._load_manifest(manifest_path)
        new_manifest = {}

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        incremental_dir = self.backup_dir / f"incremental_{timestamp}"
        incremental_dir.mkdir(exist_ok=True)

        files_backed_up = 0

        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                file_path = Path(root) / file
                rel_path = str(file_path.relative_to(self.source_dir))

                # 파일 해시 계산
                file_hash = self._calculate_hash(file_path)
                new_manifest[rel_path] = file_hash

                # 새 파일이거나 변경된 파일만 백업
                if rel_path not in old_manifest or old_manifest[rel_path] != file_hash:
                    dest_path = incremental_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    files_backed_up += 1

        # 매니페스트 저장
        self._save_manifest(manifest_path, new_manifest)

        print(f"Incremental backup created: {incremental_dir}")
        print(f"Files backed up: {files_backed_up}")

        return incremental_dir

    def restore_zip_backup(self, backup_file, restore_dir=None):
        """ZIP 백업 복원"""
        if restore_dir is None:
            restore_dir = self.source_dir.parent / f"restored_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        restore_dir = Path(restore_dir)
        restore_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(restore_dir)

        print(f"Backup restored to: {restore_dir}")
        return restore_dir

    def restore_tar_backup(self, backup_file, restore_dir=None):
        """TAR 백업 복원"""
        if restore_dir is None:
            restore_dir = self.source_dir.parent / f"restored_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        restore_dir = Path(restore_dir)
        restore_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(backup_file, 'r:*') as tar:
            tar.extractall(restore_dir)

        print(f"Backup restored to: {restore_dir}")
        return restore_dir

    def list_backups(self):
        """백업 목록 조회"""
        backups = []

        for file in self.backup_dir.iterdir():
            if file.is_file() and file.suffix in ['.zip', '.tar', '.gz', '.bz2', '.xz']:
                stat = file.stat()
                backups.append({
                    'name': file.name,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_mtime),
                    'path': str(file)
                })

        return sorted(backups, key=lambda x: x['created'], reverse=True)

    def delete_old_backups(self, keep_count=5):
        """오래된 백업 삭제"""
        backups = self.list_backups()

        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                Path(backup['path']).unlink()
                print(f"Deleted old backup: {backup['name']}")

    def _calculate_hash(self, file_path):
        """파일 해시 계산"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _load_manifest(self, manifest_path):
        """매니페스트 로드"""
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_manifest(self, manifest_path, manifest):
        """매니페스트 저장"""
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

# 사용 예제
if __name__ == '__main__':
    # 테스트 디렉토리 생성
    test_dir = Path('test_backup_source')
    test_dir.mkdir(exist_ok=True)

    # 테스트 파일 생성
    (test_dir / 'file1.txt').write_text('This is file 1')
    (test_dir / 'file2.txt').write_text('This is file 2')
    (test_dir / 'subdir').mkdir(exist_ok=True)
    (test_dir / 'subdir' / 'file3.txt').write_text('This is file 3')

    # 백업 도구 생성
    backup_tool = BackupTool(test_dir)

    print("=== Backup Tool Demo ===\n")

    # 1. ZIP 백업
    print("1. Creating ZIP backup...")
    zip_backup = backup_tool.create_zip_backup()

    # 2. TAR.GZ 백업
    print("\n2. Creating TAR.GZ backup...")
    tar_backup = backup_tool.create_tar_backup()

    # 3. 증분 백업
    print("\n3. Creating incremental backup...")
    incremental = backup_tool.create_incremental_backup()

    # 파일 수정
    (test_dir / 'file1.txt').write_text('This is modified file 1')

    # 다시 증분 백업
    print("\n4. Creating second incremental backup (after modification)...")
    incremental2 = backup_tool.create_incremental_backup()

    # 백업 목록
    print("\n5. Listing all backups:")
    backups = backup_tool.list_backups()
    for backup in backups:
        print(f"  {backup['name']}: {backup['size']:,} bytes, created {backup['created']}")

    # 복원
    print("\n6. Restoring ZIP backup...")
    restored = backup_tool.restore_zip_backup(zip_backup)

    # 오래된 백업 삭제
    print("\n7. Cleaning old backups (keep last 3)...")
    backup_tool.delete_old_backups(keep_count=3)

    print("\nDemo complete!")
