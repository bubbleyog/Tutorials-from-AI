"""
示例程序：控件属性与方法
所属章节：第一章 - PyQt基础入门

功能说明：
    演示控件的通用属性和方法，包括：
    - 大小与位置设置
    - 可见性与启用状态
    - 样式设置
    - 提示信息
    - 键盘快捷键
    
    本程序模拟一个物理实验参数设置面板

运行方式：
    python widget_properties.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QShortcut, QKeySequence


class ExperimentParameterPanel(QMainWindow):
    """
    实验参数设置面板
    
    模拟低温物理实验的参数设置界面，
    演示PyQt控件的各种属性和方法
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_shortcuts()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("低温磁性测量系统 - 参数设置")
        self.setMinimumSize(450, 550)
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 添加控件组
        main_layout.addWidget(self.create_temperature_group())
        main_layout.addWidget(self.create_magnetic_field_group())
        main_layout.addWidget(self.create_measurement_group())
        main_layout.addWidget(self.create_notes_group())
        main_layout.addWidget(self.create_button_group())
        main_layout.addStretch()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪 | 快捷键: Ctrl+S 应用, Ctrl+R 重置, Ctrl+Q 退出")
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #dcdde1;
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
            QLabel {
                font-size: 12px;
                color: #2c3e50;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QCheckBox {
                font-size: 12px;
                color: #2c3e50;
            }
        """)
    
    def create_temperature_group(self) -> QGroupBox:
        """创建温度设置组"""
        group = QGroupBox("温度控制")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 目标温度
        lbl_target = QLabel("目标温度:")
        lbl_target.setToolTip("设置样品的目标温度")
        layout.addWidget(lbl_target, 0, 0)
        
        self.spin_target_temp = QDoubleSpinBox()
        self.spin_target_temp.setRange(1.5, 400.0)
        self.spin_target_temp.setValue(300.0)
        self.spin_target_temp.setSuffix(" K")
        self.spin_target_temp.setDecimals(1)
        self.spin_target_temp.setSingleStep(1.0)
        self.spin_target_temp.setToolTip("范围: 1.5 K - 400 K")
        self.spin_target_temp.setStatusTip("设置目标温度（1.5K - 400K）")
        layout.addWidget(self.spin_target_temp, 0, 1)
        
        # 升温速率
        lbl_rate = QLabel("升温速率:")
        layout.addWidget(lbl_rate, 1, 0)
        
        self.spin_temp_rate = QDoubleSpinBox()
        self.spin_temp_rate.setRange(0.1, 20.0)
        self.spin_temp_rate.setValue(2.0)
        self.spin_temp_rate.setSuffix(" K/min")
        self.spin_temp_rate.setDecimals(1)
        self.spin_temp_rate.setToolTip("建议速率: 1-5 K/min")
        layout.addWidget(self.spin_temp_rate, 1, 1)
        
        # 温度稳定判据
        lbl_stable = QLabel("稳定判据:")
        layout.addWidget(lbl_stable, 2, 0)
        
        self.spin_temp_stable = QDoubleSpinBox()
        self.spin_temp_stable.setRange(0.001, 1.0)
        self.spin_temp_stable.setValue(0.01)
        self.spin_temp_stable.setSuffix(" K")
        self.spin_temp_stable.setDecimals(3)
        self.spin_temp_stable.setToolTip("温度波动小于此值时认为稳定")
        layout.addWidget(self.spin_temp_stable, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_magnetic_field_group(self) -> QGroupBox:
        """创建磁场设置组"""
        group = QGroupBox("磁场控制")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 目标磁场
        lbl_field = QLabel("目标磁场:")
        layout.addWidget(lbl_field, 0, 0)
        
        self.spin_field = QDoubleSpinBox()
        self.spin_field.setRange(-14.0, 14.0)
        self.spin_field.setValue(0.0)
        self.spin_field.setSuffix(" T")
        self.spin_field.setDecimals(3)
        self.spin_field.setSingleStep(0.1)
        self.spin_field.setToolTip("超导磁体范围: ±14 T")
        layout.addWidget(self.spin_field, 0, 1)
        
        # 扫场速率
        lbl_rate = QLabel("扫场速率:")
        layout.addWidget(lbl_rate, 1, 0)
        
        self.spin_field_rate = QDoubleSpinBox()
        self.spin_field_rate.setRange(0.001, 1.0)
        self.spin_field_rate.setValue(0.1)
        self.spin_field_rate.setSuffix(" T/min")
        self.spin_field_rate.setDecimals(3)
        layout.addWidget(self.spin_field_rate, 1, 1)
        
        # 扫场模式
        lbl_mode = QLabel("扫场模式:")
        layout.addWidget(lbl_mode, 2, 0)
        
        self.combo_field_mode = QComboBox()
        self.combo_field_mode.addItems([
            "单向扫场",
            "双向扫场 (回滞)",
            "零场冷却 (ZFC)",
            "场冷却 (FC)"
        ])
        self.combo_field_mode.setToolTip("选择磁场扫描模式")
        layout.addWidget(self.combo_field_mode, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_measurement_group(self) -> QGroupBox:
        """创建测量设置组"""
        group = QGroupBox("测量参数")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 测量类型
        lbl_type = QLabel("测量类型:")
        layout.addWidget(lbl_type, 0, 0)
        
        self.combo_measure_type = QComboBox()
        self.combo_measure_type.addItems([
            "直流磁化率 (DC)",
            "交流磁化率 (AC)",
            "电阻率",
            "比热"
        ])
        layout.addWidget(self.combo_measure_type, 0, 1)
        
        # 采样点数
        lbl_points = QLabel("采样点数:")
        layout.addWidget(lbl_points, 1, 0)
        
        self.spin_points = QSpinBox()
        self.spin_points.setRange(10, 10000)
        self.spin_points.setValue(100)
        self.spin_points.setSingleStep(10)
        layout.addWidget(self.spin_points, 1, 1)
        
        # 平均次数
        lbl_avg = QLabel("平均次数:")
        layout.addWidget(lbl_avg, 2, 0)
        
        self.spin_average = QSpinBox()
        self.spin_average.setRange(1, 100)
        self.spin_average.setValue(3)
        layout.addWidget(self.spin_average, 2, 1)
        
        # 选项
        self.check_auto_range = QCheckBox("自动量程")
        self.check_auto_range.setChecked(True)
        self.check_auto_range.setToolTip("自动选择最佳测量量程")
        layout.addWidget(self.check_auto_range, 3, 0)
        
        self.check_log_scale = QCheckBox("对数间隔采样")
        self.check_log_scale.setToolTip("使用对数间隔的温度/磁场点")
        layout.addWidget(self.check_log_scale, 3, 1)
        
        group.setLayout(layout)
        return group
    
    def create_notes_group(self) -> QGroupBox:
        """创建备注组"""
        group = QGroupBox("实验备注")
        layout = QVBoxLayout()
        
        # 样品名称
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("样品名称:"))
        self.input_sample_name = QLineEdit()
        self.input_sample_name.setPlaceholderText("例如: Fe3O4_sample_001")
        name_layout.addWidget(self.input_sample_name)
        layout.addLayout(name_layout)
        
        # 实验备注
        note_layout = QHBoxLayout()
        note_layout.addWidget(QLabel("备注:"))
        self.input_note = QLineEdit()
        self.input_note.setPlaceholderText("输入实验备注信息...")
        note_layout.addWidget(self.input_note)
        layout.addLayout(note_layout)
        
        group.setLayout(layout)
        return group
    
    def create_button_group(self) -> QWidget:
        """创建按钮组"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # 应用按钮
        self.btn_apply = QPushButton("应用设置 (Ctrl+S)")
        self.btn_apply.setMinimumHeight(38)
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1c5980; }
        """)
        self.btn_apply.clicked.connect(self.apply_settings)
        
        # 重置按钮
        self.btn_reset = QPushButton("重置 (Ctrl+R)")
        self.btn_reset.setMinimumHeight(38)
        self.btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
            QPushButton:pressed { background-color: #6c7a7d; }
        """)
        self.btn_reset.clicked.connect(self.reset_settings)
        
        # 开始测量按钮
        self.btn_start = QPushButton("▶ 开始测量")
        self.btn_start.setMinimumHeight(38)
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #219a52; }
            QPushButton:pressed { background-color: #1e8449; }
        """)
        self.btn_start.clicked.connect(self.start_measurement)
        
        layout.addWidget(self.btn_apply)
        layout.addWidget(self.btn_reset)
        layout.addStretch()
        layout.addWidget(self.btn_start)
        
        return widget
    
    def setup_shortcuts(self):
        """设置键盘快捷键"""
        # Ctrl+S: 应用设置
        shortcut_apply = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut_apply.activated.connect(self.apply_settings)
        
        # Ctrl+R: 重置设置
        shortcut_reset = QShortcut(QKeySequence("Ctrl+R"), self)
        shortcut_reset.activated.connect(self.reset_settings)
        
        # Ctrl+Q: 退出程序
        shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        shortcut_quit.activated.connect(self.close)
    
    def apply_settings(self):
        """应用当前设置"""
        settings = self.get_all_settings()
        
        print("\n" + "=" * 60)
        print("应用实验设置")
        print("=" * 60)
        
        print("\n[温度控制]")
        print(f"  目标温度: {settings['target_temp']} K")
        print(f"  升温速率: {settings['temp_rate']} K/min")
        print(f"  稳定判据: {settings['temp_stable']} K")
        
        print("\n[磁场控制]")
        print(f"  目标磁场: {settings['field']} T")
        print(f"  扫场速率: {settings['field_rate']} T/min")
        print(f"  扫场模式: {settings['field_mode']}")
        
        print("\n[测量参数]")
        print(f"  测量类型: {settings['measure_type']}")
        print(f"  采样点数: {settings['points']}")
        print(f"  平均次数: {settings['average']}")
        print(f"  自动量程: {'是' if settings['auto_range'] else '否'}")
        print(f"  对数间隔: {'是' if settings['log_scale'] else '否'}")
        
        print("\n[实验信息]")
        print(f"  样品名称: {settings['sample_name'] or '(未设置)'}")
        print(f"  备注: {settings['note'] or '(无)'}")
        
        print("=" * 60)
        
        self.statusBar.showMessage("设置已应用", 3000)
    
    def reset_settings(self):
        """重置为默认值"""
        # 温度设置
        self.spin_target_temp.setValue(300.0)
        self.spin_temp_rate.setValue(2.0)
        self.spin_temp_stable.setValue(0.01)
        
        # 磁场设置
        self.spin_field.setValue(0.0)
        self.spin_field_rate.setValue(0.1)
        self.combo_field_mode.setCurrentIndex(0)
        
        # 测量设置
        self.combo_measure_type.setCurrentIndex(0)
        self.spin_points.setValue(100)
        self.spin_average.setValue(3)
        self.check_auto_range.setChecked(True)
        self.check_log_scale.setChecked(False)
        
        # 备注
        self.input_sample_name.clear()
        self.input_note.clear()
        
        print("设置已重置为默认值")
        self.statusBar.showMessage("设置已重置", 3000)
    
    def start_measurement(self):
        """开始测量（模拟）"""
        sample_name = self.input_sample_name.text()
        if not sample_name:
            self.statusBar.showMessage("警告: 请先输入样品名称!", 3000)
            self.input_sample_name.setFocus()
            self.input_sample_name.setStyleSheet(
                "border: 2px solid #e74c3c; background-color: #fdf2f2;"
            )
            return
        
        self.input_sample_name.setStyleSheet("")  # 恢复正常样式
        print(f"\n开始测量样品: {sample_name}")
        self.statusBar.showMessage(f"正在测量: {sample_name}...", 5000)
    
    def get_all_settings(self) -> dict:
        """获取所有设置值"""
        return {
            "target_temp": self.spin_target_temp.value(),
            "temp_rate": self.spin_temp_rate.value(),
            "temp_stable": self.spin_temp_stable.value(),
            "field": self.spin_field.value(),
            "field_rate": self.spin_field_rate.value(),
            "field_mode": self.combo_field_mode.currentText(),
            "measure_type": self.combo_measure_type.currentText(),
            "points": self.spin_points.value(),
            "average": self.spin_average.value(),
            "auto_range": self.check_auto_range.isChecked(),
            "log_scale": self.check_log_scale.isChecked(),
            "sample_name": self.input_sample_name.text(),
            "note": self.input_note.text()
        }


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 9)  # 微软雅黑
    app.setFont(font)
    
    window = ExperimentParameterPanel()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

