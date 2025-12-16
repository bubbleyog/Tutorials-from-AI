"""
示例程序：嵌套布局与复杂界面
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示如何通过嵌套多种布局来创建复杂界面，包括：
    - 多层布局嵌套
    - 典型的主从界面结构
    - 数据采集系统界面示例

运行方式：
    python nested_layout.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QTextEdit, QListWidget, QProgressBar, QSlider,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QGroupBox, QFrame, QSplitter, QStatusBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import random


class NestedLayoutDemo(QWidget):
    """嵌套布局基础演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("嵌套布局演示")
        self.setMinimumSize(600, 450)
        
        # ===== 主布局（垂直）=====
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== 1. 顶部栏（水平布局）=====
        top_layout = QHBoxLayout()
        
        title = QLabel("嵌套布局示例")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        top_layout.addWidget(title)
        
        top_layout.addStretch()
        
        btn_settings = QPushButton("⚙ 设置")
        btn_help = QPushButton("❓ 帮助")
        top_layout.addWidget(btn_settings)
        top_layout.addWidget(btn_help)
        
        main_layout.addLayout(top_layout)
        
        # 分隔线
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: #bdc3c7;")
        main_layout.addWidget(line1)
        
        # ===== 2. 中间内容区（水平布局：左右分栏）=====
        content_layout = QHBoxLayout()
        
        # 左侧：参数面板（表单布局）
        left_group = QGroupBox("参数设置")
        left_form = QFormLayout()
        left_form.setSpacing(10)
        
        self.spin_freq = QDoubleSpinBox()
        self.spin_freq.setRange(0.1, 1000)
        self.spin_freq.setValue(100)
        self.spin_freq.setSuffix(" Hz")
        left_form.addRow("频率:", self.spin_freq)
        
        self.spin_amp = QDoubleSpinBox()
        self.spin_amp.setRange(0, 10)
        self.spin_amp.setValue(1.0)
        self.spin_amp.setSuffix(" V")
        left_form.addRow("幅度:", self.spin_amp)
        
        self.combo_wave = QComboBox()
        self.combo_wave.addItems(["正弦波", "方波", "三角波", "锯齿波"])
        left_form.addRow("波形:", self.combo_wave)
        
        self.check_output = QCheckBox("启用输出")
        left_form.addRow("", self.check_output)
        
        left_group.setLayout(left_form)
        left_group.setFixedWidth(200)
        content_layout.addWidget(left_group)
        
        # 右侧：显示区域（垂直布局）
        right_layout = QVBoxLayout()
        
        # 右侧上部：模拟图表区
        chart_label = QLabel("📊 波形显示区域")
        chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_label.setMinimumHeight(150)
        chart_label.setStyleSheet("""
            background-color: #1a1a2e;
            color: #00ff88;
            border: 2px solid #3498db;
            border-radius: 8px;
            font-size: 16px;
            font-family: monospace;
        """)
        right_layout.addWidget(chart_label, stretch=2)
        
        # 右侧下部：状态信息（网格布局）
        status_group = QGroupBox("状态信息")
        status_grid = QGridLayout()
        
        status_grid.addWidget(QLabel("采样率:"), 0, 0)
        status_grid.addWidget(QLabel("44100 Hz"), 0, 1)
        status_grid.addWidget(QLabel("位深度:"), 0, 2)
        status_grid.addWidget(QLabel("16 bit"), 0, 3)
        
        status_grid.addWidget(QLabel("缓冲区:"), 1, 0)
        self.progress_buffer = QProgressBar()
        self.progress_buffer.setValue(65)
        status_grid.addWidget(self.progress_buffer, 1, 1, 1, 3)
        
        status_group.setLayout(status_grid)
        right_layout.addWidget(status_group, stretch=1)
        
        content_layout.addLayout(right_layout)
        main_layout.addLayout(content_layout)
        
        # ===== 3. 底部按钮栏（水平布局）=====
        bottom_layout = QHBoxLayout()
        
        btn_start = QPushButton("▶ 开始")
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #219a52; }
        """)
        
        btn_stop = QPushButton("⏹ 停止")
        btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        
        bottom_layout.addWidget(btn_start)
        bottom_layout.addWidget(btn_stop)
        bottom_layout.addStretch()
        
        btn_export = QPushButton("📁 导出数据")
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        bottom_layout.addWidget(btn_export)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QWidget { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2c3e50;
            }
            QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)


class DataAcquisitionSystem(QMainWindow):
    """
    数据采集系统界面
    
    演示一个完整的数据采集软件界面布局
    使用多层嵌套布局实现复杂界面
    """
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.data_count = 0
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        self.setWindowTitle("多通道数据采集系统")
        self.setMinimumSize(900, 650)
        
        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        
        # ===== 主布局 =====
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # ===== 顶部工具栏 =====
        main_layout.addLayout(self.create_toolbar())
        
        # ===== 中间主内容区（使用Splitter可调整大小）=====
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧面板
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 中间显示区
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)
        
        # 右侧面板
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置初始大小比例
        splitter.setSizes([200, 450, 200])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(2, False)
        
        main_layout.addWidget(splitter)
        
        # ===== 底部状态栏 =====
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 状态栏添加永久控件
        self.label_status = QLabel("● 已停止")
        self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.statusBar.addPermanentWidget(self.label_status)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 1px solid #34495e;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel { color: #ecf0f1; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #5d6d7e;
                border-radius: 3px;
                background-color: #1a252f;
                color: #ecf0f1;
            }
            QCheckBox { color: #ecf0f1; }
            QListWidget {
                background-color: #1a252f;
                color: #ecf0f1;
                border: 1px solid #5d6d7e;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #0d1117;
                color: #00ff88;
                border: 1px solid #5d6d7e;
                border-radius: 3px;
                font-family: 'Consolas', monospace;
            }
            QProgressBar {
                border: 1px solid #5d6d7e;
                border-radius: 3px;
                background-color: #1a252f;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                color: white;
            }
            QSplitter::handle {
                background-color: #5d6d7e;
                width: 3px;
            }
        """)
    
    def create_toolbar(self) -> QHBoxLayout:
        """创建顶部工具栏"""
        layout = QHBoxLayout()
        
        # 标题
        title = QLabel("📡 数据采集系统")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 连接状态
        layout.addWidget(QLabel("设备:"))
        self.combo_device = QComboBox()
        self.combo_device.addItems(["COM3 - NI DAQ", "COM4 - Arduino", "TCP/IP"])
        self.combo_device.setMinimumWidth(150)
        layout.addWidget(self.combo_device)
        
        self.btn_connect = QPushButton("🔌 连接")
        self.btn_connect.setStyleSheet("background-color: #3498db;")
        layout.addWidget(self.btn_connect)
        
        return layout
    
    def create_left_panel(self) -> QWidget:
        """创建左侧参数面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 5, 0)
        
        # 通道设置
        ch_group = QGroupBox("通道设置")
        ch_layout = QVBoxLayout()
        
        self.channel_checks = []
        for i in range(4):
            check = QCheckBox(f"通道 {i+1}")
            check.setChecked(i < 2)  # 默认启用前两个
            self.channel_checks.append(check)
            ch_layout.addWidget(check)
        
        ch_group.setLayout(ch_layout)
        layout.addWidget(ch_group)
        
        # 采集参数
        param_group = QGroupBox("采集参数")
        param_form = QFormLayout()
        
        self.spin_rate = QSpinBox()
        self.spin_rate.setRange(1, 100000)
        self.spin_rate.setValue(1000)
        self.spin_rate.setSuffix(" Hz")
        param_form.addRow("采样率:", self.spin_rate)
        
        self.spin_samples = QSpinBox()
        self.spin_samples.setRange(100, 1000000)
        self.spin_samples.setValue(10000)
        param_form.addRow("采样点:", self.spin_samples)
        
        self.combo_trigger = QComboBox()
        self.combo_trigger.addItems(["立即", "边沿触发", "电平触发"])
        param_form.addRow("触发:", self.combo_trigger)
        
        param_group.setLayout(param_form)
        layout.addWidget(param_group)
        
        # 控制按钮
        ctrl_layout = QVBoxLayout()
        
        self.btn_start = QPushButton("▶ 开始采集")
        self.btn_start.setStyleSheet("background-color: #27ae60;")
        self.btn_start.clicked.connect(self.toggle_acquisition)
        ctrl_layout.addWidget(self.btn_start)
        
        self.btn_single = QPushButton("◉ 单次采集")
        self.btn_single.setStyleSheet("background-color: #f39c12;")
        ctrl_layout.addWidget(self.btn_single)
        
        layout.addLayout(ctrl_layout)
        layout.addStretch()
        
        return widget
    
    def create_center_panel(self) -> QWidget:
        """创建中间显示区"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 0, 5, 0)
        
        # 波形显示（模拟）
        wave_group = QGroupBox("实时波形")
        wave_layout = QVBoxLayout()
        
        self.wave_display = QLabel("等待数据...")
        self.wave_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wave_display.setMinimumHeight(200)
        self.wave_display.setStyleSheet("""
            background-color: #0d1117;
            color: #00ff88;
            border: 2px solid #27ae60;
            border-radius: 5px;
            font-family: monospace;
            font-size: 14px;
        """)
        wave_layout.addWidget(self.wave_display)
        
        # 通道选择按钮
        ch_btn_layout = QHBoxLayout()
        for i in range(4):
            btn = QPushButton(f"CH{i+1}")
            btn.setCheckable(True)
            btn.setChecked(i < 2)
            btn.setStyleSheet("""
                QPushButton { background-color: #5d6d7e; }
                QPushButton:checked { background-color: #27ae60; }
            """)
            ch_btn_layout.addWidget(btn)
        wave_layout.addLayout(ch_btn_layout)
        
        wave_group.setLayout(wave_layout)
        layout.addWidget(wave_group, stretch=2)
        
        # 数据统计
        stats_group = QGroupBox("数据统计")
        stats_grid = QGridLayout()
        
        stats = [
            ("CH1 平均:", "0.00 V"), ("CH1 最大:", "0.00 V"),
            ("CH2 平均:", "0.00 V"), ("CH2 最大:", "0.00 V"),
        ]
        
        self.stat_labels = []
        for i, (name, value) in enumerate(stats):
            row, col = divmod(i, 2)
            stats_grid.addWidget(QLabel(name), row, col*2)
            label = QLabel(value)
            label.setStyleSheet("color: #3498db; font-weight: bold;")
            self.stat_labels.append(label)
            stats_grid.addWidget(label, row, col*2 + 1)
        
        stats_group.setLayout(stats_grid)
        layout.addWidget(stats_group, stretch=1)
        
        return widget
    
    def create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 0, 0, 0)
        
        # 数据文件
        file_group = QGroupBox("数据文件")
        file_layout = QVBoxLayout()
        
        file_layout.addWidget(QLabel("保存路径:"))
        path_layout = QHBoxLayout()
        self.input_path = QLineEdit("./data/")
        path_layout.addWidget(self.input_path)
        btn_browse = QPushButton("...")
        btn_browse.setFixedWidth(30)
        btn_browse.setStyleSheet("background-color: #5d6d7e;")
        path_layout.addWidget(btn_browse)
        file_layout.addLayout(path_layout)
        
        file_layout.addWidget(QLabel("文件名:"))
        self.input_filename = QLineEdit("data_001.csv")
        file_layout.addWidget(self.input_filename)
        
        self.check_auto_save = QCheckBox("自动保存")
        file_layout.addWidget(self.check_auto_save)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # 日志
        log_group = QGroupBox("运行日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.append("[系统] 程序启动")
        self.log_text.append("[系统] 等待连接设备...")
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # 进度
        progress_group = QGroupBox("采集进度")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.label_progress = QLabel("0 / 10000 点")
        self.label_progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.label_progress)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        layout.addStretch()
        
        return widget
    
    def setup_timer(self):
        """设置定时器用于模拟数据更新"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
    
    def toggle_acquisition(self):
        """切换采集状态"""
        if self.is_running:
            self.stop_acquisition()
        else:
            self.start_acquisition()
    
    def start_acquisition(self):
        """开始采集"""
        self.is_running = True
        self.data_count = 0
        self.btn_start.setText("⏹ 停止采集")
        self.btn_start.setStyleSheet("background-color: #e74c3c;")
        self.label_status.setText("● 采集中")
        self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.log_text.append("[采集] 开始采集数据...")
        self.timer.start(50)  # 50ms更新一次
    
    def stop_acquisition(self):
        """停止采集"""
        self.is_running = False
        self.timer.stop()
        self.btn_start.setText("▶ 开始采集")
        self.btn_start.setStyleSheet("background-color: #27ae60;")
        self.label_status.setText("● 已停止")
        self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.log_text.append(f"[采集] 停止采集，共 {self.data_count} 点")
    
    def update_data(self):
        """更新模拟数据"""
        self.data_count += 100
        total = self.spin_samples.value()
        
        progress = min(100, int(self.data_count / total * 100))
        self.progress_bar.setValue(progress)
        self.label_progress.setText(f"{min(self.data_count, total)} / {total} 点")
        
        # 更新统计
        for label in self.stat_labels:
            value = random.uniform(-2, 2)
            label.setText(f"{value:.3f} V")
        
        # 更新波形显示
        wave_str = "".join(["▁▂▃▄▅▆▇█"[random.randint(0, 7)] for _ in range(40)])
        self.wave_display.setText(f"CH1: {wave_str}\nCH2: {wave_str[::-1]}")
        
        if self.data_count >= total:
            self.stop_acquisition()
            self.log_text.append("[采集] 采集完成")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 基础嵌套布局演示
    demo = NestedLayoutDemo()
    demo.show()
    
    # 完整的数据采集系统
    daq = DataAcquisitionSystem()
    daq.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

