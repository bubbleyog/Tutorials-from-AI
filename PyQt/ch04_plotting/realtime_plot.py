"""
示例程序：实时数据更新曲线
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示实时数据可视化技术：
    - QTimer驱动的定时更新
    - set_data()高效数据更新
    - 模拟传感器数据流

运行方式：
    python realtime_plot.py
"""

import sys
import time
import random
import numpy as np
from collections import deque
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QComboBox
)
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class RealtimePlotCanvas(FigureCanvas):
    """实时绑图画布"""
    
    def __init__(self, parent=None, width=10, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor('#1a1a2e')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#16213e')
        super().__init__(self.fig)


class RealtimePlotWindow(QMainWindow):
    """实时数据绑图窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 数据缓冲区
        self.max_points = 200
        self.time_data = deque(maxlen=self.max_points)
        self.value_data = deque(maxlen=self.max_points)
        
        # 时间计数
        self.start_time = time.time()
        self.data_count = 0
        
        # 信号参数
        self.frequency = 1.0
        self.amplitude = 1.0
        self.noise_level = 0.1
        
        self.init_ui()
        self.setup_plot()
        self.setup_timer()
    
    def init_ui(self):
        self.setWindowTitle("实时数据曲线 - 传感器模拟")
        self.setMinimumSize(1000, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧：图形区域
        plot_layout = QVBoxLayout()
        
        # 创建画布
        self.canvas = RealtimePlotCanvas(self, width=10, height=5, dpi=100)
        
        # 状态栏
        self.status_layout = QHBoxLayout()
        
        self.label_fps = QLabel("FPS: --")
        self.label_fps.setStyleSheet("color: #00ff88; font-family: monospace;")
        self.status_layout.addWidget(self.label_fps)
        
        self.label_points = QLabel("数据点: 0")
        self.label_points.setStyleSheet("color: #3498db; font-family: monospace;")
        self.status_layout.addWidget(self.label_points)
        
        self.label_value = QLabel("当前值: --")
        self.label_value.setStyleSheet("color: #f39c12; font-family: monospace;")
        self.status_layout.addWidget(self.label_value)
        
        self.status_layout.addStretch()
        
        plot_layout.addWidget(self.canvas)
        plot_layout.addLayout(self.status_layout)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #0d1117; }
            QLabel { color: #ecf0f1; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #1a1a2e;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #5d6d7e;
                border-radius: 4px;
                background-color: #16213e;
                color: #ecf0f1;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(250)
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("📊 实时数据监控")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        # 信号参数
        signal_group = QGroupBox("信号参数")
        form = QFormLayout()
        
        self.spin_freq = QDoubleSpinBox()
        self.spin_freq.setRange(0.1, 10)
        self.spin_freq.setValue(1.0)
        self.spin_freq.setSingleStep(0.1)
        self.spin_freq.setSuffix(" Hz")
        self.spin_freq.valueChanged.connect(lambda v: setattr(self, 'frequency', v))
        form.addRow("频率:", self.spin_freq)
        
        self.spin_amp = QDoubleSpinBox()
        self.spin_amp.setRange(0.1, 5)
        self.spin_amp.setValue(1.0)
        self.spin_amp.setSingleStep(0.1)
        self.spin_amp.valueChanged.connect(lambda v: setattr(self, 'amplitude', v))
        form.addRow("振幅:", self.spin_amp)
        
        self.spin_noise = QDoubleSpinBox()
        self.spin_noise.setRange(0, 1)
        self.spin_noise.setValue(0.1)
        self.spin_noise.setSingleStep(0.05)
        self.spin_noise.valueChanged.connect(lambda v: setattr(self, 'noise_level', v))
        form.addRow("噪声:", self.spin_noise)
        
        self.combo_signal = QComboBox()
        self.combo_signal.addItems(["正弦波", "方波", "三角波", "随机游走"])
        form.addRow("波形:", self.combo_signal)
        
        signal_group.setLayout(form)
        layout.addWidget(signal_group)
        
        # 显示设置
        display_group = QGroupBox("显示设置")
        display_form = QFormLayout()
        
        self.spin_points = QSpinBox()
        self.spin_points.setRange(50, 500)
        self.spin_points.setValue(200)
        self.spin_points.valueChanged.connect(self.on_max_points_changed)
        display_form.addRow("显示点数:", self.spin_points)
        
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(10, 500)
        self.spin_interval.setValue(50)
        self.spin_interval.setSuffix(" ms")
        self.spin_interval.valueChanged.connect(self.on_interval_changed)
        display_form.addRow("更新间隔:", self.spin_interval)
        
        display_group.setLayout(display_form)
        layout.addWidget(display_group)
        
        layout.addStretch()
        
        # 控制按钮
        self.btn_start = QPushButton("▶ 开始")
        self.btn_start.setStyleSheet("background-color: #27ae60;")
        self.btn_start.clicked.connect(self.toggle_acquisition)
        layout.addWidget(self.btn_start)
        
        btn_clear = QPushButton("🗑 清除数据")
        btn_clear.setStyleSheet("background-color: #e74c3c;")
        btn_clear.clicked.connect(self.clear_data)
        layout.addWidget(btn_clear)
        
        return panel
    
    def setup_plot(self):
        """初始化图形"""
        self.axes = self.canvas.axes
        
        # 创建空线条（使用set_data更新）
        self.line, = self.axes.plot([], [], 'c-', linewidth=1.5, label='传感器数据')
        
        # 设置样式
        self.axes.set_xlabel('时间 (s)', color='#ecf0f1', fontsize=11)
        self.axes.set_ylabel('数值', color='#ecf0f1', fontsize=11)
        self.axes.set_title('实时数据流', color='#ecf0f1', fontsize=14, fontweight='bold')
        self.axes.tick_params(colors='#ecf0f1')
        self.axes.grid(True, alpha=0.3, color='#5d6d7e')
        self.axes.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#5d6d7e',
                         labelcolor='#ecf0f1')
        
        # 设置初始范围
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(-2, 2)
        
        for spine in self.axes.spines.values():
            spine.set_color('#5d6d7e')
        
        self.canvas.fig.tight_layout()
    
    def setup_timer(self):
        """设置定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        
        # FPS计算
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)
        self.frame_count = 0
        
        self.is_running = False
    
    def toggle_acquisition(self):
        """切换采集状态"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.btn_start.setText("▶ 开始")
            self.btn_start.setStyleSheet("background-color: #27ae60;")
        else:
            self.timer.start(self.spin_interval.value())
            self.is_running = True
            self.btn_start.setText("⏸ 暂停")
            self.btn_start.setStyleSheet("background-color: #f39c12;")
    
    def update_data(self):
        """更新数据"""
        # 获取当前时间
        current_time = time.time() - self.start_time
        
        # 生成模拟数据
        signal_type = self.combo_signal.currentText()
        value = self.generate_signal(current_time, signal_type)
        
        # 添加到缓冲区
        self.time_data.append(current_time)
        self.value_data.append(value)
        self.data_count += 1
        
        # 更新图形
        self.update_plot()
        
        # 更新状态
        self.label_points.setText(f"数据点: {self.data_count}")
        self.label_value.setText(f"当前值: {value:.3f}")
        
        self.frame_count += 1
    
    def generate_signal(self, t: float, signal_type: str) -> float:
        """生成模拟信号"""
        noise = random.gauss(0, self.noise_level)
        
        if signal_type == "正弦波":
            return self.amplitude * np.sin(2 * np.pi * self.frequency * t) + noise
        elif signal_type == "方波":
            return self.amplitude * np.sign(np.sin(2 * np.pi * self.frequency * t)) + noise
        elif signal_type == "三角波":
            return self.amplitude * (2 * abs(2 * (self.frequency * t % 1) - 1) - 1) + noise
        elif signal_type == "随机游走":
            if len(self.value_data) > 0:
                return self.value_data[-1] + random.gauss(0, 0.1)
            return noise
        return noise
    
    def update_plot(self):
        """更新图形（高效方式）"""
        if len(self.time_data) < 2:
            return
        
        # 使用set_data而不是重新绑制
        self.line.set_data(list(self.time_data), list(self.value_data))
        
        # 自动调整x轴范围
        x_min = min(self.time_data)
        x_max = max(self.time_data)
        if x_max - x_min < 10:
            x_min = max(0, x_max - 10)
        self.axes.set_xlim(x_min, x_max + 0.5)
        
        # 自动调整y轴范围
        y_min = min(self.value_data)
        y_max = max(self.value_data)
        margin = (y_max - y_min) * 0.1 + 0.1
        self.axes.set_ylim(y_min - margin, y_max + margin)
        
        # 刷新画布
        self.canvas.draw()
    
    def update_fps(self):
        """更新FPS显示"""
        self.label_fps.setText(f"FPS: {self.frame_count}")
        self.frame_count = 0
    
    def clear_data(self):
        """清除数据"""
        self.time_data.clear()
        self.value_data.clear()
        self.data_count = 0
        self.start_time = time.time()
        
        self.line.set_data([], [])
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(-2, 2)
        self.canvas.draw()
        
        self.label_points.setText("数据点: 0")
        self.label_value.setText("当前值: --")
    
    def on_max_points_changed(self, value: int):
        """最大点数改变"""
        self.max_points = value
        self.time_data = deque(list(self.time_data)[-value:], maxlen=value)
        self.value_data = deque(list(self.value_data)[-value:], maxlen=value)
    
    def on_interval_changed(self, value: int):
        """更新间隔改变"""
        if self.is_running:
            self.timer.setInterval(value)


class MultiChannelRealtime(QMainWindow):
    """多通道实时数据"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多通道实时数据")
        self.setMinimumSize(800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # 创建画布（多子图）
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.fig.set_facecolor('#1a1a2e')
        self.canvas = FigureCanvas(self.fig)
        
        # 创建4个子图
        self.axes = []
        for i in range(4):
            ax = self.fig.add_subplot(2, 2, i + 1)
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='#ecf0f1')
            ax.set_title(f'通道 {i + 1}', color='#ecf0f1')
            for spine in ax.spines.values():
                spine.set_color('#5d6d7e')
            self.axes.append(ax)
        
        self.fig.tight_layout()
        layout.addWidget(self.canvas)
        
        # 数据
        self.max_points = 100
        self.data = [deque(maxlen=self.max_points) for _ in range(4)]
        self.lines = []
        
        for i, ax in enumerate(self.axes):
            line, = ax.plot([], [], ['c-', 'g-', 'r-', 'y-'][i], linewidth=1.5)
            ax.set_xlim(0, self.max_points)
            ax.set_ylim(-2, 2)
            ax.grid(True, alpha=0.3, color='#5d6d7e')
            self.lines.append(line)
        
        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)
        
        self.t = 0
        
        self.setStyleSheet("QMainWindow { background-color: #0d1117; }")
    
    def update_data(self):
        """更新多通道数据"""
        self.t += 1
        
        # 生成4通道数据
        signals = [
            np.sin(2 * np.pi * 0.5 * self.t / 20),
            np.cos(2 * np.pi * 0.3 * self.t / 20),
            np.sin(2 * np.pi * 0.7 * self.t / 20) * 0.5,
            random.gauss(0, 0.5),
        ]
        
        for i, (data, signal) in enumerate(zip(self.data, signals)):
            data.append(signal + random.gauss(0, 0.1))
            
            x = list(range(len(data)))
            self.lines[i].set_data(x, list(data))
            
            if len(data) > 10:
                y_data = list(data)
                y_min, y_max = min(y_data), max(y_data)
                margin = (y_max - y_min) * 0.1 + 0.2
                self.axes[i].set_ylim(y_min - margin, y_max + margin)
        
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    
    # 单通道实时图
    window = RealtimePlotWindow()
    window.show()
    
    # 多通道实时图
    multi = MultiChannelRealtime()
    multi.move(100, 100)
    multi.show()
    
    print("=" * 50)
    print("实时数据绑图演示")
    print("=" * 50)
    print("优化技术:")
    print("  1. 使用set_data()而不是clear()+plot()")
    print("  2. 使用deque限制数据点数")
    print("  3. 只更新必要的图形元素")
    print("  4. 合理设置更新间隔")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

