"""
32. PDF Generator - PDF 문서 생성
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import datetime

class PDFGenerator:
    def __init__(self, filename='output.pdf', pagesize=letter):
        """PDF 생성기 초기화"""
        self.filename = filename
        self.pagesize = pagesize
        self.doc = SimpleDocTemplate(filename, pagesize=pagesize)
        self.story = []
        self.styles = getSampleStyleSheet()

    def add_title(self, text, style='Title'):
        """제목 추가"""
        para = Paragraph(text, self.styles[style])
        self.story.append(para)
        self.story.append(Spacer(1, 12))

    def add_heading(self, text, level=1):
        """헤딩 추가"""
        style_name = f'Heading{level}'
        para = Paragraph(text, self.styles[style_name])
        self.story.append(para)
        self.story.append(Spacer(1, 12))

    def add_paragraph(self, text, style='Normal'):
        """단락 추가"""
        para = Paragraph(text, self.styles[style])
        self.story.append(para)
        self.story.append(Spacer(1, 12))

    def add_table(self, data, col_widths=None, style=None):
        """테이블 추가"""
        table = Table(data, colWidths=col_widths)

        if style is None:
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

        table.setStyle(style)
        self.story.append(table)
        self.story.append(Spacer(1, 12))

    def add_image(self, image_path, width=None, height=None):
        """이미지 추가"""
        img = Image(image_path, width=width, height=height)
        self.story.append(img)
        self.story.append(Spacer(1, 12))

    def add_spacer(self, height=12):
        """공백 추가"""
        self.story.append(Spacer(1, height))

    def add_page_break(self):
        """페이지 나누기"""
        from reportlab.platypus import PageBreak
        self.story.append(PageBreak())

    def build(self):
        """PDF 생성"""
        self.doc.build(self.story)
        print(f"PDF generated: {self.filename}")

# 사용 예제
if __name__ == '__main__':
    # PDF 생성
    pdf = PDFGenerator('sample_report.pdf')

    # 제목
    pdf.add_title('Monthly Sales Report')

    # 날짜
    pdf.add_paragraph(f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')

    # 헤딩
    pdf.add_heading('Executive Summary', level=1)
    pdf.add_paragraph('This report provides an overview of sales performance for the month.')

    # 테이블
    pdf.add_heading('Sales Data', level=2)
    table_data = [
        ['Product', 'Units Sold', 'Revenue'],
        ['Product A', '150', '$15,000'],
        ['Product B', '200', '$20,000'],
        ['Product C', '100', '$10,000'],
        ['Total', '450', '$45,000']
    ]
    pdf.add_table(table_data)

    # 결론
    pdf.add_heading('Conclusion', level=2)
    pdf.add_paragraph('Sales performance exceeded expectations this month.')

    # PDF 생성
    pdf.build()

    print("\nNote: Install reportlab with: pip install reportlab")
