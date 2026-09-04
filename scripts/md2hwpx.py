# -*- coding: utf-8 -*-
"""마크다운 -> HWPX 변환 (제목/표/목록/코드블록/인용/굵게)"""
import io, re, sys
from hwpx.document import HwpxDocument

KFONT, MONO = "맑은 고딕", "D2Coding"
INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`)')

def runs_for(p, text, size=10, base_bold=False, color=None):
    text = text.replace('<br>', ' / ')
    any_run = False
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            p.add_run(part[2:-2], bold=True, size=size, font=KFONT, color=color)
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            p.add_run(part[1:-1], size=size - 0.5, font=MONO, color="#B03060")
        else:
            p.add_run(part, bold=base_bold, size=size, font=KFONT, color=color)
        any_run = True
    if not any_run:
        p.add_run('', size=size, font=KFONT)

def convert(md_path, out_path):
    lines = io.open(md_path, encoding='utf-8').read().split('\n')
    doc = HwpxDocument.new()
    # 기본 문단 비우기
    for p in list(doc.paragraphs):
        try: p.remove()
        except Exception: pass

    def para(**kw):
        return doc.add_paragraph('', include_run=False, **kw)

    i = 0
    while i < len(lines):
        ln = lines[i]; s = ln.strip()

        # 코드블록
        if s.startswith('```'):
            i += 1; buf = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                buf.append(lines[i]); i += 1
            i += 1
            for b in buf:
                p = para()
                p.add_run(('    ' + b) if b else ' ', size=9, font=MONO, color="#222222")
                doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                         line_spacing_percent=110, spacing_after_pt=0)
            para().add_run(' ', size=6, font=KFONT)
            continue

        # 표
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                if not re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            ncol = max(len(r) for r in rows)
            t = doc.add_table(len(rows), ncol)
            for ri, row in enumerate(rows):
                for ci in range(ncol):
                    raw = row[ci] if ci < len(row) else ''
                    txt = raw.replace('<br>', ' / ')
                    txt = re.sub(r'\*\*(.+?)\*\*', r'\1', txt)
                    txt = re.sub(r'`([^`]+)`', r'\1', txt)
                    t.set_cell_text(ri, ci, txt)
                    if ri == 0:
                        try: t.set_cell_shading(ri, ci, "#DCE6F1")
                        except Exception: pass
            try: t.equalize_column_widths()
            except Exception: pass
            para().add_run(' ', size=6, font=KFONT)
            continue

        # 구분선
        if s == '---':
            para().add_run(' ', size=6, font=KFONT)
            try:
                doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                         bottom_border=True, border_color="#AAAAAA")
            except Exception: pass
            i += 1; continue

        # 제목
        m = re.match(r'^(#{1,4})\s+(.*)', s)
        if m:
            lvl = len(m.group(1))
            txt = re.sub(r'\*\*(.+?)\*\*', r'\1', m.group(2))
            size = {1: 16, 2: 13, 3: 11.5, 4: 10.5}[lvl]
            col = {1: "#1F3864", 2: "#1F3864", 3: "#2E4A7A", 4: "#333333"}[lvl]
            p = para()
            p.add_run(txt, bold=True, size=size, font=KFONT, color=col)
            doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                     alignment='center' if lvl == 1 else 'left',
                                     spacing_before_pt={1: 0, 2: 14, 3: 10, 4: 8}[lvl],
                                     spacing_after_pt=6, keep_with_next=True)
            i += 1; continue

        # 인용
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip()); i += 1
            for b in [x for x in buf if x]:
                p = para(); runs_for(p, b, size=9.5, color="#444444")
                doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                         indent_left_mm=6.0, spacing_after_pt=3)
            continue

        # 목록
        m = re.match(r'^(\s*)[-*]\s+(.*)', ln)
        if m:
            depth = len(m.group(1)) // 2
            p = para()
            p.add_run('• ' if depth == 0 else '- ', size=10, font=KFONT)
            runs_for(p, m.group(2))
            doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                     indent_left_mm=5.0 + 5.0 * depth, spacing_after_pt=2)
            i += 1; continue

        m = re.match(r'^(\s*)(\d+)\.\s+(.*)', ln)
        if m:
            p = para()
            p.add_run(m.group(2) + '. ', bold=True, size=10, font=KFONT)
            runs_for(p, m.group(3))
            doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1,
                                     indent_left_mm=5.0, spacing_after_pt=2)
            i += 1; continue

        if not s:
            i += 1; continue

        p = para(); runs_for(p, s)
        doc.styles.apply_paragraph_format(paragraph_index=len(doc.paragraphs) - 1, spacing_after_pt=4)
        i += 1

    doc.save_to_path(out_path)
    print("OK ->", out_path)

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
