"""
示例程序：信号与槽基础
所属章节：第三章 - 信号与槽机制

功能说明：
    演示信号与槽的基本用法，包括：
    - 基本的信号连接
    - 一对多和多对一连接
    - 信号链（信号连接信号）
    - 断开连接

运行方式：
    python signal_slot_basic.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGroupBox
)
from PyQt6.QtCore import Qt


class SignalSlotBasic(QWidget):
    """信号与槽基础演示"""
    
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("信号与槽基础")
        self.setMinimumSize(500, 450)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 标题
        title = QLabel("信号与槽 (Signals & Slots) 演示")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 基本连接演示
        main_layout.addWidget(self.create_basic_demo())
        
        # 一对多演示
        main_layout.addWidget(self.create_one_to_many_demo())
        
        # 多对一演示
        main_layout.addWidget(self.create_many_to_one_demo())
        
        # 日志区域
        main_layout.addWidget(self.create_log_area())
        
        self.setLayout(main_layout)
        
        # 样式
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
            QPushButton {
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1c598a; }
        """)
    
    def create_basic_demo(self) -> QGroupBox:
        """基本信号连接演示"""
        group = QGroupBox("1. 基本连接：button.clicked.connect(slot)")
        layout = QHBoxLayout()
        
        self.btn_basic = QPushButton("点击我")
        # 基本连接：将clicked信号连接到槽函数
        self.btn_basic.clicked.connect(self.on_basic_click)
        
        self.label_count = QLabel("点击次数: 0")
        self.label_count.setStyleSheet("font-size: 14px;")
        
        layout.addWidget(self.btn_basic)
        layout.addWidget(self.label_count)
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_one_to_many_demo(self) -> QGroupBox:
        """一对多连接演示"""
        group = QGroupBox("2. 一对多：一个信号连接多个槽")
        layout = QHBoxLayout()
        
        self.btn_one_to_many = QPushButton("一个信号，三个响应")
        # 一个信号连接多个槽函数
        self.btn_one_to_many.clicked.connect(self.slot_1)
        self.btn_one_to_many.clicked.connect(self.slot_2)
        self.btn_one_to_many.clicked.connect(self.slot_3)
        
        self.labels_otm = []
        for i in range(3):
            label = QLabel(f"槽{i+1}: 等待")
            label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
            self.labels_otm.append(label)
            layout.addWidget(label)
        
        layout.insertWidget(0, self.btn_one_to_many)
        
        group.setLayout(layout)
        return group
    
    def create_many_to_one_demo(self) -> QGroupBox:
        """多对一连接演示"""
        group = QGroupBox("3. 多对一：多个信号连接同一个槽")
        layout = QHBoxLayout()
        
        self.label_mto = QLabel("点击任意按钮")
        self.label_mto.setStyleSheet(
            "font-size: 14px; padding: 10px; "
            "background-color: #ecf0f1; border-radius: 5px;"
        )
        
        # 创建多个按钮，连接到同一个槽
        for i in range(4):
            btn = QPushButton(f"按钮 {i+1}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {['#e74c3c', '#27ae60', '#3498db', '#f39c12'][i]};
                }}
            """)
            # 多个信号连接同一个槽（使用lambda传递按钮编号）
            btn.clicked.connect(lambda checked, idx=i+1: self.on_any_button_click(idx))
            layout.addWidget(btn)
        
        layout.addWidget(self.label_mto)
        
        group.setLayout(layout)
        return group
    
    def create_log_area(self) -> QGroupBox:
        """日志区域"""
        group = QGroupBox("事件日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2e;
                color: #00ff88;
                font-family: Consolas, monospace;
                border: none;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # 清除按钮
        btn_clear = QPushButton("清除日志")
        btn_clear.clicked.connect(self.log_text.clear)
        btn_clear.setStyleSheet("background-color: #95a5a6;")
        layout.addWidget(btn_clear, alignment=Qt.AlignmentFlag.AlignRight)
        
        group.setLayout(layout)
        return group
    
    # ========== 槽函数 ==========
    
    def on_basic_click(self):
        """基本点击槽函数"""
        self.click_count += 1
        self.label_count.setText(f"点击次数: {self.click_count}")
        self.log(f"基本按钮被点击，计数: {self.click_count}")
    
    def slot_1(self):
        """槽函数1"""
        self.labels_otm[0].setText("槽1: ✓ 触发")
        self.labels_otm[0].setStyleSheet(
            "padding: 5px; background-color: #d5f5e3; border-radius: 3px;"
        )
        self.log("槽函数 1 被调用")
    
    def slot_2(self):
        """槽函数2"""
        self.labels_otm[1].setText("槽2: ✓ 触发")
        self.labels_otm[1].setStyleSheet(
            "padding: 5px; background-color: #d6eaf8; border-radius: 3px;"
        )
        self.log("槽函数 2 被调用")
    
    def slot_3(self):
        """槽函数3"""
        self.labels_otm[2].setText("槽3: ✓ 触发")
        self.labels_otm[2].setStyleSheet(
            "padding: 5px; background-color: #fdebd0; border-radius: 3px;"
        )
        self.log("槽函数 3 被调用")
    
    def on_any_button_click(self, button_id: int):
        """多对一：任意按钮点击"""
        colors = ['红', '绿', '蓝', '橙']
        self.label_mto.setText(f"你点击了: {colors[button_id-1]}色按钮 (#{button_id})")
        self.log(f"按钮 {button_id} ({colors[button_id-1]}色) 被点击")
    
    def log(self, message: str):
        """添加日志"""
        self.log_text.append(f"[{self.get_time()}] {message}")
    
    def get_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")


class DisconnectDemo(QWidget):
    """断开连接演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_connected = True
    
    def init_ui(self):
        self.setWindowTitle("断开信号连接演示")
        self.setMinimumSize(400, 200)
        
        layout = QVBoxLayout()
        
        # 说明
        info = QLabel(
            "演示 disconnect() 断开信号连接\n"
            "点击'切换连接'可以连接/断开信号"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        # 测试按钮
        self.btn_test = QPushButton("测试按钮（点击查看效果）")
        self.btn_test.clicked.connect(self.on_test_click)
        layout.addWidget(self.btn_test)
        
        # 切换按钮
        self.btn_toggle = QPushButton("断开连接")
        self.btn_toggle.clicked.connect(self.toggle_connection)
        self.btn_toggle.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.btn_toggle)
        
        # 状态标签
        self.label_status = QLabel("状态: 已连接")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        layout.addWidget(self.label_status)
        
        self.setLayout(layout)
    
    def on_test_click(self):
        """测试按钮点击"""
        print("测试按钮被点击！信号槽正在工作。")
        self.label_status.setText("状态: 已连接 - 信号已触发！")
    
    def toggle_connection(self):
        """切换连接状态"""
        if self.is_connected:
            # 断开连接
            self.btn_test.clicked.disconnect(self.on_test_click)
            self.is_connected = False
            self.btn_toggle.setText("重新连接")
            self.btn_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
            """)
            self.label_status.setText("状态: 已断开")
            self.label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
            print("信号已断开")
        else:
            # 重新连接
            self.btn_test.clicked.connect(self.on_test_click)
            self.is_connected = True
            self.btn_toggle.setText("断开连接")
            self.btn_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
            """)
            self.label_status.setText("状态: 已连接")
            self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
            print("信号已重新连接")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 基础演示
    window = SignalSlotBasic()
    window.show()
    
    # 断开连接演示
    disconnect_demo = DisconnectDemo()
    disconnect_demo.move(550, 100)
    disconnect_demo.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

