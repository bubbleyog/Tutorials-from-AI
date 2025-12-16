"""
示例程序：Matplotlib嵌入PyQt基础
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示将Matplotlib嵌入PyQt的基本方法：
    - FigureCanvas的创建和使用
    - 基本绑图操作
    - 图形更新方法

运行方式：
    python mpl_embed_basic.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox
)
from PyQt6.QtCore import Qt

# Matplotlib后端
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """
    Matplotlib画布类
    
    继承自FigureCanvasQTAgg，是将Matplotlib嵌入PyQt的核心组件
    """
    
    def __init__(self, parent=None, width: float = 8, height: float = 6, dpi: int = 100):
        """
        初始化画布
        
        Args:
            parent: 父控件
            width: 图形宽度（英寸）
            height: 图形高度（英寸）
            dpi: 分辨率
        """
        # 创建Figure对象
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        # 设置Figure的背景色
        self.fig.set_facecolor('#f8f9fa')
        
        # 添加子图（111表示1行1列的第1个）
        self.axes = self.fig.add_subplot(111)
        
        # 调用父类构造函数
        super().__init__(self.fig)
        
        # 设置尺寸策略，使画布可以随窗口调整大小
        self.setMinimumSize(400, 300)


class BasicPlotWindow(QMainWindow):
    """基本绑图窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.plot_sine()  # 初始绑图
    
    def init_ui(self):
        self.setWindowTitle("Matplotlib嵌入PyQt - 基础示例")
        self.setMinimumSize(700, 550)
        
        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        
        # 主布局
        layout = QVBoxLayout(central)
        
        # 标题
        title = QLabel("📊 Matplotlib + PyQt6 基础演示")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 创建Matplotlib画布
        self.canvas = MplCanvas(self, width=8, height=5, dpi=100)
        layout.addWidget(self.canvas)
        
        # 控制按钮
        btn_layout = QHBoxLayout()
        
        # 图形类型选择
        btn_layout.addWidget(QLabel("选择图形:"))
        self.combo_plot = QComboBox()
        self.combo_plot.addItems(["正弦波", "余弦波", "高斯分布", "阻尼振荡", "随机数据"])
        self.combo_plot.currentTextChanged.connect(self.on_plot_type_changed)
        btn_layout.addWidget(self.combo_plot)
        
        btn_layout.addStretch()
        
        # 刷新按钮
        btn_refresh = QPushButton("🔄 刷新数据")
        btn_refresh.clicked.connect(self.refresh_plot)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_layout.addWidget(btn_refresh)
        
        # 清除按钮
        btn_clear = QPushButton("🗑 清除")
        btn_clear.clicked.connect(self.clear_plot)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_layout.addWidget(btn_clear)
        
        layout.addLayout(btn_layout)
        
        # 状态标签
        self.label_status = QLabel("当前显示: 正弦波")
        self.label_status.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(self.label_status)
    
    def on_plot_type_changed(self, plot_type: str):
        """图形类型改变"""
        plot_functions = {
            "正弦波": self.plot_sine,
            "余弦波": self.plot_cosine,
            "高斯分布": self.plot_gaussian,
            "阻尼振荡": self.plot_damped,
            "随机数据": self.plot_random,
        }
        
        if plot_type in plot_functions:
            plot_functions[plot_type]()
            self.label_status.setText(f"当前显示: {plot_type}")
    
    def refresh_plot(self):
        """刷新当前图形"""
        self.on_plot_type_changed(self.combo_plot.currentText())
    
    def clear_plot(self):
        """清除图形"""
        self.canvas.axes.clear()
        self.canvas.axes.set_title("图形已清除")
        self.canvas.draw()
        self.label_status.setText("图形已清除")
    
    # ========== 绑图函数 ==========
    
    def plot_sine(self):
        """绑制正弦波"""
        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)
        
        # 清除之前的图形
        self.canvas.axes.clear()
        
        # 绑制新图形
        self.canvas.axes.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        self.canvas.axes.fill_between(x, y, alpha=0.3)
        
        # 设置标签和标题
        self.canvas.axes.set_xlabel('x (rad)', fontsize=12)
        self.canvas.axes.set_ylabel('y', fontsize=12)
        self.canvas.axes.set_title('正弦函数 y = sin(x)', fontsize=14)
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        
        # 刷新显示
        self.canvas.draw()
    
    def plot_cosine(self):
        """绑制余弦波"""
        x = np.linspace(0, 4 * np.pi, 500)
        y = np.cos(x)
        
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, y, 'r-', linewidth=2, label='cos(x)')
        self.canvas.axes.fill_between(x, y, alpha=0.3, color='red')
        self.canvas.axes.set_xlabel('x (rad)', fontsize=12)
        self.canvas.axes.set_ylabel('y', fontsize=12)
        self.canvas.axes.set_title('余弦函数 y = cos(x)', fontsize=14)
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_gaussian(self):
        """绑制高斯分布"""
        x = np.linspace(-5, 5, 500)
        
        # 多个高斯分布
        for sigma in [0.5, 1.0, 2.0]:
            y = np.exp(-x**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
            self.canvas.axes.plot(x, y, linewidth=2, label=f'σ = {sigma}')
        
        self.canvas.axes.clear()
        for sigma in [0.5, 1.0, 2.0]:
            y = np.exp(-x**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))
            self.canvas.axes.plot(x, y, linewidth=2, label=f'σ = {sigma}')
        
        self.canvas.axes.set_xlabel('x', fontsize=12)
        self.canvas.axes.set_ylabel('概率密度', fontsize=12)
        self.canvas.axes.set_title('高斯分布 (不同σ值)', fontsize=14)
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_damped(self):
        """绑制阻尼振荡"""
        t = np.linspace(0, 10, 500)
        gamma = 0.3  # 阻尼系数
        omega = 2 * np.pi  # 角频率
        
        y = np.exp(-gamma * t) * np.cos(omega * t)
        envelope = np.exp(-gamma * t)
        
        self.canvas.axes.clear()
        self.canvas.axes.plot(t, y, 'b-', linewidth=2, label='阻尼振荡')
        self.canvas.axes.plot(t, envelope, 'r--', linewidth=1, label='包络线')
        self.canvas.axes.plot(t, -envelope, 'r--', linewidth=1)
        self.canvas.axes.set_xlabel('时间 t (s)', fontsize=12)
        self.canvas.axes.set_ylabel('振幅', fontsize=12)
        self.canvas.axes.set_title(f'阻尼振荡 (γ = {gamma})', fontsize=14)
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.draw()
    
    def plot_random(self):
        """绑制随机数据"""
        x = np.arange(50)
        y = np.random.randn(50).cumsum()  # 随机游走
        
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, y, 'g-o', linewidth=1, markersize=4, label='随机游走')
        self.canvas.axes.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        self.canvas.axes.set_xlabel('步数', fontsize=12)
        self.canvas.axes.set_ylabel('位置', fontsize=12)
        self.canvas.axes.set_title('随机游走', fontsize=14)
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    
    window = BasicPlotWindow()
    window.show()
    
    print("=" * 50)
    print("Matplotlib嵌入PyQt基础示例")
    print("=" * 50)
    print("核心类:")
    print("  - Figure: Matplotlib图形对象")
    print("  - FigureCanvasQTAgg: Qt画布控件")
    print("关键方法:")
    print("  - axes.plot(): 绑制曲线")
    print("  - axes.clear(): 清除图形")
    print("  - canvas.draw(): 刷新显示")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

