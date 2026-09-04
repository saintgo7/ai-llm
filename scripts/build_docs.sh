#!/usr/bin/env bash
# docs/*.md -> docs/출력/*.docx, *.hwpx 재생성
#   의존성:  pip install python-docx python-hwpx
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p "docs/출력"

python3 -W ignore scripts/md2docx.py "docs/01_회신메일_본문.md"        "docs/출력/GPU활용현황_회신문.docx"
python3 -W ignore scripts/md2hwpx.py "docs/01_회신메일_본문.md"        "docs/출력/GPU활용현황_회신문.hwpx"
python3 -W ignore scripts/md2docx.py "docs/02_클러스터링_기술검토.md"  "docs/출력/첨부1_24GPU클러스터링_기술검토.docx"
python3 -W ignore scripts/md2hwpx.py "docs/02_클러스터링_기술검토.md"  "docs/출력/첨부1_24GPU클러스터링_기술검토.hwpx"

chmod 644 "docs/출력/"*
echo "완료: docs/출력/"
