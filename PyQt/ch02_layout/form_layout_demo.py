"""
示例程序：表单布局
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示QFormLayout的使用，包括：
    - 基本的标签-控件配对
    - 表单布局选项
    - 实验参数输入表单示例

运行方式：
    python form_layout_demo.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QTextEdit, QFormLayout, QVBoxLayout, QHBoxLayout, QGroupBox
)
from PyQt6.QtCore import Qt


class FormLayoutDemo(QWidget):
    """表单布局演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QFormLayout 表单布局演示")
        self.setMinimumSize(450, 350)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        main_layout.addWidget(self.create_basic_form())
        main_layout.addWidget(self.create_styled_form())
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #9b59b6;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #9b59b6;
            }
        """)
    
    def create_basic_form(self) -> QGroupBox:
        """创建基本表单"""
        group = QGroupBox("基本表单布局")
        
        layout = QFormLayout()
        layout.setSpacing(10)
        
        # 使用addRow添加标签-控件对
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("请输入姓名")
        layout.addRow("姓名:", self.input_name)
        
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("example@email.com")
        layout.addRow("邮箱:", self.input_email)
        
        self.spin_age = QSpinBox()
        self.spin_age.setRange(0, 120)
        self.spin_age.setValue(25)
        layout.addRow("年龄:", self.spin_age)
        
        self.combo_dept = QComboBox()
        self.combo_dept.addItems(["物理系", "化学系", "数学系", "计算机系"])
        layout.addRow("院系:", self.combo_dept)
        
        group.setLayout(layout)
        return group
    
    def create_styled_form(self) -> QGroupBox:
        """创建带样式的表单"""
        group = QGroupBox("带样式的表单（必填项标红）")
        
        layout = QFormLayout()
        layout.setSpacing(10)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 必填项使用红色星号
        label_required = QLabel("项目名称: <span style='color:red'>*</span>")
        label_required.setTextFormat(Qt.TextFormat.RichText)
        self.input_project = QLineEdit()
        layout.addRow(label_required, self.input_project)
        
        label_required2 = QLabel("负责人: <span style='color:red'>*</span>")
        label_required2.setTextFormat(Qt.TextFormat.RichText)
        self.input_leader = QLineEdit()
        layout.addRow(label_required2, self.input_leader)
        
        # 可选项
        self.input_note = QLineEdit()
        self.input_note.setPlaceholderText("(可选)")
        layout.addRow("备注:", self.input_note)
        
        group.setLayout(layout)
        return group


class ExperimentParameterForm(QMainWindow):
    """
    实验参数输入表单
    
    模拟实际科研中的实验参数配置界面
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("实验参数配置")
        self.setMinimumSize(500, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("X射线衍射实验参数")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 各部分表单
        main_layout.addWidget(self.create_sample_section())
        main_layout.addWidget(self.create_scan_section())
        main_layout.addWidget(self.create_detector_section())
        main_layout.addWidget(self.create_button_section())
        
        main_layout.addStretch()
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f8f9fa; }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding: 15px;
                padding-top: 25px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #3498db;
            }
            QLabel { font-size: 12px; color: #2c3e50; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 6px 10px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background-color: white;
                font-size: 12px;
                min-width: 150px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QCheckBox { font-size: 12px; }
            QPushButton {
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
    
    def create_sample_section(self) -> QGroupBox:
        """样品信息区"""
        group = QGroupBox("样品信息")
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.input_sample_name = QLineEdit()
        self.input_sample_name.setPlaceholderText("例如: LaFeAsO_1x")
        layout.addRow("样品名称:", self.input_sample_name)
        
        self.input_sample_id = QLineEdit()
        self.input_sample_id.setPlaceholderText("例如: 2024-XRD-001")
        layout.addRow("样品编号:", self.input_sample_id)
        
        self.combo_sample_type = QComboBox()
        self.combo_sample_type.addItems(["粉末", "单晶", "薄膜", "块体"])
        layout.addRow("样品类型:", self.combo_sample_type)
        
        self.input_composition = QLineEdit()
        self.input_composition.setPlaceholderText("化学式或成分描述")
        layout.addRow("成分:", self.input_composition)
        
        group.setLayout(layout)
        return group
    
    def create_scan_section(self) -> QGroupBox:
        """扫描参数区"""
        group = QGroupBox("扫描参数")
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 2θ范围
        self.spin_2theta_start = QDoubleSpinBox()
        self.spin_2theta_start.setRange(0, 180)
        self.spin_2theta_start.setValue(10.0)
        self.spin_2theta_start.setSuffix("°")
        layout.addRow("起始角 2θ:", self.spin_2theta_start)
        
        self.spin_2theta_end = QDoubleSpinBox()
        self.spin_2theta_end.setRange(0, 180)
        self.spin_2theta_end.setValue(90.0)
        self.spin_2theta_end.setSuffix("°")
        layout.addRow("终止角 2θ:", self.spin_2theta_end)
        
        self.spin_step = QDoubleSpinBox()
        self.spin_step.setRange(0.001, 1.0)
        self.spin_step.setValue(0.02)
        self.spin_step.setDecimals(3)
        self.spin_step.setSuffix("°")
        layout.addRow("步进:", self.spin_step)
        
        self.spin_time = QDoubleSpinBox()
        self.spin_time.setRange(0.1, 60.0)
        self.spin_time.setValue(1.0)
        self.spin_time.setSuffix(" s")
        layout.addRow("每步时间:", self.spin_time)
        
        # 扫描模式
        self.combo_scan_mode = QComboBox()
        self.combo_scan_mode.addItems([
            "连续扫描 (Continuous)",
            "步进扫描 (Step)",
            "快速扫描 (Fast)"
        ])
        layout.addRow("扫描模式:", self.combo_scan_mode)
        
        group.setLayout(layout)
        return group
    
    def create_detector_section(self) -> QGroupBox:
        """探测器设置区"""
        group = QGroupBox("探测器设置")
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.combo_radiation = QComboBox()
        self.combo_radiation.addItems([
            "Cu Kα (1.5406 Å)",
            "Mo Kα (0.7107 Å)", 
            "Co Kα (1.7889 Å)",
            "Ag Kα (0.5594 Å)"
        ])
        layout.addRow("X射线源:", self.combo_radiation)
        
        self.spin_voltage = QDoubleSpinBox()
        self.spin_voltage.setRange(20, 60)
        self.spin_voltage.setValue(40)
        self.spin_voltage.setSuffix(" kV")
        layout.addRow("管电压:", self.spin_voltage)
        
        self.spin_current = QDoubleSpinBox()
        self.spin_current.setRange(10, 60)
        self.spin_current.setValue(40)
        self.spin_current.setSuffix(" mA")
        layout.addRow("管电流:", self.spin_current)
        
        self.check_monochromator = QCheckBox("使用单色器")
        self.check_monochromator.setChecked(True)
        layout.addRow("", self.check_monochromator)
        
        self.check_anti_scatter = QCheckBox("防散射狭缝")
        self.check_anti_scatter.setChecked(True)
        layout.addRow("", self.check_anti_scatter)
        
        group.setLayout(layout)
        return group
    
    def create_button_section(self) -> QWidget:
        """按钮区"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        btn_save = QPushButton("保存配置")
        btn_save.setStyleSheet("background-color: #27ae60; color: white;")
        btn_save.clicked.connect(self.save_config)
        
        btn_load = QPushButton("加载配置")
        btn_load.setStyleSheet("background-color: #3498db; color: white;")
        
        btn_start = QPushButton("▶ 开始扫描")
        btn_start.setStyleSheet("background-color: #e74c3c; color: white;")
        btn_start.clicked.connect(self.start_scan)
        
        layout.addWidget(btn_save)
        layout.addWidget(btn_load)
        layout.addStretch()
        layout.addWidget(btn_start)
        
        return widget
    
    def save_config(self):
        """保存配置"""
        config = {
            "sample_name": self.input_sample_name.text(),
            "sample_id": self.input_sample_id.text(),
            "sample_type": self.combo_sample_type.currentText(),
            "2theta_start": self.spin_2theta_start.value(),
            "2theta_end": self.spin_2theta_end.value(),
            "step": self.spin_step.value(),
            "time_per_step": self.spin_time.value(),
            "radiation": self.combo_radiation.currentText(),
            "voltage": self.spin_voltage.value(),
            "current": self.spin_current.value(),
        }
        
        print("\n保存配置:")
        print("-" * 40)
        for key, value in config.items():
            print(f"  {key}: {value}")
        print("-" * 40)
    
    def start_scan(self):
        """开始扫描"""
        sample = self.input_sample_name.text() or "(未命名)"
        start = self.spin_2theta_start.value()
        end = self.spin_2theta_end.value()
        step = self.spin_step.value()
        
        points = int((end - start) / step) + 1
        total_time = points * self.spin_time.value()
        
        print(f"\n开始扫描: {sample}")
        print(f"  范围: {start}° - {end}°")
        print(f"  步进: {step}°")
        print(f"  总点数: {points}")
        print(f"  预计时间: {total_time:.1f} 秒 ({total_time/60:.1f} 分钟)")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 基本演示
    demo = FormLayoutDemo()
    demo.show()
    
    # 实验参数表单
    experiment = ExperimentParameterForm()
    experiment.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

