"""
示例程序：Qt Designer使用示例
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示两种使用Qt Designer设计的UI文件的方法：
    1. 使用uic动态加载.ui文件
    2. 使用转换后的Python代码

    由于.ui文件需要Qt Designer创建，本示例提供了
    一个纯代码实现的等效界面作为参考。

运行方式：
    python main.py
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QStatusBar
)
from PyQt6.QtCore import Qt

# 尝试导入uic模块用于加载.ui文件
try:
    from PyQt6 import uic
    HAS_UIC = True
except ImportError:
    HAS_UIC = False


class ExperimentWindow(QMainWindow):
    """
    实验参数设置窗口
    
    这是一个用纯Python代码实现的界面，
    展示了如果使用Qt Designer设计会是什么样子。
    
    在实际使用中，你可以用Qt Designer拖放控件来创建这个界面，
    然后保存为.ui文件，再用uic.loadUi()加载。
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面（模拟Qt Designer生成的布局）"""
        self.setWindowTitle("实验控制面板 - Qt Designer 风格")
        self.setMinimumSize(400, 450)
        
        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        
        # 主布局
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ===== 样品信息组 =====
        sample_group = QGroupBox("样品信息")
        sample_group.setObjectName("sampleGroup")  # 设置对象名（Qt Designer会自动生成）
        
        sample_layout = QFormLayout()
        
        self.lineEdit_sampleName = QLineEdit()
        self.lineEdit_sampleName.setObjectName("lineEdit_sampleName")
        self.lineEdit_sampleName.setPlaceholderText("请输入样品名称")
        sample_layout.addRow("样品名称:", self.lineEdit_sampleName)
        
        self.lineEdit_sampleId = QLineEdit()
        self.lineEdit_sampleId.setObjectName("lineEdit_sampleId")
        sample_layout.addRow("样品编号:", self.lineEdit_sampleId)
        
        self.comboBox_sampleType = QComboBox()
        self.comboBox_sampleType.setObjectName("comboBox_sampleType")
        self.comboBox_sampleType.addItems(["粉末", "单晶", "薄膜", "块体"])
        sample_layout.addRow("样品类型:", self.comboBox_sampleType)
        
        sample_group.setLayout(sample_layout)
        main_layout.addWidget(sample_group)
        
        # ===== 测量参数组 =====
        measure_group = QGroupBox("测量参数")
        measure_group.setObjectName("measureGroup")
        
        measure_layout = QFormLayout()
        
        self.doubleSpinBox_tempStart = QDoubleSpinBox()
        self.doubleSpinBox_tempStart.setObjectName("doubleSpinBox_tempStart")
        self.doubleSpinBox_tempStart.setRange(1.5, 400)
        self.doubleSpinBox_tempStart.setValue(2.0)
        self.doubleSpinBox_tempStart.setSuffix(" K")
        measure_layout.addRow("起始温度:", self.doubleSpinBox_tempStart)
        
        self.doubleSpinBox_tempEnd = QDoubleSpinBox()
        self.doubleSpinBox_tempEnd.setObjectName("doubleSpinBox_tempEnd")
        self.doubleSpinBox_tempEnd.setRange(1.5, 400)
        self.doubleSpinBox_tempEnd.setValue(300.0)
        self.doubleSpinBox_tempEnd.setSuffix(" K")
        measure_layout.addRow("终止温度:", self.doubleSpinBox_tempEnd)
        
        self.spinBox_points = QSpinBox()
        self.spinBox_points.setObjectName("spinBox_points")
        self.spinBox_points.setRange(10, 1000)
        self.spinBox_points.setValue(100)
        measure_layout.addRow("测量点数:", self.spinBox_points)
        
        self.comboBox_mode = QComboBox()
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItems(["ZFC", "FC", "ZFC-FC"])
        measure_layout.addRow("测量模式:", self.comboBox_mode)
        
        measure_group.setLayout(measure_layout)
        main_layout.addWidget(measure_group)
        
        # ===== 选项组 =====
        option_group = QGroupBox("选项")
        option_group.setObjectName("optionGroup")
        
        option_layout = QVBoxLayout()
        
        self.checkBox_autoSave = QCheckBox("自动保存数据")
        self.checkBox_autoSave.setObjectName("checkBox_autoSave")
        self.checkBox_autoSave.setChecked(True)
        option_layout.addWidget(self.checkBox_autoSave)
        
        self.checkBox_showPlot = QCheckBox("实时显示曲线")
        self.checkBox_showPlot.setObjectName("checkBox_showPlot")
        self.checkBox_showPlot.setChecked(True)
        option_layout.addWidget(self.checkBox_showPlot)
        
        self.checkBox_sendEmail = QCheckBox("完成后发送邮件通知")
        self.checkBox_sendEmail.setObjectName("checkBox_sendEmail")
        option_layout.addWidget(self.checkBox_sendEmail)
        
        option_group.setLayout(option_layout)
        main_layout.addWidget(option_group)
        
        # ===== 按钮 =====
        button_layout = QHBoxLayout()
        
        self.pushButton_start = QPushButton("开始测量")
        self.pushButton_start.setObjectName("pushButton_start")
        self.pushButton_start.setStyleSheet("""
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
        
        self.pushButton_stop = QPushButton("停止")
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_stop.setEnabled(False)
        self.pushButton_stop.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 25px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c0392b; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)
        
        self.pushButton_reset = QPushButton("重置")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.pushButton_reset.setStyleSheet("""
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
        
        button_layout.addWidget(self.pushButton_start)
        button_layout.addWidget(self.pushButton_stop)
        button_layout.addStretch()
        button_layout.addWidget(self.pushButton_reset)
        
        main_layout.addLayout(button_layout)
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 窗口样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
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
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def connect_signals(self):
        """连接信号与槽（在Qt Designer中可以通过信号/槽编辑器完成）"""
        self.pushButton_start.clicked.connect(self.on_start)
        self.pushButton_stop.clicked.connect(self.on_stop)
        self.pushButton_reset.clicked.connect(self.on_reset)
    
    def on_start(self):
        """开始测量"""
        sample_name = self.lineEdit_sampleName.text()
        if not sample_name:
            self.statusBar.showMessage("错误：请输入样品名称", 3000)
            return
        
        self.pushButton_start.setEnabled(False)
        self.pushButton_stop.setEnabled(True)
        self.statusBar.showMessage(f"正在测量: {sample_name}...")
        
        # 打印参数
        print(f"\n开始测量:")
        print(f"  样品: {sample_name}")
        print(f"  编号: {self.lineEdit_sampleId.text()}")
        print(f"  类型: {self.comboBox_sampleType.currentText()}")
        print(f"  温度范围: {self.doubleSpinBox_tempStart.value()} - "
              f"{self.doubleSpinBox_tempEnd.value()} K")
        print(f"  测量点数: {self.spinBox_points.value()}")
        print(f"  模式: {self.comboBox_mode.currentText()}")
    
    def on_stop(self):
        """停止测量"""
        self.pushButton_start.setEnabled(True)
        self.pushButton_stop.setEnabled(False)
        self.statusBar.showMessage("测量已停止")
        print("测量已停止")
    
    def on_reset(self):
        """重置所有参数"""
        self.lineEdit_sampleName.clear()
        self.lineEdit_sampleId.clear()
        self.comboBox_sampleType.setCurrentIndex(0)
        self.doubleSpinBox_tempStart.setValue(2.0)
        self.doubleSpinBox_tempEnd.setValue(300.0)
        self.spinBox_points.setValue(100)
        self.comboBox_mode.setCurrentIndex(0)
        self.checkBox_autoSave.setChecked(True)
        self.checkBox_showPlot.setChecked(True)
        self.checkBox_sendEmail.setChecked(False)
        self.statusBar.showMessage("参数已重置")


class UiLoaderExample(QWidget):
    """
    演示如何使用uic.loadUi()加载.ui文件
    
    注意：这需要一个实际的.ui文件存在
    """
    
    def __init__(self, ui_file: str):
        super().__init__()
        
        if os.path.exists(ui_file) and HAS_UIC:
            # 加载.ui文件
            uic.loadUi(ui_file, self)
            
            # 现在可以通过objectName访问控件
            # 例如：self.pushButton_start.clicked.connect(self.on_start)
            print(f"成功加载UI文件: {ui_file}")
        else:
            # 如果没有.ui文件，显示提示信息
            layout = QVBoxLayout()
            
            label = QLabel(
                "Qt Designer UI 文件加载示例\n\n"
                "要使用此功能，请：\n"
                "1. 使用 Qt Designer 创建 .ui 文件\n"
                "2. 保存到本目录\n"
                "3. 修改代码中的文件路径\n\n"
                f"当前查找的文件: {ui_file}\n"
                f"uic模块可用: {HAS_UIC}"
            )
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 14px; color: #2c3e50;")
            
            layout.addWidget(label)
            self.setLayout(layout)
            self.setWindowTitle("UI文件加载示例")
            self.setMinimumSize(400, 300)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 显示纯代码实现的窗口（模拟Qt Designer效果）
    window = ExperimentWindow()
    window.show()
    
    # 尝试加载.ui文件（如果存在）
    # ui_loader = UiLoaderExample("experiment_ui.ui")
    # ui_loader.show()
    
    print("\n" + "=" * 50)
    print("Qt Designer 使用说明")
    print("=" * 50)
    print("1. 安装: pip install pyqt6-tools")
    print("2. 启动: pyqt6-tools designer")
    print("3. 设计界面并保存为 .ui 文件")
    print("4. 加载: uic.loadUi('file.ui', self)")
    print("5. 或转换: pyuic6 -x file.ui -o ui_file.py")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

