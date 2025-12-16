"""
示例程序：连接内置信号
所属章节：第三章 - 信号与槽机制

功能说明：
    演示PyQt各种控件的内置信号，包括：
    - QPushButton: clicked, pressed, released, toggled
    - QLineEdit: textChanged, returnPressed, editingFinished
    - QSpinBox/QDoubleSpinBox: valueChanged
    - QComboBox: currentIndexChanged, currentTextChanged
    - QCheckBox: stateChanged, toggled
    - QSlider: valueChanged, sliderMoved, sliderReleased

运行方式：
    python builtin_signals.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QSlider, QProgressBar, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QGroupBox
)
from PyQt6.QtCore import Qt
from datetime import datetime


class BuiltinSignalsDemo(QMainWindow):
    """内置信号演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("控件内置信号演示")
        self.setMinimumSize(750, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(15)
        
        # 左侧：控件区域
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.create_button_group())
        left_layout.addWidget(self.create_input_group())
        left_layout.addWidget(self.create_selection_group())
        left_layout.addWidget(self.create_slider_group())
        main_layout.addLayout(left_layout, stretch=2)
        
        # 右侧：日志区域
        main_layout.addWidget(self.create_log_group(), stretch=1)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
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
            QPushButton {
                padding: 6px 12px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1c598a; }
            QPushButton:checked { background-color: #27ae60; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def create_button_group(self) -> QGroupBox:
        """按钮信号组"""
        group = QGroupBox("QPushButton 信号")
        layout = QGridLayout()
        
        # clicked信号
        btn_click = QPushButton("clicked")
        btn_click.clicked.connect(lambda: self.log("clicked", "按钮被点击"))
        layout.addWidget(QLabel("点击信号:"), 0, 0)
        layout.addWidget(btn_click, 0, 1)
        
        # pressed/released信号
        btn_press = QPushButton("pressed/released")
        btn_press.pressed.connect(lambda: self.log("pressed", "按钮被按下"))
        btn_press.released.connect(lambda: self.log("released", "按钮被释放"))
        layout.addWidget(QLabel("按下/释放:"), 1, 0)
        layout.addWidget(btn_press, 1, 1)
        
        # toggled信号（可切换按钮）
        btn_toggle = QPushButton("toggled (可切换)")
        btn_toggle.setCheckable(True)
        btn_toggle.toggled.connect(
            lambda checked: self.log("toggled", f"状态: {'选中' if checked else '未选中'}")
        )
        layout.addWidget(QLabel("切换信号:"), 2, 0)
        layout.addWidget(btn_toggle, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_input_group(self) -> QGroupBox:
        """输入控件信号组"""
        group = QGroupBox("QLineEdit 信号")
        layout = QFormLayout()
        
        # textChanged信号
        line_text = QLineEdit()
        line_text.setPlaceholderText("输入文本查看 textChanged")
        line_text.textChanged.connect(
            lambda text: self.log("textChanged", f"文本: '{text}'")
        )
        layout.addRow("textChanged:", line_text)
        
        # returnPressed信号
        line_return = QLineEdit()
        line_return.setPlaceholderText("按回车触发 returnPressed")
        line_return.returnPressed.connect(
            lambda: self.log("returnPressed", f"回车! 内容: '{line_return.text()}'")
        )
        layout.addRow("returnPressed:", line_return)
        
        # editingFinished信号
        line_finish = QLineEdit()
        line_finish.setPlaceholderText("失去焦点或回车触发")
        line_finish.editingFinished.connect(
            lambda: self.log("editingFinished", f"编辑完成: '{line_finish.text()}'")
        )
        layout.addRow("editingFinished:", line_finish)
        
        group.setLayout(layout)
        return group
    
    def create_selection_group(self) -> QGroupBox:
        """选择控件信号组"""
        group = QGroupBox("选择控件信号")
        layout = QGridLayout()
        
        # QSpinBox valueChanged
        layout.addWidget(QLabel("QSpinBox:"), 0, 0)
        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.valueChanged.connect(
            lambda v: self.log("valueChanged", f"SpinBox值: {v}")
        )
        layout.addWidget(spin, 0, 1)
        
        # QDoubleSpinBox valueChanged
        layout.addWidget(QLabel("QDoubleSpinBox:"), 1, 0)
        dspin = QDoubleSpinBox()
        dspin.setRange(0, 100)
        dspin.setDecimals(2)
        dspin.valueChanged.connect(
            lambda v: self.log("valueChanged", f"DoubleSpinBox值: {v:.2f}")
        )
        layout.addWidget(dspin, 1, 1)
        
        # QComboBox currentIndexChanged
        layout.addWidget(QLabel("QComboBox:"), 2, 0)
        combo = QComboBox()
        combo.addItems(["选项A", "选项B", "选项C", "选项D"])
        combo.currentIndexChanged.connect(
            lambda i: self.log("currentIndexChanged", f"索引: {i}")
        )
        combo.currentTextChanged.connect(
            lambda t: self.log("currentTextChanged", f"文本: {t}")
        )
        layout.addWidget(combo, 2, 1)
        
        # QCheckBox stateChanged/toggled
        layout.addWidget(QLabel("QCheckBox:"), 3, 0)
        check = QCheckBox("启用选项")
        check.stateChanged.connect(
            lambda state: self.log("stateChanged", f"状态码: {state}")
        )
        check.toggled.connect(
            lambda checked: self.log("toggled", f"选中: {checked}")
        )
        layout.addWidget(check, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def create_slider_group(self) -> QGroupBox:
        """滑动条信号组"""
        group = QGroupBox("QSlider 信号")
        layout = QVBoxLayout()
        
        # 滑动条
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        
        # 值标签
        self.slider_label = QLabel("值: 50")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 连接信号
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.slider.sliderMoved.connect(
            lambda v: self.log("sliderMoved", f"滑块拖动到: {v}")
        )
        self.slider.sliderPressed.connect(
            lambda: self.log("sliderPressed", "滑块被按下")
        )
        self.slider.sliderReleased.connect(
            lambda: self.log("sliderReleased", f"滑块释放，最终值: {self.slider.value()}")
        )
        
        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)
        
        # 说明
        info = QLabel(
            "• valueChanged: 值改变时触发（拖动或程序设置）\n"
            "• sliderMoved: 仅用户拖动时触发\n"
            "• sliderPressed: 按下滑块时触发\n"
            "• sliderReleased: 释放滑块时触发"
        )
        info.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        return group
    
    def create_log_group(self) -> QGroupBox:
        """日志组"""
        group = QGroupBox("信号日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2e;
                color: #00ff88;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: none;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        btn_clear = QPushButton("清除日志")
        btn_clear.clicked.connect(self.log_text.clear)
        layout.addWidget(btn_clear)
        
        group.setLayout(layout)
        return group
    
    def on_slider_value_changed(self, value: int):
        """滑动条值变化"""
        self.slider_label.setText(f"值: {value}")
        # 不记录每次变化，太频繁
    
    def log(self, signal_name: str, message: str):
        """记录日志"""
        time_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_text.append(f"[{time_str}] <{signal_name}> {message}")
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class SignalChainDemo(QWidget):
    """信号链演示：信号连接信号"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("信号链演示")
        self.setMinimumSize(350, 200)
        
        layout = QVBoxLayout()
        
        # 说明
        info = QLabel(
            "信号可以连接到另一个信号\n"
            "button1.clicked → button2.click()\n"
            "点击按钮1会触发按钮2"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("background-color: #fef9e7; padding: 10px; border-radius: 5px;")
        layout.addWidget(info)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.btn1 = QPushButton("按钮1 (点我)")
        self.btn1.setStyleSheet("background-color: #3498db; color: white; padding: 15px;")
        
        self.btn2 = QPushButton("按钮2 (会跟着触发)")
        self.btn2.setStyleSheet("background-color: #e74c3c; color: white; padding: 15px;")
        
        # 信号链：按钮1的clicked连接到按钮2的click
        self.btn1.clicked.connect(self.btn2.click)
        
        # 按钮2的实际响应
        self.btn2.clicked.connect(self.on_btn2_clicked)
        
        btn_layout.addWidget(self.btn1)
        btn_layout.addWidget(self.btn2)
        layout.addLayout(btn_layout)
        
        # 状态
        self.label_status = QLabel("等待点击...")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)
        
        self.setLayout(layout)
    
    def on_btn2_clicked(self):
        """按钮2点击响应"""
        self.label_status.setText("按钮2被触发了！（可能是通过按钮1的信号链）")
        self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 主演示窗口
    window = BuiltinSignalsDemo()
    window.show()
    
    # 信号链演示
    chain_demo = SignalChainDemo()
    chain_demo.move(800, 100)
    chain_demo.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

