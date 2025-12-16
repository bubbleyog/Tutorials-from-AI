"""
示例程序：网格布局
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示QGridLayout的使用，包括：
    - 基本的行列布局
    - 跨行跨列（rowSpan, colSpan）
    - 行列拉伸比例
    - 物理公式计算器示例

运行方式：
    python grid_layout_demo.py
"""

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QDoubleSpinBox, QComboBox, QGridLayout, QVBoxLayout, 
    QHBoxLayout, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class GridLayoutDemo(QWidget):
    """网格布局演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QGridLayout 网格布局演示")
        self.setMinimumSize(500, 400)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        main_layout.addWidget(self.create_basic_grid())
        main_layout.addWidget(self.create_span_demo())
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #27ae60;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #27ae60;
            }
            QPushButton {
                padding: 10px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #219a52; }
        """)
    
    def create_basic_grid(self) -> QGroupBox:
        """创建基本网格布局"""
        group = QGroupBox("基本网格布局 - 3x3 按钮矩阵")
        
        layout = QGridLayout()
        layout.setSpacing(5)
        
        # 创建3x3按钮网格
        for row in range(3):
            for col in range(3):
                btn = QPushButton(f"({row}, {col})")
                layout.addWidget(btn, row, col)
        
        group.setLayout(layout)
        return group
    
    def create_span_demo(self) -> QGroupBox:
        """创建跨行跨列演示"""
        group = QGroupBox("跨行跨列 - addWidget(widget, row, col, rowSpan, colSpan)")
        
        layout = QGridLayout()
        layout.setSpacing(5)
        
        # 标题（跨3列）
        title = QLabel("这个标签跨越3列 (0, 0, 1, 3)")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "background-color: #3498db; color: white; "
            "padding: 10px; border-radius: 4px;"
        )
        layout.addWidget(title, 0, 0, 1, 3)  # row=0, col=0, rowSpan=1, colSpan=3
        
        # 左侧大按钮（跨2行）
        left_btn = QPushButton("跨2行\n(1,0,2,1)")
        left_btn.setStyleSheet(
            "background-color: #e74c3c; min-height: 80px;"
        )
        layout.addWidget(left_btn, 1, 0, 2, 1)  # row=1, col=0, rowSpan=2, colSpan=1
        
        # 右侧普通按钮
        layout.addWidget(QPushButton("(1, 1)"), 1, 1)
        layout.addWidget(QPushButton("(1, 2)"), 1, 2)
        layout.addWidget(QPushButton("(2, 1)"), 2, 1)
        layout.addWidget(QPushButton("(2, 2)"), 2, 2)
        
        # 底部（跨3列）
        bottom = QLabel("底部标签跨越3列 (3, 0, 1, 3)")
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom.setStyleSheet(
            "background-color: #9b59b6; color: white; "
            "padding: 10px; border-radius: 4px;"
        )
        layout.addWidget(bottom, 3, 0, 1, 3)
        
        group.setLayout(layout)
        return group


class PhysicsCalculator(QMainWindow):
    """
    物理公式计算器
    
    使用网格布局创建的实用物理计算工具
    支持多种常用物理公式计算
    """
    
    # 物理常数
    CONSTANTS = {
        "h": 6.62607015e-34,      # 普朗克常数 (J·s)
        "hbar": 1.054571817e-34,  # 约化普朗克常数 (J·s)
        "c": 299792458,           # 光速 (m/s)
        "e": 1.602176634e-19,     # 元电荷 (C)
        "me": 9.1093837015e-31,   # 电子质量 (kg)
        "mp": 1.67262192369e-27,  # 质子质量 (kg)
        "kB": 1.380649e-23,       # 玻尔兹曼常数 (J/K)
        "NA": 6.02214076e23,      # 阿伏伽德罗常数 (1/mol)
    }
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("物理公式计算器")
        self.setMinimumSize(450, 400)
        
        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("物理公式计算器")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 公式选择和参数输入
        main_layout.addWidget(self.create_formula_section())
        
        # 计算按钮和结果
        main_layout.addWidget(self.create_result_section())
        
        # 物理常数参考
        main_layout.addWidget(self.create_constants_section())
        
        main_layout.addStretch()
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2c3e50;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2c3e50;
            }
            QLabel { color: #2c3e50; }
            QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
    
    def create_formula_section(self) -> QGroupBox:
        """创建公式选择和参数输入区"""
        group = QGroupBox("公式与参数")
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 第0行：公式选择
        layout.addWidget(QLabel("选择公式:"), 0, 0)
        self.combo_formula = QComboBox()
        self.combo_formula.addItems([
            "动能 E = ½mv²",
            "动量 p = mv",
            "德布罗意波长 λ = h/p",
            "光子能量 E = hν",
            "爱因斯坦质能 E = mc²",
        ])
        self.combo_formula.currentIndexChanged.connect(self.on_formula_changed)
        layout.addWidget(self.combo_formula, 0, 1, 1, 2)
        
        # 第1行：参数1
        self.label_param1 = QLabel("质量 m:")
        layout.addWidget(self.label_param1, 1, 0)
        self.spin_param1 = QDoubleSpinBox()
        self.spin_param1.setRange(1e-35, 1e35)
        self.spin_param1.setDecimals(6)
        self.spin_param1.setValue(9.109e-31)  # 电子质量
        layout.addWidget(self.spin_param1, 1, 1)
        self.combo_unit1 = QComboBox()
        self.combo_unit1.addItems(["kg", "g", "u"])
        layout.addWidget(self.combo_unit1, 1, 2)
        
        # 第2行：参数2
        self.label_param2 = QLabel("速度 v:")
        layout.addWidget(self.label_param2, 2, 0)
        self.spin_param2 = QDoubleSpinBox()
        self.spin_param2.setRange(0, 3e8)
        self.spin_param2.setDecimals(2)
        self.spin_param2.setValue(1e6)  # 1000 km/s
        layout.addWidget(self.spin_param2, 2, 1)
        self.combo_unit2 = QComboBox()
        self.combo_unit2.addItems(["m/s", "km/s", "c"])
        layout.addWidget(self.combo_unit2, 2, 2)
        
        # 设置列拉伸
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_result_section(self) -> QGroupBox:
        """创建结果显示区"""
        group = QGroupBox("计算结果")
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 计算按钮
        self.btn_calculate = QPushButton("计算")
        self.btn_calculate.clicked.connect(self.calculate)
        layout.addWidget(self.btn_calculate, 0, 0)
        
        # 结果显示
        self.label_result = QLabel("--")
        self.label_result.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #27ae60; "
            "padding: 10px; background-color: #e8f6e9; border-radius: 5px;"
        )
        self.label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_result, 0, 1, 1, 2)
        
        layout.setColumnStretch(1, 2)
        
        group.setLayout(layout)
        return group
    
    def create_constants_section(self) -> QGroupBox:
        """创建物理常数参考区"""
        group = QGroupBox("物理常数参考")
        group.setCheckable(True)
        group.setChecked(False)
        
        layout = QGridLayout()
        layout.setSpacing(5)
        
        constants_display = [
            ("h (普朗克常数)", f"{self.CONSTANTS['h']:.4e} J·s"),
            ("ℏ (约化普朗克)", f"{self.CONSTANTS['hbar']:.4e} J·s"),
            ("c (光速)", f"{self.CONSTANTS['c']:.0f} m/s"),
            ("e (元电荷)", f"{self.CONSTANTS['e']:.4e} C"),
            ("mₑ (电子质量)", f"{self.CONSTANTS['me']:.4e} kg"),
            ("kB (玻尔兹曼)", f"{self.CONSTANTS['kB']:.4e} J/K"),
        ]
        
        for i, (name, value) in enumerate(constants_display):
            row, col = divmod(i, 2)
            label = QLabel(f"{name}: {value}")
            label.setStyleSheet("font-size: 11px; color: #7f8c8d;")
            layout.addWidget(label, row, col)
        
        group.setLayout(layout)
        return group
    
    def on_formula_changed(self, index: int):
        """公式选择改变时更新参数标签"""
        formulas = [
            ("质量 m:", "速度 v:", ["kg", "g", "u"], ["m/s", "km/s", "c"]),
            ("质量 m:", "速度 v:", ["kg", "g", "u"], ["m/s", "km/s", "c"]),
            ("动量 p:", "(不使用)", ["kg·m/s", "eV/c"], []),
            ("频率 ν:", "(不使用)", ["Hz", "THz", "PHz"], []),
            ("质量 m:", "(不使用)", ["kg", "g", "u"], []),
        ]
        
        param1_label, param2_label, units1, units2 = formulas[index]
        self.label_param1.setText(param1_label)
        self.label_param2.setText(param2_label)
        
        self.combo_unit1.clear()
        self.combo_unit1.addItems(units1)
        
        self.combo_unit2.clear()
        if units2:
            self.combo_unit2.addItems(units2)
            self.combo_unit2.setEnabled(True)
            self.spin_param2.setEnabled(True)
        else:
            self.combo_unit2.setEnabled(False)
            self.spin_param2.setEnabled(False)
    
    def calculate(self):
        """执行计算"""
        formula_index = self.combo_formula.currentIndex()
        
        # 获取参数值（转换为SI单位）
        val1 = self.spin_param1.value()
        val2 = self.spin_param2.value()
        
        # 单位转换
        unit1 = self.combo_unit1.currentText()
        unit2 = self.combo_unit2.currentText()
        
        # 质量单位转换
        if unit1 == "g":
            val1 *= 1e-3
        elif unit1 == "u":
            val1 *= 1.66054e-27
        
        # 速度单位转换
        if unit2 == "km/s":
            val2 *= 1e3
        elif unit2 == "c":
            val2 *= self.CONSTANTS["c"]
        
        try:
            if formula_index == 0:  # 动能
                result = 0.5 * val1 * val2**2
                self.label_result.setText(f"E = {result:.4e} J = {result/self.CONSTANTS['e']:.4e} eV")
            
            elif formula_index == 1:  # 动量
                result = val1 * val2
                self.label_result.setText(f"p = {result:.4e} kg·m/s")
            
            elif formula_index == 2:  # 德布罗意波长
                p = val1  # 动量已经是SI单位
                wavelength = self.CONSTANTS["h"] / p
                self.label_result.setText(f"λ = {wavelength:.4e} m = {wavelength*1e9:.4f} nm")
            
            elif formula_index == 3:  # 光子能量
                freq = val1
                if self.combo_unit1.currentText() == "THz":
                    freq *= 1e12
                elif self.combo_unit1.currentText() == "PHz":
                    freq *= 1e15
                energy = self.CONSTANTS["h"] * freq
                self.label_result.setText(f"E = {energy:.4e} J = {energy/self.CONSTANTS['e']:.4f} eV")
            
            elif formula_index == 4:  # 质能方程
                energy = val1 * self.CONSTANTS["c"]**2
                self.label_result.setText(f"E = {energy:.4e} J = {energy/self.CONSTANTS['e']/1e6:.4f} MeV")
        
        except Exception as e:
            self.label_result.setText(f"计算错误: {str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 显示网格布局演示
    demo = GridLayoutDemo()
    demo.show()
    
    # 显示物理计算器
    calculator = PhysicsCalculator()
    calculator.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

