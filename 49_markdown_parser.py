"""
49. Markdown Parser - Markdown 파서 및 AST 생성기
"""
import re
from typing import List, Dict, Any

class MarkdownNode:
    """Markdown AST 노드"""

    def __init__(self, node_type, value=None, children=None, meta=None):
        self.type = node_type
        self.value = value
        self.children = children or []
        self.meta = meta or {}

    def __repr__(self):
        return f"Node({self.type}, {self.value}, {len(self.children)} children)"

class MarkdownParser:
    """Markdown 파서"""

    def __init__(self):
        self.patterns = {
            'heading': r'^(#{1,6})\s+(.+)$',
            'bold': r'\*\*(.+?)\*\*',
            'italic': r'\*(.+?)\*',
            'code_inline': r'`(.+?)`',
            'link': r'\[(.+?)\]\((.+?)\)',
            'image': r'!\[(.+?)\]\((.+?)\)',
            'list_item': r'^[\*\-\+]\s+(.+)$',
            'ordered_list': r'^(\d+)\.\s+(.+)$',
            'blockquote': r'^>\s+(.+)$',
            'code_block': r'^```(\w+)?\n(.*?)\n```$',
            'hr': r'^(---|___|\*\*\*)$',
        }

    def parse(self, markdown_text):
        """Markdown 텍스트를 AST로 파싱"""
        lines = markdown_text.split('\n')
        root = MarkdownNode('document')
        i = 0

        while i < len(lines):
            line = lines[i]

            # 코드 블록
            if line.strip().startswith('```'):
                node, consumed = self._parse_code_block(lines[i:])
                root.children.append(node)
                i += consumed
                continue

            # 헤딩
            heading_match = re.match(self.patterns['heading'], line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2)
                node = MarkdownNode('heading', text, meta={'level': level})
                root.children.append(node)
                i += 1
                continue

            # 수평선
            if re.match(self.patterns['hr'], line.strip()):
                root.children.append(MarkdownNode('hr'))
                i += 1
                continue

            # 인용
            blockquote_match = re.match(self.patterns['blockquote'], line)
            if blockquote_match:
                text = blockquote_match.group(1)
                node = MarkdownNode('blockquote', text)
                root.children.append(node)
                i += 1
                continue

            # 순서 없는 리스트
            list_match = re.match(self.patterns['list_item'], line)
            if list_match:
                node, consumed = self._parse_list(lines[i:], ordered=False)
                root.children.append(node)
                i += consumed
                continue

            # 순서 있는 리스트
            ordered_match = re.match(self.patterns['ordered_list'], line)
            if ordered_match:
                node, consumed = self._parse_list(lines[i:], ordered=True)
                root.children.append(node)
                i += consumed
                continue

            # 빈 줄
            if not line.strip():
                i += 1
                continue

            # 일반 단락
            node, consumed = self._parse_paragraph(lines[i:])
            root.children.append(node)
            i += consumed

        return root

    def _parse_code_block(self, lines):
        """코드 블록 파싱"""
        lang_match = re.match(r'^```(\w+)?', lines[0])
        lang = lang_match.group(1) if lang_match else ''

        code_lines = []
        i = 1

        while i < len(lines) and not lines[i].strip().startswith('```'):
            code_lines.append(lines[i])
            i += 1

        code = '\n'.join(code_lines)
        node = MarkdownNode('code_block', code, meta={'language': lang})

        return node, i + 1

    def _parse_list(self, lines, ordered=False):
        """리스트 파싱"""
        list_node = MarkdownNode('ordered_list' if ordered else 'unordered_list')
        pattern = self.patterns['ordered_list'] if ordered else self.patterns['list_item']
        i = 0

        while i < len(lines):
            match = re.match(pattern, lines[i])
            if not match:
                break

            text = match.group(2) if ordered else match.group(1)
            item_node = MarkdownNode('list_item', text)
            list_node.children.append(item_node)
            i += 1

        return list_node, i

    def _parse_paragraph(self, lines):
        """단락 파싱"""
        para_lines = []
        i = 0

        while i < len(lines) and lines[i].strip():
            para_lines.append(lines[i])
            i += 1

        text = ' '.join(para_lines)

        # 인라인 요소 파싱
        node = MarkdownNode('paragraph')
        node.children = self._parse_inline(text)

        return node, i

    def _parse_inline(self, text):
        """인라인 요소 파싱"""
        nodes = []
        remaining = text

        while remaining:
            # 이미지
            img_match = re.search(self.patterns['image'], remaining)
            if img_match and img_match.start() == 0:
                node = MarkdownNode('image', meta={
                    'alt': img_match.group(1),
                    'url': img_match.group(2)
                })
                nodes.append(node)
                remaining = remaining[img_match.end():]
                continue

            # 링크
            link_match = re.search(self.patterns['link'], remaining)
            if link_match and link_match.start() == 0:
                node = MarkdownNode('link', img_match.group(1), meta={
                    'url': link_match.group(2)
                })
                nodes.append(node)
                remaining = remaining[link_match.end():]
                continue

            # Bold
            bold_match = re.search(self.patterns['bold'], remaining)
            if bold_match and bold_match.start() == 0:
                node = MarkdownNode('bold', bold_match.group(1))
                nodes.append(node)
                remaining = remaining[bold_match.end():]
                continue

            # Italic
            italic_match = re.search(self.patterns['italic'], remaining)
            if italic_match and italic_match.start() == 0:
                node = MarkdownNode('italic', italic_match.group(1))
                nodes.append(node)
                remaining = remaining[italic_match.end():]
                continue

            # Code
            code_match = re.search(self.patterns['code_inline'], remaining)
            if code_match and code_match.start() == 0:
                node = MarkdownNode('code_inline', code_match.group(1))
                nodes.append(node)
                remaining = remaining[code_match.end():]
                continue

            # 일반 텍스트
            nodes.append(MarkdownNode('text', remaining[0]))
            remaining = remaining[1:]

        return nodes

    def ast_to_dict(self, node):
        """AST를 딕셔너리로 변환"""
        result = {
            'type': node.type,
            'value': node.value,
            'meta': node.meta
        }

        if node.children:
            result['children'] = [self.ast_to_dict(child) for child in node.children]

        return result

    def print_ast(self, node, indent=0):
        """AST를 보기 좋게 출력"""
        prefix = "  " * indent

        if node.value:
            print(f"{prefix}{node.type}: {node.value[:50]}..." if len(str(node.value)) > 50 else f"{prefix}{node.type}: {node.value}")
        else:
            print(f"{prefix}{node.type}")

        if node.meta:
            print(f"{prefix}  meta: {node.meta}")

        for child in node.children:
            self.print_ast(child, indent + 1)

if __name__ == '__main__':
    # 테스트 Markdown
    markdown_sample = """# Hello World

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

End of document"""

    print("=== Markdown Parser ===\n")
    print("Input Markdown:")
    print("-" * 50)
    print(markdown_sample)
    print("-" * 50)

    # 파싱
    parser = MarkdownParser()
    ast = parser.parse(markdown_sample)

    print("\n=== AST (Abstract Syntax Tree) ===\n")
    parser.print_ast(ast)

    print("\n=== AST as Dictionary ===\n")
    import json
    ast_dict = parser.ast_to_dict(ast)
    print(json.dumps(ast_dict, indent=2))
