"""
示例程序：多线程防止界面冻结
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示QThread的使用：
    - 将耗时任务放到工作线程
    - 使用信号更新进度
    - 防止界面冻结

运行方式：
    python threading_demo.py
"""

import sys
import time
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QGroupBox,
    QSpinBox, QFormLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject


# ============================================================
# 工作线程类
# ============================================================

class DataProcessingWorker(QThread):
    """
    数据处理工作线程
    
    将耗时的数据处理任务放到后台执行，
    通过信号更新进度和返回结果
    """
    
    # 定义信号
    progress = pyqtSignal(int, str)      # 进度(百分比, 消息)
    result = pyqtSignal(object)          # 结果
    error = pyqtSignal(str)              # 错误
    finished = pyqtSignal()              # 完成
    
    def __init__(self, data_size: int, iterations: int):
        super().__init__()
        self.data_size = data_size
        self.iterations = iterations
        self._is_cancelled = False
    
    def run(self):
        """线程执行的任务"""
        try:
            self.progress.emit(0, "开始处理...")
            
            # 生成数据
            self.progress.emit(5, f"生成 {self.data_size} 个数据点...")
            data = np.random.randn(self.data_size)
            time.sleep(0.5)
            
            if self._is_cancelled:
                return
            
            results = []
            
            # 模拟耗时计算
            for i in range(self.iterations):
                if self._is_cancelled:
                    self.progress.emit(0, "任务已取消")
                    return
                
                # 模拟复杂计算
                processed = np.fft.fft(data)
                processed = np.abs(processed)
                result = np.mean(processed)
                results.append(result)
                
                # 更新进度
                progress = int((i + 1) / self.iterations * 90) + 5
                self.progress.emit(progress, f"迭代 {i+1}/{self.iterations}")
                
                # 模拟耗时
                time.sleep(0.1)
            
            # 完成
            self.progress.emit(100, "处理完成!")
            
            # 发送结果
            final_result = {
                "mean": np.mean(results),
                "std": np.std(results),
                "min": np.min(results),
                "max": np.max(results),
                "data_size": self.data_size,
                "iterations": self.iterations
            }
            self.result.emit(final_result)
            
        except Exception as e:
            self.error.emit(str(e))
        
        finally:
            self.finished.emit()
    
    def cancel(self):
        """取消任务"""
        self._is_cancelled = True


class SimulationWorker(QThread):
    """
    物理模拟工作线程
    
    模拟蒙特卡洛模拟等耗时计算
    """
    
    progress = pyqtSignal(int)
    step_result = pyqtSignal(int, float)  # 步数, 结果
    finished = pyqtSignal(list)
    
    def __init__(self, n_steps: int, n_particles: int):
        super().__init__()
        self.n_steps = n_steps
        self.n_particles = n_particles
        self._is_running = True
    
    def run(self):
        """随机游走模拟"""
        positions = np.zeros(self.n_particles)
        history = []
        
        for step in range(self.n_steps):
            if not self._is_running:
                break
            
            # 随机游走步进
            moves = np.random.choice([-1, 1], size=self.n_particles)
            positions += moves
            
            # 计算均方位移
            msd = np.mean(positions**2)
            history.append(msd)
            
            # 发送进度和结果
            progress = int((step + 1) / self.n_steps * 100)
            self.progress.emit(progress)
            self.step_result.emit(step, msd)
            
            time.sleep(0.02)  # 控制速度
        
        self.finished.emit(history)
    
    def stop(self):
        """停止模拟"""
        self._is_running = False


# ============================================================
# 主窗口
# ============================================================

class ThreadingDemo(QMainWindow):
    """多线程演示"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.sim_worker = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("多线程 - 防止界面冻结")
        self.setMinimumSize(700, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        
        # 说明
        info = QLabel(
            "💡 将耗时任务放到QThread中执行，防止界面冻结。\n"
            "通过信号(pyqtSignal)更新界面，实现线程安全的通信。"
        )
        info.setStyleSheet("""
            background-color: #fef9e7;
            padding: 15px;
            border-radius: 5px;
            color: #856404;
        """)
        main_layout.addWidget(info)
        
        # 演示1：数据处理
        main_layout.addWidget(self.create_data_processing_demo())
        
        # 演示2：物理模拟
        main_layout.addWidget(self.create_simulation_demo())
        
        # 日志
        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 11px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
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
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def create_data_processing_demo(self) -> QGroupBox:
        """创建数据处理演示"""
        group = QGroupBox("示例1: 数据处理任务")
        layout = QVBoxLayout()
        
        # 参数
        param_layout = QHBoxLayout()
        
        param_layout.addWidget(QLabel("数据量:"))
        self.spin_data_size = QSpinBox()
        self.spin_data_size.setRange(1000, 100000)
        self.spin_data_size.setValue(10000)
        self.spin_data_size.setSingleStep(1000)
        param_layout.addWidget(self.spin_data_size)
        
        param_layout.addWidget(QLabel("迭代次数:"))
        self.spin_iterations = QSpinBox()
        self.spin_iterations.setRange(5, 100)
        self.spin_iterations.setValue(20)
        param_layout.addWidget(self.spin_iterations)
        
        param_layout.addStretch()
        layout.addLayout(param_layout)
        
        # 进度条
        self.progress1 = QProgressBar()
        self.progress1.setRange(0, 100)
        layout.addWidget(self.progress1)
        
        self.label_status1 = QLabel("就绪")
        self.label_status1.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(self.label_status1)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.btn_start1 = QPushButton("▶ 开始处理")
        self.btn_start1.setStyleSheet("background-color: #27ae60;")
        self.btn_start1.clicked.connect(self.start_processing)
        btn_layout.addWidget(self.btn_start1)
        
        self.btn_cancel1 = QPushButton("✖ 取消")
        self.btn_cancel1.setStyleSheet("background-color: #e74c3c;")
        self.btn_cancel1.setEnabled(False)
        self.btn_cancel1.clicked.connect(self.cancel_processing)
        btn_layout.addWidget(self.btn_cancel1)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def create_simulation_demo(self) -> QGroupBox:
        """创建物理模拟演示"""
        group = QGroupBox("示例2: 蒙特卡洛模拟 (随机游走)")
        layout = QVBoxLayout()
        
        # 参数
        param_layout = QHBoxLayout()
        
        param_layout.addWidget(QLabel("步数:"))
        self.spin_steps = QSpinBox()
        self.spin_steps.setRange(100, 1000)
        self.spin_steps.setValue(200)
        param_layout.addWidget(self.spin_steps)
        
        param_layout.addWidget(QLabel("粒子数:"))
        self.spin_particles = QSpinBox()
        self.spin_particles.setRange(100, 10000)
        self.spin_particles.setValue(1000)
        param_layout.addWidget(self.spin_particles)
        
        param_layout.addStretch()
        layout.addLayout(param_layout)
        
        # 进度条
        self.progress2 = QProgressBar()
        self.progress2.setRange(0, 100)
        layout.addWidget(self.progress2)
        
        self.label_msd = QLabel("均方位移: --")
        self.label_msd.setStyleSheet("font-size: 14px; color: #3498db;")
        layout.addWidget(self.label_msd)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        self.btn_start2 = QPushButton("▶ 开始模拟")
        self.btn_start2.setStyleSheet("background-color: #9b59b6;")
        self.btn_start2.clicked.connect(self.start_simulation)
        btn_layout.addWidget(self.btn_start2)
        
        self.btn_stop2 = QPushButton("⏹ 停止")
        self.btn_stop2.setStyleSheet("background-color: #e74c3c;")
        self.btn_stop2.setEnabled(False)
        self.btn_stop2.clicked.connect(self.stop_simulation)
        btn_layout.addWidget(self.btn_stop2)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    # ========== 数据处理 ==========
    
    def start_processing(self):
        """开始数据处理"""
        self.log("开始数据处理任务...")
        
        # 创建工作线程
        self.worker = DataProcessingWorker(
            self.spin_data_size.value(),
            self.spin_iterations.value()
        )
        
        # 连接信号
        self.worker.progress.connect(self.on_processing_progress)
        self.worker.result.connect(self.on_processing_result)
        self.worker.error.connect(self.on_processing_error)
        self.worker.finished.connect(self.on_processing_finished)
        
        # 更新UI
        self.btn_start1.setEnabled(False)
        self.btn_cancel1.setEnabled(True)
        
        # 启动线程
        self.worker.start()
    
    def cancel_processing(self):
        """取消处理"""
        if self.worker:
            self.worker.cancel()
            self.log("正在取消任务...")
    
    def on_processing_progress(self, value: int, message: str):
        """处理进度更新"""
        self.progress1.setValue(value)
        self.label_status1.setText(message)
    
    def on_processing_result(self, result: dict):
        """处理结果"""
        self.log(f"处理完成!")
        self.log(f"  数据量: {result['data_size']}")
        self.log(f"  迭代次数: {result['iterations']}")
        self.log(f"  结果均值: {result['mean']:.4f}")
        self.log(f"  结果标准差: {result['std']:.4f}")
    
    def on_processing_error(self, error: str):
        """处理错误"""
        self.log(f"错误: {error}")
        self.label_status1.setText(f"错误: {error}")
    
    def on_processing_finished(self):
        """处理完成"""
        self.btn_start1.setEnabled(True)
        self.btn_cancel1.setEnabled(False)
        self.worker = None
    
    # ========== 物理模拟 ==========
    
    def start_simulation(self):
        """开始模拟"""
        self.log("开始蒙特卡洛模拟...")
        
        self.sim_worker = SimulationWorker(
            self.spin_steps.value(),
            self.spin_particles.value()
        )
        
        self.sim_worker.progress.connect(self.progress2.setValue)
        self.sim_worker.step_result.connect(self.on_simulation_step)
        self.sim_worker.finished.connect(self.on_simulation_finished)
        
        self.btn_start2.setEnabled(False)
        self.btn_stop2.setEnabled(True)
        
        self.sim_worker.start()
    
    def stop_simulation(self):
        """停止模拟"""
        if self.sim_worker:
            self.sim_worker.stop()
            self.log("模拟已停止")
    
    def on_simulation_step(self, step: int, msd: float):
        """模拟步进"""
        self.label_msd.setText(f"步数: {step+1} | 均方位移: {msd:.2f}")
    
    def on_simulation_finished(self, history: list):
        """模拟完成"""
        self.btn_start2.setEnabled(True)
        self.btn_stop2.setEnabled(False)
        
        if history:
            self.log(f"模拟完成! 共 {len(history)} 步")
            self.log(f"最终均方位移: {history[-1]:.2f}")
            # 扩散系数 D ≈ MSD / (2 * t)
            D = history[-1] / (2 * len(history))
            self.log(f"扩散系数 D ≈ {D:.4f}")
        
        self.sim_worker = None
    
    def log(self, message: str):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")


def main():
    app = QApplication(sys.argv)
    window = ThreadingDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

