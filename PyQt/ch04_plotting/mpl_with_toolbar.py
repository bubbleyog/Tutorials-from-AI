"""
示例程序：带工具栏的绑图窗口
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示如何添加Matplotlib标准工具栏：
    - NavigationToolbar2QT的使用
    - 工具栏功能（缩放、平移、保存）
    - 自定义工具栏布局

运行方式：
    python mpl_with_toolbar.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDoubleSpinBox, QComboBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor('#ffffff')
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class PlotWithToolbar(QMainWindow):
    """带工具栏的绑图窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plot()
    
    def init_ui(self):
        self.setWindowTitle("Matplotlib工具栏演示 - 洛伦兹函数")
        self.setMinimumSize(900, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：参数面板
        main_layout.addWidget(self.create_params_panel(), stretch=0)
        
        # 右侧：图形区域
        plot_layout = QVBoxLayout()
        
        # 创建画布
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        
        # 创建工具栏（关键！）
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # 添加工具栏和画布
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        # 工具栏说明
        info = QLabel(
            "工具栏功能: 🏠复位 | ⬅➡历史 | ✥平移 | 🔍缩放 | ⚙调整 | 💾保存"
        )
        info.setStyleSheet("color: #7f8c8d; padding: 5px;")
        plot_layout.addWidget(info)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #8e44ad;
            }
            QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8e44ad; }
        """)
    
    def create_params_panel(self) -> QWidget:
        """创建参数面板"""
        panel = QWidget()
        panel.setFixedWidth(250)
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("参数设置")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 洛伦兹函数参数
        lorentz_group = QGroupBox("洛伦兹函数")
        form = QFormLayout()
        
        # 中心位置 x0
        self.spin_x0 = QDoubleSpinBox()
        self.spin_x0.setRange(-10, 10)
        self.spin_x0.setValue(0)
        self.spin_x0.setSingleStep(0.5)
        self.spin_x0.valueChanged.connect(self.update_plot)
        form.addRow("中心 x₀:", self.spin_x0)
        
        # 半高宽 Γ
        self.spin_gamma = QDoubleSpinBox()
        self.spin_gamma.setRange(0.1, 10)
        self.spin_gamma.setValue(1)
        self.spin_gamma.setSingleStep(0.1)
        self.spin_gamma.valueChanged.connect(self.update_plot)
        form.addRow("半高宽 Γ:", self.spin_gamma)
        
        # 幅度 A
        self.spin_amp = QDoubleSpinBox()
        self.spin_amp.setRange(0.1, 10)
        self.spin_amp.setValue(1)
        self.spin_amp.setSingleStep(0.1)
        self.spin_amp.valueChanged.connect(self.update_plot)
        form.addRow("幅度 A:", self.spin_amp)
        
        lorentz_group.setLayout(form)
        layout.addWidget(lorentz_group)
        
        # 显示选项
        display_group = QGroupBox("显示选项")
        display_form = QFormLayout()
        
        # 颜色选择
        self.combo_color = QComboBox()
        self.combo_color.addItems(["蓝色", "红色", "绿色", "紫色", "橙色"])
        self.combo_color.currentIndexChanged.connect(self.update_plot)
        display_form.addRow("线条颜色:", self.combo_color)
        
        # 线型选择
        self.combo_style = QComboBox()
        self.combo_style.addItems(["实线", "虚线", "点线", "点划线"])
        self.combo_style.currentIndexChanged.connect(self.update_plot)
        display_form.addRow("线型:", self.combo_style)
        
        display_group.setLayout(display_form)
        layout.addWidget(display_group)
        
        # 公式显示
        formula_group = QGroupBox("洛伦兹函数公式")
        formula_layout = QVBoxLayout()
        
        formula = QLabel(
            "L(x) = A · (Γ/2)² / [(x-x₀)² + (Γ/2)²]\n\n"
            "物理应用:\n"
            "• 共振曲线\n"
            "• 光谱线型\n"
            "• 布里渊散射"
        )
        formula.setStyleSheet("font-size: 11px; color: #2c3e50;")
        formula_layout.addWidget(formula)
        
        formula_group.setLayout(formula_layout)
        layout.addWidget(formula_group)
        
        layout.addStretch()
        
        # 更新按钮
        btn_update = QPushButton("🔄 更新图形")
        btn_update.clicked.connect(self.update_plot)
        layout.addWidget(btn_update)
        
        return panel
    
    def update_plot(self):
        """更新图形"""
        # 获取参数
        x0 = self.spin_x0.value()
        gamma = self.spin_gamma.value()
        amp = self.spin_amp.value()
        
        # 颜色映射
        colors = {'蓝色': 'b', '红色': 'r', '绿色': 'g', '紫色': 'purple', '橙色': 'orange'}
        color = colors.get(self.combo_color.currentText(), 'b')
        
        # 线型映射
        styles = {'实线': '-', '虚线': '--', '点线': ':', '点划线': '-.'}
        style = styles.get(self.combo_style.currentText(), '-')
        
        # 生成数据
        x = np.linspace(-10, 10, 1000)
        half_gamma = gamma / 2
        y = amp * (half_gamma ** 2) / ((x - x0) ** 2 + half_gamma ** 2)
        
        # 绑图
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, y, color + style, linewidth=2, label=f'L(x), x₀={x0}, Γ={gamma}')
        
        # 标注半高宽
        y_max = amp
        y_half = y_max / 2
        self.canvas.axes.axhline(y=y_half, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
        self.canvas.axes.annotate(f'FWHM = {gamma}', xy=(x0 + gamma/2, y_half),
                                   xytext=(x0 + 2, y_half + 0.1),
                                   fontsize=10, color='gray',
                                   arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7))
        
        # 标注峰值
        self.canvas.axes.plot(x0, y_max, 'ro', markersize=8)
        self.canvas.axes.annotate(f'峰值 ({x0}, {y_max:.2f})', xy=(x0, y_max),
                                   xytext=(x0 + 1.5, y_max + 0.1),
                                   fontsize=10)
        
        # 设置样式
        self.canvas.axes.set_xlabel('x', fontsize=12)
        self.canvas.axes.set_ylabel('L(x)', fontsize=12)
        self.canvas.axes.set_title('洛伦兹函数 (Lorentzian)', fontsize=14, fontweight='bold')
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.axes.set_xlim(-10, 10)
        self.canvas.axes.set_ylim(0, amp * 1.2)
        
        # 调整布局并刷新
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class MultiCurveToolbar(QMainWindow):
    """多曲线带工具栏示例"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.plot_multiple_curves()
    
    def init_ui(self):
        self.setWindowTitle("多曲线绑图 - 工具栏缩放演示")
        self.setMinimumSize(800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        
        # 说明
        info = QLabel("使用工具栏的缩放功能查看曲线细节，拖动平移浏览不同区域")
        info.setStyleSheet("color: #2c3e50; font-size: 13px; padding: 10px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        # 画布和工具栏
        self.canvas = MplCanvas(self, width=10, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
    
    def plot_multiple_curves(self):
        """绑制多条曲线"""
        x = np.linspace(0, 10, 1000)
        
        # 多个频率的正弦波叠加
        y1 = np.sin(2 * np.pi * 1 * x)
        y2 = 0.5 * np.sin(2 * np.pi * 3 * x)
        y3 = 0.25 * np.sin(2 * np.pi * 7 * x)
        y_sum = y1 + y2 + y3
        
        self.canvas.axes.plot(x, y1, 'b-', linewidth=1, alpha=0.7, label='f=1 Hz')
        self.canvas.axes.plot(x, y2, 'g-', linewidth=1, alpha=0.7, label='f=3 Hz')
        self.canvas.axes.plot(x, y3, 'r-', linewidth=1, alpha=0.7, label='f=7 Hz')
        self.canvas.axes.plot(x, y_sum, 'k-', linewidth=2, label='叠加')
        
        self.canvas.axes.set_xlabel('时间 (s)', fontsize=12)
        self.canvas.axes.set_ylabel('振幅', fontsize=12)
        self.canvas.axes.set_title('多频率正弦波叠加', fontsize=14)
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    
    # 洛伦兹函数示例
    window1 = PlotWithToolbar()
    window1.show()
    
    # 多曲线示例
    window2 = MultiCurveToolbar()
    window2.move(100, 100)
    window2.show()
    
    print("=" * 50)
    print("Matplotlib工具栏演示")
    print("=" * 50)
    print("工具栏功能:")
    print("  🏠 Home - 恢复原始视图")
    print("  ⬅️ Back - 返回上一视图")
    print("  ➡️ Forward - 前进到下一视图")
    print("  ✥ Pan - 拖动平移模式")
    print("  🔍 Zoom - 矩形缩放模式")
    print("  ⚙️ Subplots - 调整子图边距")
    print("  💾 Save - 保存图片")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

