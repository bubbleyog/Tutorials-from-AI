"""
示例程序：进度条与状态反馈
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示各种进度反馈方式：
    - QProgressBar基本用法
    - 不确定进度（忙碌指示）
    - QProgressDialog模态对话框
    - 状态栏更新
    - 多任务进度

运行方式：
    python progress_bar.py
"""

import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QProgressDialog,
    QGroupBox, QFormLayout, QSpinBox, QStatusBar, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer


class SimulatedTask(QThread):
    """模拟任务线程"""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, duration: int = 5):
        super().__init__()
        self.duration = duration
        self._is_cancelled = False
    
    def run(self):
        steps = self.duration * 10  # 每秒10步
        for i in range(steps):
            if self._is_cancelled:
                self.status.emit("已取消")
                return
            
            progress = int((i + 1) / steps * 100)
            self.progress.emit(progress)
            self.status.emit(f"处理中... {progress}%")
            time.sleep(0.1)
        
        self.status.emit("完成!")
        self.finished.emit()
    
    def cancel(self):
        self._is_cancelled = True


class MultiTaskWorker(QThread):
    """多任务工作线程"""
    
    task_progress = pyqtSignal(int, int)  # 任务索引, 进度
    task_status = pyqtSignal(int, str)    # 任务索引, 状态
    overall_progress = pyqtSignal(int)
    finished = pyqtSignal()
    
    def __init__(self, n_tasks: int):
        super().__init__()
        self.n_tasks = n_tasks
    
    def run(self):
        for task_idx in range(self.n_tasks):
            self.task_status.emit(task_idx, "进行中")
            
            # 模拟任务执行
            for i in range(100):
                self.task_progress.emit(task_idx, i + 1)
                overall = int((task_idx * 100 + i + 1) / (self.n_tasks * 100) * 100)
                self.overall_progress.emit(overall)
                time.sleep(0.02)
            
            self.task_status.emit(task_idx, "完成")
        
        self.finished.emit()


class ProgressBarDemo(QMainWindow):
    """进度条演示"""
    
    def __init__(self):
        super().__init__()
        self.task = None
        self.multi_task = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("进度条与状态反馈")
        self.setMinimumSize(700, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        
        # 基本进度条
        main_layout.addWidget(self.create_basic_progress())
        
        # 不确定进度
        main_layout.addWidget(self.create_indeterminate_progress())
        
        # 进度对话框
        main_layout.addWidget(self.create_dialog_progress())
        
        # 多任务进度
        main_layout.addWidget(self.create_multi_task_progress())
        
        # 自定义样式进度条
        main_layout.addWidget(self.create_styled_progress())
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 状态栏永久控件
        self.status_label = QLabel("● 空闲")
        self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.statusBar.addPermanentWidget(self.status_label)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #d35400;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #d35400; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)
    
    def create_basic_progress(self) -> QGroupBox:
        """基本进度条"""
        group = QGroupBox("基本进度条")
        layout = QVBoxLayout()
        
        # 进度条
        self.progress_basic = QProgressBar()
        self.progress_basic.setRange(0, 100)
        self.progress_basic.setValue(0)
        self.progress_basic.setFormat("%v% 完成")
        layout.addWidget(self.progress_basic)
        
        # 状态标签
        self.label_basic = QLabel("点击开始按钮启动任务")
        layout.addWidget(self.label_basic)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.btn_start_basic = QPushButton("▶ 开始")
        self.btn_start_basic.clicked.connect(self.start_basic_task)
        btn_layout.addWidget(self.btn_start_basic)
        
        self.btn_cancel_basic = QPushButton("✖ 取消")
        self.btn_cancel_basic.setEnabled(False)
        self.btn_cancel_basic.clicked.connect(self.cancel_basic_task)
        btn_layout.addWidget(self.btn_cancel_basic)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def create_indeterminate_progress(self) -> QGroupBox:
        """不确定进度（忙碌指示）"""
        group = QGroupBox("不确定进度（忙碌指示）")
        layout = QVBoxLayout()
        
        info = QLabel("当无法确定任务进度时，使用不确定模式")
        info.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(info)
        
        self.progress_indeterminate = QProgressBar()
        self.progress_indeterminate.setRange(0, 100)
        layout.addWidget(self.progress_indeterminate)
        
        btn_layout = QHBoxLayout()
        
        btn_start_busy = QPushButton("显示忙碌状态")
        btn_start_busy.clicked.connect(self.toggle_busy)
        btn_layout.addWidget(btn_start_busy)
        
        btn_stop_busy = QPushButton("停止")
        btn_stop_busy.clicked.connect(lambda: self.progress_indeterminate.setRange(0, 100))
        btn_layout.addWidget(btn_stop_busy)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def create_dialog_progress(self) -> QGroupBox:
        """进度对话框"""
        group = QGroupBox("QProgressDialog 模态对话框")
        layout = QVBoxLayout()
        
        info = QLabel("模态进度对话框会阻止用户与主窗口交互")
        info.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(info)
        
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("持续时间:"))
        self.spin_dialog_duration = QSpinBox()
        self.spin_dialog_duration.setRange(1, 10)
        self.spin_dialog_duration.setValue(3)
        self.spin_dialog_duration.setSuffix(" 秒")
        param_layout.addWidget(self.spin_dialog_duration)
        param_layout.addStretch()
        layout.addLayout(param_layout)
        
        btn = QPushButton("显示进度对话框")
        btn.clicked.connect(self.show_progress_dialog)
        layout.addWidget(btn)
        
        group.setLayout(layout)
        return group
    
    def create_multi_task_progress(self) -> QGroupBox:
        """多任务进度"""
        group = QGroupBox("多任务进度")
        layout = QVBoxLayout()
        
        # 任务进度条
        self.task_progress_bars = []
        self.task_labels = []
        
        for i in range(3):
            row = QHBoxLayout()
            
            label = QLabel(f"任务 {i+1}:")
            label.setFixedWidth(60)
            row.addWidget(label)
            
            progress = QProgressBar()
            progress.setRange(0, 100)
            self.task_progress_bars.append(progress)
            row.addWidget(progress)
            
            status = QLabel("等待")
            status.setFixedWidth(60)
            self.task_labels.append(status)
            row.addWidget(status)
            
            layout.addLayout(row)
        
        # 总进度
        layout.addWidget(QLabel("总体进度:"))
        self.progress_overall = QProgressBar()
        self.progress_overall.setRange(0, 100)
        self.progress_overall.setStyleSheet("""
            QProgressBar {
                border: 2px solid #27ae60;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(self.progress_overall)
        
        self.btn_start_multi = QPushButton("▶ 开始多任务")
        self.btn_start_multi.clicked.connect(self.start_multi_task)
        layout.addWidget(self.btn_start_multi)
        
        group.setLayout(layout)
        return group
    
    def create_styled_progress(self) -> QGroupBox:
        """自定义样式进度条"""
        group = QGroupBox("自定义样式")
        layout = QVBoxLayout()
        
        # 蓝色进度条
        progress1 = QProgressBar()
        progress1.setRange(0, 100)
        progress1.setValue(75)
        progress1.setFormat("下载进度: %v%")
        progress1.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                background-color: #ecf0f1;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9
                );
                border-radius: 3px;
            }
        """)
        layout.addWidget(QLabel("渐变蓝色:"))
        layout.addWidget(progress1)
        
        # 绿色条纹进度条
        progress2 = QProgressBar()
        progress2.setRange(0, 100)
        progress2.setValue(60)
        progress2.setFormat("上传: %v%")
        progress2.setStyleSheet("""
            QProgressBar {
                border: 2px solid #27ae60;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(QLabel("绿色:"))
        layout.addWidget(progress2)
        
        # 红色警告进度条
        progress3 = QProgressBar()
        progress3.setRange(0, 100)
        progress3.setValue(90)
        progress3.setFormat("磁盘使用: %v%")
        progress3.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e74c3c;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
            }
        """)
        layout.addWidget(QLabel("红色警告:"))
        layout.addWidget(progress3)
        
        group.setLayout(layout)
        return group
    
    # ========== 事件处理 ==========
    
    def start_basic_task(self):
        """开始基本任务"""
        self.task = SimulatedTask(5)
        self.task.progress.connect(self.progress_basic.setValue)
        self.task.status.connect(self.label_basic.setText)
        self.task.finished.connect(self.on_basic_task_finished)
        
        self.btn_start_basic.setEnabled(False)
        self.btn_cancel_basic.setEnabled(True)
        self.status_label.setText("● 运行中")
        self.status_label.setStyleSheet("color: #e67e22; font-weight: bold;")
        self.statusBar.showMessage("正在执行任务...")
        
        self.task.start()
    
    def cancel_basic_task(self):
        """取消基本任务"""
        if self.task:
            self.task.cancel()
    
    def on_basic_task_finished(self):
        """基本任务完成"""
        self.btn_start_basic.setEnabled(True)
        self.btn_cancel_basic.setEnabled(False)
        self.status_label.setText("● 空闲")
        self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        self.statusBar.showMessage("任务完成", 3000)
        self.task = None
    
    def toggle_busy(self):
        """切换忙碌状态"""
        # 设置范围为(0, 0)开启不确定模式
        self.progress_indeterminate.setRange(0, 0)
    
    def show_progress_dialog(self):
        """显示进度对话框"""
        duration = self.spin_dialog_duration.value()
        steps = duration * 10
        
        dialog = QProgressDialog("正在处理...", "取消", 0, steps, self)
        dialog.setWindowTitle("进度")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(0)
        dialog.show()
        
        for i in range(steps):
            if dialog.wasCanceled():
                self.statusBar.showMessage("操作已取消", 3000)
                return
            
            dialog.setValue(i + 1)
            dialog.setLabelText(f"正在处理... ({i+1}/{steps})")
            QApplication.processEvents()
            time.sleep(0.1)
        
        dialog.close()
        self.statusBar.showMessage("操作完成", 3000)
    
    def start_multi_task(self):
        """开始多任务"""
        # 重置进度
        for pb in self.task_progress_bars:
            pb.setValue(0)
        for label in self.task_labels:
            label.setText("等待")
        self.progress_overall.setValue(0)
        
        self.multi_task = MultiTaskWorker(3)
        self.multi_task.task_progress.connect(self.on_task_progress)
        self.multi_task.task_status.connect(self.on_task_status)
        self.multi_task.overall_progress.connect(self.progress_overall.setValue)
        self.multi_task.finished.connect(self.on_multi_task_finished)
        
        self.btn_start_multi.setEnabled(False)
        self.multi_task.start()
    
    def on_task_progress(self, idx: int, progress: int):
        """任务进度更新"""
        if idx < len(self.task_progress_bars):
            self.task_progress_bars[idx].setValue(progress)
    
    def on_task_status(self, idx: int, status: str):
        """任务状态更新"""
        if idx < len(self.task_labels):
            self.task_labels[idx].setText(status)
    
    def on_multi_task_finished(self):
        """多任务完成"""
        self.btn_start_multi.setEnabled(True)
        self.statusBar.showMessage("所有任务完成", 3000)


def main():
    app = QApplication(sys.argv)
    window = ProgressBarDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

