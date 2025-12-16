"""
示例程序：第一个PyQt窗口
所属章节：第一章 - PyQt基础入门

功能说明：
    演示PyQt窗口的创建方式，包括：
    1. 最简单的窗口创建
    2. 使用类封装的窗口
    3. 添加简单的控件和交互

运行方式：
    python first_window.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class FirstWindow(QWidget):
    """
    第一个PyQt窗口类
    
    演示了PyQt窗口的基本结构和组织方式
    """
    
    def __init__(self):
        """初始化窗口"""
        super().__init__()
        self.click_count = 0
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # ========== 窗口属性设置 ==========
        self.setWindowTitle("PyQt6 入门示例 - 第一个窗口")
        self.setGeometry(200, 200, 450, 300)
        
        # ========== 创建控件 ==========
        # 标题标签
        self.label_title = QLabel("欢迎学习 PyQt 编程！")
        title_font = QFont("Arial", 18, QFont.Weight.Bold)
        self.label_title.setFont(title_font)
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # 说明标签
        self.label_info = QLabel(
            "PyQt是一个功能强大的Python GUI框架，\n"
            "适用于开发科研数据处理和仪器控制软件。"
        )
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        
        # 计数标签
        self.label_count = QLabel("点击次数: 0")
        self.label_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_count.setStyleSheet(
            "font-size: 16px; color: #3498db; margin: 15px;"
        )
        
        # 按钮
        self.button = QPushButton("点击我")
        self.button.setFixedSize(120, 40)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }
        """)
        
        # 连接信号与槽
        self.button.clicked.connect(self.on_button_click)
        
        # ========== 布局设置 ==========
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_info)
        layout.addSpacing(20)
        layout.addWidget(self.label_count)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(2)
        
        self.setLayout(layout)
        
        # 设置窗口背景色
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def on_button_click(self):
        """
        按钮点击事件处理函数（槽函数）
        
        这个函数会在按钮被点击时自动调用
        """
        self.click_count += 1
        self.label_count.setText(f"点击次数: {self.click_count}")
        
        # 在控制台输出信息
        print(f"按钮被点击！当前点击次数: {self.click_count}")
        
        # 根据点击次数改变按钮颜色
        if self.click_count >= 10:
            self.button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #c0392b; }
            """)
            self.button.setText("太多了！")
        elif self.click_count >= 5:
            self.button.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #d68910; }
            """)
            self.button.setText("继续点击")


def simple_window_example():
    """
    最简单的窗口创建示例（不使用类）
    
    这种方式适合快速测试，不推荐用于实际项目
    """
    app = QApplication(sys.argv)
    
    # 创建窗口
    window = QWidget()
    window.setWindowTitle("最简单的PyQt窗口")
    window.setGeometry(100, 100, 300, 200)
    
    # 添加一个标签
    label = QLabel("Hello, PyQt!", window)
    label.setGeometry(80, 80, 150, 30)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    # 显示窗口
    window.show()
    
    # 进入事件循环
    sys.exit(app.exec())


def main():
    """主函数"""
    # 创建应用程序对象（每个PyQt程序必须有且仅有一个）
    app = QApplication(sys.argv)
    
    # 创建并显示窗口
    window = FirstWindow()
    window.show()
    
    # 进入事件循环
    # app.exec() 会阻塞程序，直到所有窗口关闭
    # sys.exit() 确保程序正确退出
    sys.exit(app.exec())


if __name__ == "__main__":
    # 运行主程序
    main()
    
    # 如果想测试简单窗口示例，注释上面的 main() 并取消下面的注释
    # simple_window_example()

