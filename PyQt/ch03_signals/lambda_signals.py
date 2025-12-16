"""
示例程序：Lambda表达式与信号
所属章节：第三章 - 信号与槽机制

功能说明：
    演示Lambda表达式在信号槽中的应用，包括：
    - 传递额外参数
    - 参数转换
    - 循环中正确捕获变量
    - functools.partial替代方案
    - 温度转换器示例

运行方式：
    python lambda_signals.py
"""

import sys
from functools import partial
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt


class LambdaBasicDemo(QWidget):
    """Lambda基础演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Lambda表达式与信号 - 基础演示")
        self.setMinimumSize(500, 450)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 演示1：传递额外参数
        main_layout.addWidget(self.create_extra_params_demo())
        
        # 演示2：循环中的正确用法
        main_layout.addWidget(self.create_loop_demo())
        
        # 演示3：参数转换
        main_layout.addWidget(self.create_transform_demo())
        
        # 日志区
        main_layout.addWidget(self.create_log_area())
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QWidget { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #d35400;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #d35400; }
        """)
    
    def create_extra_params_demo(self) -> QGroupBox:
        """传递额外参数演示"""
        group = QGroupBox("1. Lambda传递额外参数")
        layout = QVBoxLayout()
        
        info = QLabel("使用Lambda可以将额外的参数传递给槽函数")
        info.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        # 创建按钮，每个按钮传递不同的消息
        messages = ["你好！", "欢迎使用PyQt", "Lambda真好用"]
        
        for i, msg in enumerate(messages):
            btn = QPushButton(f"消息 {i+1}")
            # 使用Lambda传递额外参数
            btn.clicked.connect(lambda checked, m=msg: self.show_message(m))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        return group
    
    def create_loop_demo(self) -> QGroupBox:
        """循环中的Lambda演示"""
        group = QGroupBox("2. 循环中正确捕获变量")
        layout = QVBoxLayout()
        
        info = QLabel(
            "错误: lambda: print(i) → 所有按钮都会打印最后的值\n"
            "正确: lambda checked, idx=i: print(idx) → 使用默认参数捕获"
        )
        info.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(info)
        
        btn_layout = QHBoxLayout()
        
        # 正确的方式：使用默认参数捕获循环变量
        for i in range(5):
            btn = QPushButton(f"按钮 {i}")
            # 注意: idx=i 在循环时捕获当前的i值
            btn.clicked.connect(lambda checked, idx=i: self.log(f"点击了按钮 {idx}"))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        group.setLayout(layout)
        return group
    
    def create_transform_demo(self) -> QGroupBox:
        """参数转换演示"""
        group = QGroupBox("3. Lambda参数转换")
        layout = QGridLayout()
        
        # 滑动条值转换为百分比
        layout.addWidget(QLabel("滑动条 (0-100):"), 0, 0)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        layout.addWidget(slider, 0, 1)
        
        label_percent = QLabel("50%")
        label_percent.setStyleSheet("font-weight: bold; min-width: 50px;")
        layout.addWidget(label_percent, 0, 2)
        
        # 使用Lambda转换值
        slider.valueChanged.connect(lambda v: label_percent.setText(f"{v}%"))
        slider.valueChanged.connect(lambda v: self.log(f"滑动条值: {v}%"))
        
        # SpinBox值乘以系数
        layout.addWidget(QLabel("数值 × 0.1:"), 1, 0)
        spin = QSpinBox()
        spin.setRange(0, 100)
        spin.setValue(10)
        layout.addWidget(spin, 1, 1)
        
        label_scaled = QLabel("1.0")
        label_scaled.setStyleSheet("font-weight: bold; min-width: 50px;")
        layout.addWidget(label_scaled, 1, 2)
        
        # Lambda进行数值转换
        spin.valueChanged.connect(lambda v: label_scaled.setText(f"{v * 0.1:.1f}"))
        
        group.setLayout(layout)
        return group
    
    def create_log_area(self) -> QGroupBox:
        """日志区域"""
        group = QGroupBox("事件日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            background-color: #2c3e50;
            color: #00ff88;
            font-family: Consolas, monospace;
            border-radius: 5px;
        """)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def show_message(self, message: str):
        """显示消息"""
        self.log(f"消息: {message}")
    
    def log(self, text: str):
        """添加日志"""
        self.log_text.append(text)


class TemperatureConverter(QMainWindow):
    """
    温度转换器
    
    演示使用Lambda实现控件间的实时联动
    """
    
    def __init__(self):
        super().__init__()
        self._updating = False  # 防止循环更新
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        self.setWindowTitle("温度转换器 - Lambda实时联动")
        self.setMinimumSize(450, 300)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("🌡️ 温度单位转换器")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 温度输入区
        temp_layout = QGridLayout()
        temp_layout.setSpacing(15)
        
        # 摄氏度
        temp_layout.addWidget(QLabel("摄氏度 (°C):"), 0, 0)
        self.spin_celsius = QDoubleSpinBox()
        self.spin_celsius.setRange(-273.15, 1000)
        self.spin_celsius.setValue(25)
        self.spin_celsius.setDecimals(2)
        self.spin_celsius.setSuffix(" °C")
        self.spin_celsius.setStyleSheet("font-size: 16px; padding: 8px;")
        temp_layout.addWidget(self.spin_celsius, 0, 1)
        
        # 华氏度
        temp_layout.addWidget(QLabel("华氏度 (°F):"), 1, 0)
        self.spin_fahrenheit = QDoubleSpinBox()
        self.spin_fahrenheit.setRange(-459.67, 1832)
        self.spin_fahrenheit.setValue(77)
        self.spin_fahrenheit.setDecimals(2)
        self.spin_fahrenheit.setSuffix(" °F")
        self.spin_fahrenheit.setStyleSheet("font-size: 16px; padding: 8px;")
        temp_layout.addWidget(self.spin_fahrenheit, 1, 1)
        
        # 开尔文
        temp_layout.addWidget(QLabel("开尔文 (K):"), 2, 0)
        self.spin_kelvin = QDoubleSpinBox()
        self.spin_kelvin.setRange(0, 1273.15)
        self.spin_kelvin.setValue(298.15)
        self.spin_kelvin.setDecimals(2)
        self.spin_kelvin.setSuffix(" K")
        self.spin_kelvin.setStyleSheet("font-size: 16px; padding: 8px;")
        temp_layout.addWidget(self.spin_kelvin, 2, 1)
        
        main_layout.addLayout(temp_layout)
        
        # 公式说明
        formula = QLabel(
            "转换公式:\n"
            "°F = °C × 9/5 + 32\n"
            "K = °C + 273.15"
        )
        formula.setStyleSheet("""
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            color: #7f8c8d;
        """)
        main_layout.addWidget(formula)
        
        main_layout.addStretch()
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QLabel { color: #2c3e50; font-size: 14px; }
            QDoubleSpinBox {
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: white;
            }
            QDoubleSpinBox:focus {
                border-color: #e74c3c;
            }
        """)
    
    def connect_signals(self):
        """连接信号实现联动"""
        # 摄氏度改变时，更新华氏度和开尔文
        self.spin_celsius.valueChanged.connect(self.on_celsius_changed)
        
        # 华氏度改变时，更新摄氏度和开尔文
        self.spin_fahrenheit.valueChanged.connect(self.on_fahrenheit_changed)
        
        # 开尔文改变时，更新摄氏度和华氏度
        self.spin_kelvin.valueChanged.connect(self.on_kelvin_changed)
    
    def on_celsius_changed(self, celsius: float):
        """摄氏度改变"""
        if self._updating:
            return
        
        self._updating = True
        
        # 使用Lambda进行转换
        fahrenheit = celsius * 9 / 5 + 32
        kelvin = celsius + 273.15
        
        self.spin_fahrenheit.setValue(fahrenheit)
        self.spin_kelvin.setValue(kelvin)
        
        self._updating = False
    
    def on_fahrenheit_changed(self, fahrenheit: float):
        """华氏度改变"""
        if self._updating:
            return
        
        self._updating = True
        
        celsius = (fahrenheit - 32) * 5 / 9
        kelvin = celsius + 273.15
        
        self.spin_celsius.setValue(celsius)
        self.spin_kelvin.setValue(kelvin)
        
        self._updating = False
    
    def on_kelvin_changed(self, kelvin: float):
        """开尔文改变"""
        if self._updating:
            return
        
        self._updating = True
        
        celsius = kelvin - 273.15
        fahrenheit = celsius * 9 / 5 + 32
        
        self.spin_celsius.setValue(celsius)
        self.spin_fahrenheit.setValue(fahrenheit)
        
        self._updating = False


class PartialDemo(QWidget):
    """functools.partial演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("functools.partial 替代Lambda")
        self.setMinimumSize(400, 250)
        
        layout = QVBoxLayout()
        
        # 说明
        info = QLabel(
            "functools.partial 可以替代复杂的Lambda\n\n"
            "Lambda: button.clicked.connect(lambda: func(a, b))\n"
            "Partial: button.clicked.connect(partial(func, a, b))"
        )
        info.setStyleSheet("""
            background-color: #fef9e7;
            padding: 15px;
            border-radius: 5px;
            font-family: Consolas, monospace;
        """)
        layout.addWidget(info)
        
        # 按钮演示
        btn_layout = QHBoxLayout()
        
        actions = [
            ("保存", "save", "file.txt"),
            ("加载", "load", "file.txt"),
            ("删除", "delete", "file.txt"),
        ]
        
        for label, action, filename in actions:
            btn = QPushButton(label)
            # 使用partial替代lambda
            btn.clicked.connect(partial(self.handle_action, action, filename))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        
        # 结果标签
        self.label_result = QLabel("点击按钮查看效果")
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_result.setStyleSheet("""
            font-size: 14px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
        """)
        layout.addWidget(self.label_result)
        
        self.setLayout(layout)
    
    def handle_action(self, action: str, filename: str):
        """处理动作"""
        self.label_result.setText(f"执行: {action}('{filename}')")
        print(f"Action: {action}, File: {filename}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Lambda基础演示
    basic = LambdaBasicDemo()
    basic.show()
    
    # 温度转换器
    converter = TemperatureConverter()
    converter.move(550, 50)
    converter.show()
    
    # Partial演示
    partial_demo = PartialDemo()
    partial_demo.move(550, 400)
    partial_demo.show()
    
    # 打印说明
    print("=" * 50)
    print("Lambda表达式与信号 演示")
    print("=" * 50)
    print("常见用法:")
    print("  1. 传递额外参数: lambda: func(extra_arg)")
    print("  2. 循环捕获变量: lambda _, i=i: func(i)")
    print("  3. 参数转换: lambda v: label.setText(str(v))")
    print("  4. 忽略参数: lambda _: do_something()")
    print("  5. 多步操作: lambda: (step1(), step2())")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

