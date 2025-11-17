"""
27. Markdown Converter - Markdown을 HTML로 변환
"""
import re

class MarkdownConverter:
    def __init__(self):
        self.converters = [
            (r'#{6}\s+(.*)', r'<h6>\1</h6>'),
            (r'#{5}\s+(.*)', r'<h5>\1</h5>'),
            (r'#{4}\s+(.*)', r'<h4>\1</h4>'),
            (r'#{3}\s+(.*)', r'<h3>\1</h3>'),
            (r'#{2}\s+(.*)', r'<h2>\1</h2>'),
            (r'#{1}\s+(.*)', r'<h1>\1</h1>'),
            (r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>'),
            (r'\*\*(.+?)\*\*', r'<strong>\1</strong>'),
            (r'\*(.+?)\*', r'<em>\1</em>'),
            (r'__(.+?)__', r'<strong>\1</strong>'),
            (r'_(.+?)_', r'<em>\1</em>'),
            (r'~~(.+?)~~', r'<del>\1</del>'),
            (r'`(.+?)`', r'<code>\1</code>'),
            (r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>'),
            (r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1">'),
        ]

    def convert(self, markdown_text):
        """Markdown을 HTML로 변환"""
        lines = markdown_text.split('\n')
        html_lines = []
        in_code_block = False
        in_list = False
        code_block_lines = []
        list_items = []

        for line in lines:
            # 코드 블록 처리
            if line.strip().startswith('```'):
                if in_code_block:
                    html_lines.append(f'<pre><code>{"".join(code_block_lines)}</code></pre>')
                    code_block_lines = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue

            if in_code_block:
                code_block_lines.append(line + '\n')
                continue

            # 리스트 처리
            if line.strip().startswith(('- ', '* ', '+ ')):
                if not in_list:
                    in_list = True
                    list_items = []
                list_items.append(f'<li>{self._apply_inline_styles(line.strip()[2:])}</li>')
                continue
            elif in_list:
                html_lines.append('<ul>')
                html_lines.extend(list_items)
                html_lines.append('</ul>')
                in_list = False
                list_items = []

            # 번호 리스트
            if re.match(r'^\d+\.\s+', line):
                content = re.sub(r'^\d+\.\s+', '', line)
                html_lines.append(f'<ol><li>{self._apply_inline_styles(content)}</li></ol>')
                continue

            # 인용구
            if line.strip().startswith('>'):
                content = line.strip()[1:].strip()
                html_lines.append(f'<blockquote>{self._apply_inline_styles(content)}</blockquote>')
                continue

            # 수평선
            if line.strip() in ('---', '***', '___'):
                html_lines.append('<hr>')
                continue

            # 빈 줄
            if not line.strip():
                html_lines.append('<br>')
                continue

            # 일반 텍스트 및 인라인 스타일
            html_line = self._apply_inline_styles(line)

            # 제목이 아닌 경우 단락으로 감싸기
            if not html_line.startswith('<h'):
                html_line = f'<p>{html_line}</p>'

            html_lines.append(html_line)

        # 미완성 리스트 처리
        if in_list:
            html_lines.append('<ul>')
            html_lines.extend(list_items)
            html_lines.append('</ul>')

        return '\n'.join(html_lines)

    def _apply_inline_styles(self, text):
        """인라인 스타일 적용"""
        for pattern, replacement in self.converters:
            text = re.sub(pattern, replacement, text)
        return text

    def convert_file(self, input_file, output_file=None):
        """파일 변환"""
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        html = self.convert(markdown_text)

        # HTML 템플릿
        full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 15px;
            color: #666;
        }}
    </style>
</head>
<body>
{html}
</body>
</html>'''

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            print(f"Converted {input_file} -> {output_file}")

        return full_html

if __name__ == '__main__':
    # 샘플 Markdown
    markdown_sample = '''# Hello World

This is a **bold** text and this is *italic*.

## Features

- Item 1
- Item 2
- Item 3

### Code Example

```python
def hello():
    print("Hello World!")
```

> This is a quote

[Link to Google](https://google.com)

---

End of document'''

    # 변환
    converter = MarkdownConverter()
    html = converter.convert(markdown_sample)
    print(html)

    # 파일로 저장
    with open('sample.md', 'w') as f:
        f.write(markdown_sample)

    converter.convert_file('sample.md', 'sample.html')
