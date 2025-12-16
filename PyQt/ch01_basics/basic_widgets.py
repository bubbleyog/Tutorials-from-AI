"""
示例程序：常用控件详解
所属章节：第一章 - PyQt基础入门

功能说明：
    演示PyQt中最常用的控件，包括：
    - QLabel: 标签
    - QPushButton: 按钮
    - QLineEdit: 单行输入框
    - QSpinBox / QDoubleSpinBox: 数值输入框
    - QComboBox: 下拉选择框
    - QCheckBox: 复选框
    - QSlider: 滑动条
    - QProgressBar: 进度条

运行方式：
    python basic_widgets.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, QSlider,
    QProgressBar, QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import Qt


class WidgetShowcase(QWidget):
    """
    控件展示窗口
    
    展示PyQt中常用的控件及其基本用法
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("PyQt常用控件展示")
        self.setMinimumSize(500, 600)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 添加各组控件
        main_layout.addWidget(self.create_label_group())
        main_layout.addWidget(self.create_input_group())
        main_layout.addWidget(self.create_number_group())
        main_layout.addWidget(self.create_selection_group())
        main_layout.addWidget(self.create_slider_group())
        main_layout.addWidget(self.create_button_group())
        
        self.setLayout(main_layout)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def create_label_group(self) -> QGroupBox:
        """创建标签控件组"""
        group = QGroupBox("QLabel - 标签")
        layout = QVBoxLayout()
        
        # 普通标签
        label1 = QLabel("普通文本标签")
        
        # 带样式的标签
        label2 = QLabel("带样式的标签（粗体、蓝色）")
        label2.setStyleSheet("font-weight: bold; color: #3498db;")
        
        # 可选择文本的标签
        label3 = QLabel("可选择复制的标签（尝试用鼠标选择）")
        label3.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        
        # 富文本标签
        label4 = QLabel()
        label4.setText(
            '<span style="color: #e74c3c;">红色</span> + '
            '<span style="color: #27ae60;">绿色</span> = '
            '<b>富文本</b>'
        )
        
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        group.setLayout(layout)
        return group
    
    def create_input_group(self) -> QGroupBox:
        """创建文本输入控件组"""
        group = QGroupBox("QLineEdit - 文本输入")
        layout = QGridLayout()
        
        # 普通输入框
        layout.addWidget(QLabel("普通输入:"), 0, 0)
        self.input_normal = QLineEdit()
        self.input_normal.setPlaceholderText("请输入文本...")
        layout.addWidget(self.input_normal, 0, 1)
        
        # 密码输入框
        layout.addWidget(QLabel("密码输入:"), 1, 0)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("输入密码")
        layout.addWidget(self.input_password, 1, 1)
        
        # 只读输入框
        layout.addWidget(QLabel("只读输入:"), 2, 0)
        self.input_readonly = QLineEdit("这是只读文本")
        self.input_readonly.setReadOnly(True)
        layout.addWidget(self.input_readonly, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_number_group(self) -> QGroupBox:
        """创建数值输入控件组"""
        group = QGroupBox("QSpinBox / QDoubleSpinBox - 数值输入")
        layout = QGridLayout()
        
        # 整数输入 (QSpinBox)
        layout.addWidget(QLabel("采样点数:"), 0, 0)
        self.spin_int = QSpinBox()
        self.spin_int.setRange(1, 10000)
        self.spin_int.setValue(1000)
        self.spin_int.setSuffix(" 点")
        self.spin_int.setSingleStep(100)
        layout.addWidget(self.spin_int, 0, 1)
        
        # 浮点数输入 (QDoubleSpinBox) - 频率
        layout.addWidget(QLabel("采样频率:"), 1, 0)
        self.spin_freq = QDoubleSpinBox()
        self.spin_freq.setRange(0.01, 10000.0)
        self.spin_freq.setValue(100.0)
        self.spin_freq.setSuffix(" Hz")
        self.spin_freq.setDecimals(2)
        self.spin_freq.setSingleStep(10.0)
        layout.addWidget(self.spin_freq, 1, 1)
        
        # 浮点数输入 - 温度
        layout.addWidget(QLabel("目标温度:"), 2, 0)
        self.spin_temp = QDoubleSpinBox()
        self.spin_temp.setRange(4.0, 400.0)
        self.spin_temp.setValue(300.0)
        self.spin_temp.setSuffix(" K")
        self.spin_temp.setDecimals(1)
        self.spin_temp.setSingleStep(1.0)
        layout.addWidget(self.spin_temp, 2, 1)
        
        # 浮点数输入 - 带前缀
        layout.addWidget(QLabel("电压设置:"), 3, 0)
        self.spin_voltage = QDoubleSpinBox()
        self.spin_voltage.setRange(-10.0, 10.0)
        self.spin_voltage.setValue(0.0)
        self.spin_voltage.setPrefix("V = ")
        self.spin_voltage.setSuffix(" V")
        self.spin_voltage.setDecimals(3)
        self.spin_voltage.setSingleStep(0.1)
        layout.addWidget(self.spin_voltage, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def create_selection_group(self) -> QGroupBox:
        """创建选择控件组"""
        group = QGroupBox("QComboBox / QCheckBox - 选择控件")
        layout = QGridLayout()
        
        # 下拉选择框 (QComboBox)
        layout.addWidget(QLabel("量程选择:"), 0, 0)
        self.combo_range = QComboBox()
        self.combo_range.addItems(["1 mV", "10 mV", "100 mV", "1 V", "10 V"])
        self.combo_range.setCurrentIndex(2)  # 默认选择 "100 mV"
        layout.addWidget(self.combo_range, 0, 1)
        
        # 另一个下拉框 - 通道选择
        layout.addWidget(QLabel("测量通道:"), 1, 0)
        self.combo_channel = QComboBox()
        for i in range(1, 5):
            self.combo_channel.addItem(f"通道 {i}")
        layout.addWidget(self.combo_channel, 1, 1)
        
        # 复选框 (QCheckBox)
        layout.addWidget(QLabel("选项:"), 2, 0)
        
        checkbox_layout = QHBoxLayout()
        self.check_auto = QCheckBox("自动量程")
        self.check_auto.setChecked(True)
        self.check_avg = QCheckBox("启用平均")
        self.check_log = QCheckBox("记录日志")
        checkbox_layout.addWidget(self.check_auto)
        checkbox_layout.addWidget(self.check_avg)
        checkbox_layout.addWidget(self.check_log)
        checkbox_layout.addStretch()
        
        layout.addLayout(checkbox_layout, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_slider_group(self) -> QGroupBox:
        """创建滑动条控件组"""
        group = QGroupBox("QSlider / QProgressBar - 滑动与进度")
        layout = QGridLayout()
        
        # 水平滑动条
        layout.addWidget(QLabel("增益调节:"), 0, 0)
        
        slider_layout = QHBoxLayout()
        self.slider_gain = QSlider(Qt.Orientation.Horizontal)
        self.slider_gain.setRange(0, 100)
        self.slider_gain.setValue(50)
        self.slider_gain.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_gain.setTickInterval(10)
        
        self.label_gain = QLabel("50")
        self.label_gain.setMinimumWidth(30)
        self.slider_gain.valueChanged.connect(
            lambda v: self.label_gain.setText(str(v))
        )
        
        slider_layout.addWidget(self.slider_gain)
        slider_layout.addWidget(self.label_gain)
        layout.addLayout(slider_layout, 0, 1)
        
        # 进度条
        layout.addWidget(QLabel("采集进度:"), 1, 0)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(65)
        self.progress.setFormat("%v / 100 点")
        layout.addWidget(self.progress, 1, 1)
        
        group.setLayout(layout)
        return group
    
    def create_button_group(self) -> QGroupBox:
        """创建按钮控件组"""
        group = QGroupBox("QPushButton - 按钮")
        layout = QHBoxLayout()
        
        # 普通按钮
        btn_normal = QPushButton("普通按钮")
        btn_normal.clicked.connect(self.on_normal_click)
        
        # 禁用按钮
        btn_disabled = QPushButton("禁用按钮")
        btn_disabled.setEnabled(False)
        
        # 带图标样式的按钮
        btn_start = QPushButton("▶ 开始")
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #219a52; }
            QPushButton:pressed { background-color: #1e8449; }
        """)
        btn_start.clicked.connect(self.on_start_click)
        
        btn_stop = QPushButton("■ 停止")
        btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c0392b; }
            QPushButton:pressed { background-color: #a93226; }
        """)
        btn_stop.clicked.connect(self.on_stop_click)
        
        # 读取设置按钮
        btn_read = QPushButton("读取当前设置")
        btn_read.clicked.connect(self.on_read_settings)
        
        layout.addWidget(btn_normal)
        layout.addWidget(btn_disabled)
        layout.addWidget(btn_start)
        layout.addWidget(btn_stop)
        layout.addWidget(btn_read)
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    # ========== 按钮事件处理函数 ==========
    
    def on_normal_click(self):
        """普通按钮点击"""
        print("普通按钮被点击")
    
    def on_start_click(self):
        """开始按钮点击"""
        print("开始按钮被点击 - 开始采集...")
    
    def on_stop_click(self):
        """停止按钮点击"""
        print("停止按钮被点击 - 停止采集")
    
    def on_read_settings(self):
        """读取当前所有控件的设置"""
        print("\n" + "=" * 50)
        print("当前设置:")
        print("=" * 50)
        print(f"文本输入: {self.input_normal.text()}")
        print(f"采样点数: {self.spin_int.value()} 点")
        print(f"采样频率: {self.spin_freq.value()} Hz")
        print(f"目标温度: {self.spin_temp.value()} K")
        print(f"电压设置: {self.spin_voltage.value()} V")
        print(f"量程选择: {self.combo_range.currentText()}")
        print(f"测量通道: {self.combo_channel.currentText()}")
        print(f"自动量程: {'是' if self.check_auto.isChecked() else '否'}")
        print(f"启用平均: {'是' if self.check_avg.isChecked() else '否'}")
        print(f"记录日志: {'是' if self.check_log.isChecked() else '否'}")
        print(f"增益调节: {self.slider_gain.value()}")
        print("=" * 50)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    window = WidgetShowcase()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

