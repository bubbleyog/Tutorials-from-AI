"""
示例程序：分组框与标签页
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示QGroupBox、QTabWidget、QSplitter的使用，包括：
    - 分组框的基本使用和可折叠分组框
    - 标签页控件的各种配置
    - 可拖动分割器

运行方式：
    python groupbox_tabs.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QRadioButton, QButtonGroup, QTextEdit, QListWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QGroupBox, QTabWidget, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class GroupBoxDemo(QWidget):
    """分组框演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QGroupBox 分组框演示")
        self.setMinimumSize(500, 400)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(15)
        
        # 左侧：基本分组框
        main_layout.addWidget(self.create_basic_group())
        
        # 右侧：可折叠分组框
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.create_checkable_group())
        right_layout.addWidget(self.create_radio_group())
        main_layout.addLayout(right_layout)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2c3e50;
            }
            QGroupBox::indicator {
                width: 16px;
                height: 16px;
            }
            QGroupBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QGroupBox::indicator:checked {
                border: 2px solid #27ae60;
                border-radius: 3px;
                background-color: #27ae60;
            }
        """)
    
    def create_basic_group(self) -> QGroupBox:
        """创建基本分组框"""
        group = QGroupBox("基本信息")
        
        layout = QFormLayout()
        layout.setSpacing(10)
        
        layout.addRow("姓名:", QLineEdit())
        layout.addRow("年龄:", QSpinBox())
        layout.addRow("部门:", QComboBox())
        
        group.setLayout(layout)
        return group
    
    def create_checkable_group(self) -> QGroupBox:
        """创建可折叠分组框"""
        group = QGroupBox("高级选项")
        group.setCheckable(True)
        group.setChecked(False)  # 默认折叠
        
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("启用日志"))
        layout.addWidget(QCheckBox("自动保存"))
        layout.addWidget(QCheckBox("显示调试信息"))
        
        group.setLayout(layout)
        return group
    
    def create_radio_group(self) -> QGroupBox:
        """创建单选按钮分组框"""
        group = QGroupBox("输出格式")
        
        layout = QVBoxLayout()
        
        # 创建单选按钮组
        self.format_group = QButtonGroup(self)
        
        radio_csv = QRadioButton("CSV 格式")
        radio_csv.setChecked(True)
        radio_json = QRadioButton("JSON 格式")
        radio_excel = QRadioButton("Excel 格式")
        
        self.format_group.addButton(radio_csv, 1)
        self.format_group.addButton(radio_json, 2)
        self.format_group.addButton(radio_excel, 3)
        
        layout.addWidget(radio_csv)
        layout.addWidget(radio_json)
        layout.addWidget(radio_excel)
        
        group.setLayout(layout)
        return group


class TabWidgetDemo(QWidget):
    """标签页演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QTabWidget 标签页演示")
        self.setMinimumSize(600, 450)
        
        main_layout = QVBoxLayout()
        
        # 标签页控件
        self.tabs = QTabWidget()
        
        # 添加各个页面
        self.tabs.addTab(self.create_connection_page(), "🔌 连接")
        self.tabs.addTab(self.create_acquisition_page(), "📊 采集")
        self.tabs.addTab(self.create_display_page(), "🖥 显示")
        self.tabs.addTab(self.create_export_page(), "💾 导出")
        
        main_layout.addWidget(self.tabs)
        
        # 标签页控制按钮
        ctrl_layout = QHBoxLayout()
        
        btn_prev = QPushButton("◀ 上一页")
        btn_prev.clicked.connect(self.prev_tab)
        ctrl_layout.addWidget(btn_prev)
        
        btn_next = QPushButton("下一页 ▶")
        btn_next.clicked.connect(self.next_tab)
        ctrl_layout.addWidget(btn_next)
        
        ctrl_layout.addStretch()
        
        # 标签位置选择
        ctrl_layout.addWidget(QLabel("标签位置:"))
        self.combo_position = QComboBox()
        self.combo_position.addItems(["上方", "下方", "左侧", "右侧"])
        self.combo_position.currentIndexChanged.connect(self.change_tab_position)
        ctrl_layout.addWidget(self.combo_position)
        
        main_layout.addLayout(ctrl_layout)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
            QGroupBox {
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
    
    def create_connection_page(self) -> QWidget:
        """创建连接设置页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 串口设置组
        serial_group = QGroupBox("串口设置")
        serial_form = QFormLayout()
        
        combo_port = QComboBox()
        combo_port.addItems(["COM1", "COM2", "COM3", "COM4"])
        serial_form.addRow("端口:", combo_port)
        
        combo_baud = QComboBox()
        combo_baud.addItems(["9600", "19200", "38400", "57600", "115200"])
        combo_baud.setCurrentText("115200")
        serial_form.addRow("波特率:", combo_baud)
        
        combo_parity = QComboBox()
        combo_parity.addItems(["None", "Odd", "Even"])
        serial_form.addRow("校验:", combo_parity)
        
        serial_group.setLayout(serial_form)
        layout.addWidget(serial_group)
        
        # TCP/IP设置组
        tcp_group = QGroupBox("TCP/IP 设置")
        tcp_form = QFormLayout()
        
        tcp_form.addRow("IP地址:", QLineEdit("192.168.1.100"))
        tcp_form.addRow("端口:", QSpinBox())
        
        tcp_group.setLayout(tcp_form)
        layout.addWidget(tcp_group)
        
        layout.addStretch()
        
        # 连接按钮
        btn_connect = QPushButton("连接设备")
        btn_connect.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #219a52; }
        """)
        layout.addWidget(btn_connect)
        
        return page
    
    def create_acquisition_page(self) -> QWidget:
        """创建采集设置页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(15)
        
        spin_rate = QSpinBox()
        spin_rate.setRange(1, 1000000)
        spin_rate.setValue(10000)
        spin_rate.setSuffix(" Hz")
        layout.addRow("采样率:", spin_rate)
        
        spin_samples = QSpinBox()
        spin_samples.setRange(100, 10000000)
        spin_samples.setValue(100000)
        layout.addRow("采样点数:", spin_samples)
        
        combo_channels = QComboBox()
        combo_channels.addItems(["1 通道", "2 通道", "4 通道", "8 通道"])
        layout.addRow("通道数:", combo_channels)
        
        combo_trigger = QComboBox()
        combo_trigger.addItems(["立即触发", "外部触发", "软件触发"])
        layout.addRow("触发模式:", combo_trigger)
        
        spin_trigger_level = QDoubleSpinBox()
        spin_trigger_level.setRange(-10, 10)
        spin_trigger_level.setValue(0)
        spin_trigger_level.setSuffix(" V")
        layout.addRow("触发电平:", spin_trigger_level)
        
        return page
    
    def create_display_page(self) -> QWidget:
        """创建显示设置页"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # 显示选项
        display_group = QGroupBox("显示选项")
        display_layout = QVBoxLayout()
        
        display_layout.addWidget(QCheckBox("显示网格"))
        display_layout.addWidget(QCheckBox("显示刻度"))
        display_layout.addWidget(QCheckBox("自动缩放"))
        display_layout.addWidget(QCheckBox("显示统计信息"))
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # 颜色设置
        color_group = QGroupBox("通道颜色")
        color_form = QFormLayout()
        
        for i, color in enumerate(["#e74c3c", "#27ae60", "#3498db", "#f39c12"]):
            btn = QPushButton()
            btn.setFixedSize(60, 25)
            btn.setStyleSheet(f"background-color: {color}; border: none; border-radius: 3px;")
            color_form.addRow(f"通道 {i+1}:", btn)
        
        color_group.setLayout(color_form)
        layout.addWidget(color_group)
        
        layout.addStretch()
        
        return page
    
    def create_export_page(self) -> QWidget:
        """创建导出设置页"""
        page = QWidget()
        layout = QFormLayout(page)
        layout.setSpacing(15)
        
        # 文件路径
        path_layout = QHBoxLayout()
        path_input = QLineEdit("./data/output.csv")
        path_layout.addWidget(path_input)
        btn_browse = QPushButton("浏览...")
        path_layout.addWidget(btn_browse)
        layout.addRow("保存路径:", path_layout)
        
        # 格式选择
        combo_format = QComboBox()
        combo_format.addItems(["CSV", "Excel", "JSON", "MATLAB (.mat)"])
        layout.addRow("文件格式:", combo_format)
        
        # 选项
        layout.addRow("", QCheckBox("包含时间戳"))
        layout.addRow("", QCheckBox("包含标题行"))
        layout.addRow("", QCheckBox("压缩文件"))
        
        return page
    
    def prev_tab(self):
        """切换到上一个标签页"""
        current = self.tabs.currentIndex()
        if current > 0:
            self.tabs.setCurrentIndex(current - 1)
    
    def next_tab(self):
        """切换到下一个标签页"""
        current = self.tabs.currentIndex()
        if current < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current + 1)
    
    def change_tab_position(self, index: int):
        """改变标签位置"""
        positions = [
            QTabWidget.TabPosition.North,
            QTabWidget.TabPosition.South,
            QTabWidget.TabPosition.West,
            QTabWidget.TabPosition.East
        ]
        self.tabs.setTabPosition(positions[index])


class SplitterDemo(QWidget):
    """分割器演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QSplitter 可拖动分割器演示")
        self.setMinimumSize(700, 500)
        
        main_layout = QVBoxLayout()
        
        # 说明
        info = QLabel("拖动分割线可以调整各区域大小")
        info.setStyleSheet("color: #7f8c8d; padding: 5px;")
        main_layout.addWidget(info)
        
        # 水平分割器
        h_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧面板
        left_panel = QGroupBox("导航")
        left_layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.addItems(["项目 1", "项目 2", "项目 3", "项目 4", "项目 5"])
        left_layout.addWidget(list_widget)
        left_panel.setLayout(left_layout)
        h_splitter.addWidget(left_panel)
        
        # 垂直分割器（嵌套在水平分割器中）
        v_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 上部主内容区
        main_panel = QGroupBox("主内容区")
        main_panel_layout = QVBoxLayout()
        main_text = QTextEdit()
        main_text.setPlaceholderText("在这里编辑内容...")
        main_panel_layout.addWidget(main_text)
        main_panel.setLayout(main_panel_layout)
        v_splitter.addWidget(main_panel)
        
        # 下部输出区
        output_panel = QGroupBox("输出 / 日志")
        output_layout = QVBoxLayout()
        output_text = QTextEdit()
        output_text.setReadOnly(True)
        output_text.setStyleSheet("background-color: #1a1a2e; color: #00ff88;")
        output_text.setText("[INFO] 程序启动\n[INFO] 加载配置完成\n[INFO] 等待用户操作...")
        output_layout.addWidget(output_text)
        output_panel.setLayout(output_layout)
        v_splitter.addWidget(output_panel)
        
        # 设置垂直分割比例
        v_splitter.setSizes([300, 150])
        
        h_splitter.addWidget(v_splitter)
        
        # 右侧属性面板
        right_panel = QGroupBox("属性")
        right_layout = QFormLayout()
        right_layout.addRow("名称:", QLineEdit())
        right_layout.addRow("大小:", QSpinBox())
        right_layout.addRow("类型:", QComboBox())
        right_panel.setLayout(right_layout)
        h_splitter.addWidget(right_panel)
        
        # 设置水平分割比例
        h_splitter.setSizes([150, 400, 150])
        
        # 设置最小宽度
        left_panel.setMinimumWidth(100)
        right_panel.setMinimumWidth(100)
        
        main_layout.addWidget(h_splitter)
        
        self.setLayout(main_layout)
        
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QSplitter::handle {
                background-color: #bdc3c7;
            }
            QSplitter::handle:horizontal {
                width: 5px;
            }
            QSplitter::handle:vertical {
                height: 5px;
            }
            QSplitter::handle:hover {
                background-color: #3498db;
            }
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 分组框演示
    group_demo = GroupBoxDemo()
    group_demo.show()
    
    # 标签页演示
    tab_demo = TabWidgetDemo()
    tab_demo.move(550, 100)
    tab_demo.show()
    
    # 分割器演示
    splitter_demo = SplitterDemo()
    splitter_demo.move(100, 500)
    splitter_demo.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

