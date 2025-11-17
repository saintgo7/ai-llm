"""
03. Data Visualization - matplotlib을 이용한 데이터 시각화
"""
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

class DataVisualizer:
    def __init__(self):
        self.fig = None
        self.ax = None

    def create_line_chart(self, x_data, y_data, title='Line Chart', xlabel='X', ylabel='Y'):
        """라인 차트 생성"""
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, marker='o', linestyle='-', linewidth=2, markersize=8)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt

    def create_bar_chart(self, categories, values, title='Bar Chart'):
        """막대 차트 생성"""
        plt.figure(figsize=(10, 6))
        colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
        plt.bar(categories, values, color=colors, alpha=0.8)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Categories', fontsize=12)
        plt.ylabel('Values', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return plt

    def create_pie_chart(self, labels, sizes, title='Pie Chart'):
        """파이 차트 생성"""
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 10})
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        return plt

    def create_scatter_plot(self, x_data, y_data, title='Scatter Plot'):
        """산점도 생성"""
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data, alpha=0.6, s=100, c=range(len(x_data)), cmap='viridis')
        plt.colorbar(label='Index')
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('X Values', fontsize=12)
        plt.ylabel('Y Values', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        return plt

    def create_histogram(self, data, bins=30, title='Histogram'):
        """히스토그램 생성"""
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=bins, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Value', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return plt

if __name__ == '__main__':
    visualizer = DataVisualizer()

    # 샘플 데이터 생성
    x = np.linspace(0, 10, 50)
    y = np.sin(x) * 10 + np.random.normal(0, 1, 50)

    # 라인 차트
    chart = visualizer.create_line_chart(x, y, 'Sample Line Chart', 'Time', 'Value')
    chart.savefig('line_chart.png', dpi=300, bbox_inches='tight')
    print("Line chart saved as 'line_chart.png'")

    # 막대 차트
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 56, 78, 32]
    chart = visualizer.create_bar_chart(categories, values, 'Sample Bar Chart')
    chart.savefig('bar_chart.png', dpi=300, bbox_inches='tight')
    print("Bar chart saved as 'bar_chart.png'")

    plt.close('all')
