"""
示例程序：科研图表样式定制
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示科研论文级别的图表样式设置：
    - 论文发表标准样式
    - 字体和字号设置
    - 颜色方案
    - LaTeX公式支持
    - 多种预设风格

运行方式：
    python scientific_style.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QDoubleSpinBox, QCheckBox, QTabWidget
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from cycler import cycler


# ============================================================
# 预设样式
# ============================================================

STYLES = {
    "默认": {
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'figure.figsize': (8, 6),
        'lines.linewidth': 1.5,
        'axes.linewidth': 1.0,
    },
    "论文单栏": {
        'font.family': 'serif',
        'font.size': 9,
        'axes.labelsize': 10,
        'axes.titlesize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 8,
        'figure.figsize': (3.5, 2.8),
        'figure.dpi': 300,
        'lines.linewidth': 1.0,
        'lines.markersize': 4,
        'axes.linewidth': 0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
    },
    "论文双栏": {
        'font.family': 'serif',
        'font.size': 8,
        'axes.labelsize': 9,
        'axes.titlesize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 7,
        'figure.figsize': (7.0, 5.0),
        'figure.dpi': 300,
        'lines.linewidth': 1.0,
        'lines.markersize': 3,
        'axes.linewidth': 0.6,
    },
    "演示幻灯": {
        'font.size': 14,
        'axes.labelsize': 16,
        'axes.titlesize': 18,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'legend.fontsize': 12,
        'figure.figsize': (10, 7),
        'lines.linewidth': 2.5,
        'lines.markersize': 10,
        'axes.linewidth': 1.5,
    },
    "深色主题": {
        'figure.facecolor': '#1a1a2e',
        'axes.facecolor': '#16213e',
        'axes.edgecolor': '#5d6d7e',
        'axes.labelcolor': '#ecf0f1',
        'text.color': '#ecf0f1',
        'xtick.color': '#ecf0f1',
        'ytick.color': '#ecf0f1',
        'grid.color': '#5d6d7e',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'lines.linewidth': 2.0,
    },
}

# 颜色方案
COLOR_SCHEMES = {
    "经典": ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
    "色盲友好": ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#F0E442', '#56B4E9'],
    "自然": ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD'],
    "Pastel": ['#AEC7E8', '#FFBB78', '#98DF8A', '#FF9896', '#C5B0D5', '#C49C94'],
    "深色": ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c'],
}


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class ScientificStyleDemo(QMainWindow):
    """科研图表样式演示"""
    
    def __init__(self):
        super().__init__()
        self.current_style = "默认"
        self.current_colors = "经典"
        self.init_ui()
        self.update_plot()
    
    def init_ui(self):
        self.setWindowTitle("科研图表样式定制")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧图形
        plot_layout = QVBoxLayout()
        
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        # 样式代码预览
        self.label_code = QLabel("")
        self.label_code.setStyleSheet("""
            background-color: #2c3e50;
            color: #00ff88;
            font-family: Consolas, monospace;
            font-size: 10px;
            padding: 10px;
            border-radius: 5px;
        """)
        self.label_code.setWordWrap(True)
        self.label_code.setMaximumHeight(100)
        plot_layout.addWidget(self.label_code)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #27ae60;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #219a52; }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(280)
        layout = QVBoxLayout(panel)
        
        title = QLabel("🎨 样式设置")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 预设样式
        style_group = QGroupBox("预设样式")
        style_layout = QVBoxLayout()
        
        self.combo_style = QComboBox()
        self.combo_style.addItems(list(STYLES.keys()))
        self.combo_style.currentTextChanged.connect(self.on_style_changed)
        style_layout.addWidget(self.combo_style)
        
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        # 颜色方案
        color_group = QGroupBox("颜色方案")
        color_layout = QVBoxLayout()
        
        self.combo_colors = QComboBox()
        self.combo_colors.addItems(list(COLOR_SCHEMES.keys()))
        self.combo_colors.currentTextChanged.connect(self.on_colors_changed)
        color_layout.addWidget(self.combo_colors)
        
        # 颜色预览
        self.label_color_preview = QLabel()
        self.update_color_preview()
        color_layout.addWidget(self.label_color_preview)
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # 图形选项
        option_group = QGroupBox("图形选项")
        option_layout = QVBoxLayout()
        
        self.check_grid = QCheckBox("显示网格")
        self.check_grid.setChecked(True)
        self.check_grid.stateChanged.connect(self.update_plot)
        option_layout.addWidget(self.check_grid)
        
        self.check_legend = QCheckBox("显示图例")
        self.check_legend.setChecked(True)
        self.check_legend.stateChanged.connect(self.update_plot)
        option_layout.addWidget(self.check_legend)
        
        self.check_math = QCheckBox("使用数学公式")
        self.check_math.setChecked(True)
        self.check_math.stateChanged.connect(self.update_plot)
        option_layout.addWidget(self.check_math)
        
        option_group.setLayout(option_layout)
        layout.addWidget(option_group)
        
        # 数据类型
        data_group = QGroupBox("示例数据")
        data_layout = QVBoxLayout()
        
        self.combo_data = QComboBox()
        self.combo_data.addItems([
            "多曲线对比",
            "带误差棒",
            "散点拟合",
            "双Y轴",
        ])
        self.combo_data.currentIndexChanged.connect(self.update_plot)
        data_layout.addWidget(self.combo_data)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        layout.addStretch()
        
        # 导出提示
        export_info = QLabel(
            "提示: 使用工具栏💾按钮\n"
            "可保存为 PNG/PDF/SVG"
        )
        export_info.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(export_info)
        
        return panel
    
    def on_style_changed(self, style_name: str):
        """样式改变"""
        self.current_style = style_name
        self.update_plot()
    
    def on_colors_changed(self, color_name: str):
        """颜色方案改变"""
        self.current_colors = color_name
        self.update_color_preview()
        self.update_plot()
    
    def update_color_preview(self):
        """更新颜色预览"""
        colors = COLOR_SCHEMES.get(self.current_colors, COLOR_SCHEMES["经典"])
        html = " ".join([f'<span style="color:{c}; font-size:20px;">●</span>' for c in colors])
        self.label_color_preview.setText(html)
    
    def apply_style(self):
        """应用当前样式"""
        style = STYLES.get(self.current_style, STYLES["默认"])
        
        # 重置为默认值
        plt.rcdefaults()
        
        # 应用新样式
        for key, value in style.items():
            try:
                plt.rcParams[key] = value
            except:
                pass
        
        # 应用颜色
        colors = COLOR_SCHEMES.get(self.current_colors, COLOR_SCHEMES["经典"])
        plt.rcParams['axes.prop_cycle'] = cycler(color=colors)
    
    def update_plot(self):
        """更新图形"""
        # 应用样式
        self.apply_style()
        
        # 获取选项
        show_grid = self.check_grid.isChecked()
        show_legend = self.check_legend.isChecked()
        use_math = self.check_math.isChecked()
        data_type = self.combo_data.currentIndex()
        
        # 重新创建Figure以应用新样式
        style = STYLES.get(self.current_style, STYLES["默认"])
        figsize = style.get('figure.figsize', (8, 6))
        
        self.canvas.fig.clear()
        self.canvas.fig.set_size_inches(figsize)
        
        # 应用Figure背景色
        if 'figure.facecolor' in style:
            self.canvas.fig.set_facecolor(style['figure.facecolor'])
        else:
            self.canvas.fig.set_facecolor('white')
        
        ax = self.canvas.fig.add_subplot(111)
        
        # 应用axes背景色
        if 'axes.facecolor' in style:
            ax.set_facecolor(style['axes.facecolor'])
        
        colors = COLOR_SCHEMES.get(self.current_colors, COLOR_SCHEMES["经典"])
        
        # 根据数据类型绑图
        if data_type == 0:  # 多曲线对比
            self.plot_multiple_curves(ax, colors, use_math, show_legend)
        elif data_type == 1:  # 带误差棒
            self.plot_with_errorbars(ax, colors, use_math, show_legend)
        elif data_type == 2:  # 散点拟合
            self.plot_scatter_fit(ax, colors, use_math, show_legend)
        elif data_type == 3:  # 双Y轴
            self.plot_dual_axis(ax, colors, use_math, show_legend)
        
        if show_grid:
            ax.grid(True, alpha=0.3)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
        
        # 更新代码预览
        self.update_code_preview()
    
    def plot_multiple_curves(self, ax, colors, use_math, show_legend):
        """多曲线对比图"""
        x = np.linspace(0, 2 * np.pi, 100)
        
        for i, n in enumerate([1, 2, 3]):
            y = np.sin(n * x) / n
            if use_math:
                label = f'$\\sin({n}x)/{n}$'
            else:
                label = f'sin({n}x)/{n}'
            ax.plot(x, y, color=colors[i], linewidth=1.5, label=label)
        
        if use_math:
            ax.set_xlabel(r'$x$ (rad)')
            ax.set_ylabel(r'$f(x)$')
            ax.set_title(r'傅里叶级数分量: $f(x) = \sum \frac{\sin(nx)}{n}$')
        else:
            ax.set_xlabel('x (rad)')
            ax.set_ylabel('f(x)')
            ax.set_title('傅里叶级数分量')
        
        if show_legend:
            ax.legend(loc='upper right')
    
    def plot_with_errorbars(self, ax, colors, use_math, show_legend):
        """带误差棒的图"""
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y1 = np.array([2.3, 3.1, 4.2, 4.8, 5.5, 6.1, 6.8, 7.2])
        y2 = np.array([1.8, 2.5, 3.0, 3.8, 4.2, 4.9, 5.3, 5.8])
        yerr1 = np.random.uniform(0.2, 0.5, len(x))
        yerr2 = np.random.uniform(0.2, 0.4, len(x))
        
        ax.errorbar(x, y1, yerr=yerr1, fmt='o-', color=colors[0], 
                    capsize=4, capthick=1.5, label='样品 A')
        ax.errorbar(x, y2, yerr=yerr2, fmt='s--', color=colors[1], 
                    capsize=4, capthick=1.5, label='样品 B')
        
        if use_math:
            ax.set_xlabel(r'温度 $T$ (K)')
            ax.set_ylabel(r'电阻率 $\rho$ (m$\Omega\cdot$cm)')
        else:
            ax.set_xlabel('温度 T (K)')
            ax.set_ylabel('电阻率 (mΩ·cm)')
        ax.set_title('电阻率-温度依赖关系')
        
        if show_legend:
            ax.legend(loc='upper left')
    
    def plot_scatter_fit(self, ax, colors, use_math, show_legend):
        """散点拟合图"""
        np.random.seed(42)
        x = np.linspace(0, 10, 30)
        y_true = 2.5 * x + 1.0
        y = y_true + np.random.randn(len(x)) * 2
        
        # 线性拟合
        coeffs = np.polyfit(x, y, 1)
        y_fit = np.polyval(coeffs, x)
        
        ax.scatter(x, y, c=colors[0], s=50, alpha=0.7, label='实验数据')
        ax.plot(x, y_fit, color=colors[1], linewidth=2, 
                label=f'拟合: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
        
        # R²值
        ss_res = np.sum((y - y_fit) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot
        
        if use_math:
            ax.text(0.05, 0.95, f'$R^2 = {r2:.4f}$', transform=ax.transAxes,
                    fontsize=10, verticalalignment='top')
            ax.set_xlabel(r'自变量 $x$')
            ax.set_ylabel(r'因变量 $y$')
        else:
            ax.text(0.05, 0.95, f'R² = {r2:.4f}', transform=ax.transAxes,
                    fontsize=10, verticalalignment='top')
            ax.set_xlabel('自变量 x')
            ax.set_ylabel('因变量 y')
        ax.set_title('线性回归拟合')
        
        if show_legend:
            ax.legend(loc='lower right')
    
    def plot_dual_axis(self, ax, colors, use_math, show_legend):
        """双Y轴图"""
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x) * np.exp(-0.1 * x)
        y2 = 100 * np.exp(-0.3 * x)
        
        ax.plot(x, y1, color=colors[0], linewidth=2, label='振幅')
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel('振幅 (a.u.)', color=colors[0])
        ax.tick_params(axis='y', labelcolor=colors[0])
        
        ax2 = ax.twinx()
        ax2.plot(x, y2, color=colors[2], linewidth=2, linestyle='--', label='温度')
        ax2.set_ylabel('温度 (K)', color=colors[2])
        ax2.tick_params(axis='y', labelcolor=colors[2])
        
        ax.set_title('双Y轴: 振幅与温度随时间变化')
        
        if show_legend:
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    def update_code_preview(self):
        """更新代码预览"""
        style = STYLES.get(self.current_style, STYLES["默认"])
        code_lines = ["plt.rcParams.update({"]
        for key, value in list(style.items())[:5]:
            if isinstance(value, str):
                code_lines.append(f"    '{key}': '{value}',")
            else:
                code_lines.append(f"    '{key}': {value},")
        if len(style) > 5:
            code_lines.append("    # ... 更多参数 ...")
        code_lines.append("})")
        
        self.label_code.setText("\n".join(code_lines))


def main():
    app = QApplication(sys.argv)
    
    window = ScientificStyleDemo()
    window.show()
    
    print("=" * 50)
    print("科研图表样式定制")
    print("=" * 50)
    print("预设样式:")
    for name in STYLES.keys():
        print(f"  - {name}")
    print("\n颜色方案:")
    for name in COLOR_SCHEMES.keys():
        print(f"  - {name}")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

