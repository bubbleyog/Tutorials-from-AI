"""
示例程序：水平与垂直布局
所属章节：第二章 - 布局管理与界面设计

功能说明：
    演示QHBoxLayout和QVBoxLayout的使用，包括：
    - 基本的水平/垂直排列
    - addStretch()弹性空间
    - addSpacing()固定间距
    - 控件对齐方式

运行方式：
    python hbox_vbox_demo.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt


class HBoxVBoxDemo(QWidget):
    """水平与垂直布局演示"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("QHBoxLayout & QVBoxLayout 演示")
        self.setMinimumSize(600, 500)
        
        # 主布局（垂直）
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 添加演示组
        main_layout.addWidget(self.create_hbox_demo())
        main_layout.addWidget(self.create_vbox_demo())
        main_layout.addWidget(self.create_stretch_demo())
        main_layout.addWidget(self.create_alignment_demo())
        
        self.setLayout(main_layout)
        
        # 设置样式
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
                color: #2c3e50;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def create_hbox_demo(self) -> QGroupBox:
        """创建水平布局演示"""
        group = QGroupBox("QHBoxLayout - 水平布局")
        
        layout = QHBoxLayout()
        layout.setSpacing(10)  # 控件间距
        
        # 添加按钮
        for i in range(1, 5):
            btn = QPushButton(f"按钮 {i}")
            layout.addWidget(btn)
        
        group.setLayout(layout)
        return group
    
    def create_vbox_demo(self) -> QGroupBox:
        """创建垂直布局演示"""
        group = QGroupBox("QVBoxLayout - 垂直布局（内嵌在水平布局中展示）")
        
        # 外层水平布局，用于并排显示两个垂直布局
        outer_layout = QHBoxLayout()
        
        # 第一个垂直布局
        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel("垂直布局 1:"))
        for i in range(1, 4):
            vbox1.addWidget(QPushButton(f"选项 {i}"))
        
        # 第二个垂直布局
        vbox2 = QVBoxLayout()
        vbox2.addWidget(QLabel("垂直布局 2:"))
        for text in ["开始", "暂停", "停止"]:
            vbox2.addWidget(QPushButton(text))
        
        # 添加分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setStyleSheet("color: #bdc3c7;")
        
        outer_layout.addLayout(vbox1)
        outer_layout.addWidget(line)
        outer_layout.addLayout(vbox2)
        outer_layout.addStretch()  # 右侧弹性空间
        
        group.setLayout(outer_layout)
        return group
    
    def create_stretch_demo(self) -> QGroupBox:
        """创建弹性空间演示"""
        group = QGroupBox("addStretch() - 弹性空间演示")
        
        main_layout = QVBoxLayout()
        
        # 示例1：按钮靠右
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("靠右对齐:"))
        row1.addStretch(1)  # 左侧弹性空间
        row1.addWidget(QPushButton("确定"))
        row1.addWidget(QPushButton("取消"))
        main_layout.addLayout(row1)
        
        # 示例2：按钮居中
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("居中对齐:"))
        row2.addStretch(1)  # 左侧弹性空间
        row2.addWidget(QPushButton("居中按钮"))
        row2.addStretch(1)  # 右侧弹性空间
        main_layout.addLayout(row2)
        
        # 示例3：两端分布
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("两端分布:"))
        row3.addWidget(QPushButton("左侧"))
        row3.addStretch(1)  # 中间弹性空间
        row3.addWidget(QPushButton("右侧"))
        main_layout.addLayout(row3)
        
        # 示例4：比例分布 (1:2:1)
        row4 = QHBoxLayout()
        row4.addWidget(QLabel("1:2:1 比例:"))
        row4.addStretch(1)
        row4.addWidget(QPushButton("中间宽"))
        row4.addStretch(2)  # 权重为2，占更多空间
        row4.addWidget(QPushButton("右"))
        row4.addStretch(1)
        main_layout.addLayout(row4)
        
        group.setLayout(main_layout)
        return group
    
    def create_alignment_demo(self) -> QGroupBox:
        """创建对齐方式演示"""
        group = QGroupBox("控件对齐方式")
        
        layout = QHBoxLayout()
        
        # 顶部对齐
        btn1 = QPushButton("顶部对齐")
        btn1.setFixedHeight(60)
        layout.addWidget(btn1, alignment=Qt.AlignmentFlag.AlignTop)
        
        # 居中对齐（默认）
        btn2 = QPushButton("居中对齐")
        btn2.setFixedHeight(40)
        layout.addWidget(btn2, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        # 底部对齐
        btn3 = QPushButton("底部对齐")
        btn3.setFixedHeight(50)
        layout.addWidget(btn3, alignment=Qt.AlignmentFlag.AlignBottom)
        
        layout.addStretch()
        
        group.setLayout(layout)
        group.setFixedHeight(120)
        return group


class SpacingDemo(QWidget):
    """间距设置演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("间距设置演示")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        # setContentsMargins: 布局边距
        layout.setContentsMargins(30, 30, 30, 30)  # 左、上、右、下
        
        # setSpacing: 控件间距
        layout.setSpacing(20)
        
        layout.addWidget(QPushButton("按钮 1"))
        layout.addWidget(QPushButton("按钮 2"))
        
        # addSpacing: 添加固定间距
        layout.addSpacing(40)  # 40像素的额外间距
        
        layout.addWidget(QPushButton("按钮 3（上方有额外40px间距）"))
        
        layout.addStretch()
        
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 显示主演示窗口
    window = HBoxVBoxDemo()
    window.show()
    
    # 也可以取消注释查看间距演示
    # spacing_window = SpacingDemo()
    # spacing_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

