"""
示例程序：温度控制器界面
所属章节：第七章 - 仪器控制界面实战

功能说明：
    模拟完整的温度控制器界面：
    - 温度实时显示和曲线
    - PID参数设置
    - 升温/降温控制
    - 数据记录和导出

运行方式：
    python temperature_controller.py
"""

import sys
import time
import numpy as np
from datetime import datetime
from collections import deque
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDoubleSpinBox, QGroupBox, QFormLayout,
    QComboBox, QTextEdit, QSpinBox, QProgressBar, QFileDialog,
    QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TemperatureSimulator(QThread):
    """温度模拟器（模拟真实温控器行为）"""
    
    temperature_updated = pyqtSignal(float)
    status_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_temp = 300.0  # 当前温度 (K)
        self.target_temp = 300.0   # 目标温度
        self.running = False
        
        # PID参数
        self.kp = 1.0
        self.ki = 0.1
        self.kd = 0.05
        
        # PID状态
        self.integral = 0
        self.last_error = 0
        
        # 加热/冷却功率限制
        self.max_heat_rate = 5.0   # K/s
        self.max_cool_rate = 3.0   # K/s
    
    def run(self):
        self.running = True
        dt = 0.1  # 100ms更新间隔
        
        while self.running:
            # PID控制
            error = self.target_temp - self.current_temp
            self.integral += error * dt
            derivative = (error - self.last_error) / dt
            
            # 计算输出
            output = self.kp * error + self.ki * self.integral + self.kd * derivative
            
            # 限制变化率
            if output > 0:
                delta = min(output * dt, self.max_heat_rate * dt)
            else:
                delta = max(output * dt, -self.max_cool_rate * dt)
            
            # 添加噪声
            noise = np.random.randn() * 0.1
            self.current_temp += delta + noise
            
            # 更新状态
            self.last_error = error
            
            # 发送温度
            self.temperature_updated.emit(self.current_temp)
            
            # 状态判断
            if abs(error) < 0.5:
                self.status_changed.emit("稳定")
            elif error > 0:
                self.status_changed.emit("升温中")
            else:
                self.status_changed.emit("降温中")
            
            self.msleep(100)
    
    def stop(self):
        self.running = False
        self.wait()
    
    def set_target(self, temp: float):
        self.target_temp = temp
        self.integral = 0  # 重置积分项
    
    def set_pid(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self):
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)


class TemperatureController(QMainWindow):
    """温度控制器界面"""
    
    def __init__(self):
        super().__init__()
        
        # 数据存储
        self.temp_history = deque(maxlen=600)  # 保留10分钟数据
        self.time_history = deque(maxlen=600)
        self.start_time = time.time()
        self.is_recording = False
        self.recorded_data = []
        
        # 模拟器
        self.simulator = TemperatureSimulator()
        self.simulator.temperature_updated.connect(self.on_temperature_update)
        self.simulator.status_changed.connect(self.on_status_change)
        
        self.init_ui()
        
        # 启动模拟器
        self.simulator.start()
        
        # 图形更新定时器
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(500)  # 500ms更新一次图形
    
    def init_ui(self):
        self.setWindowTitle("温度控制器")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # 连接状态
        conn_group = QGroupBox("连接状态")
        conn_layout = QVBoxLayout()
        
        self.label_conn_status = QLabel("● 已连接（模拟模式）")
        self.label_conn_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        conn_layout.addWidget(self.label_conn_status)
        
        conn_group.setLayout(conn_layout)
        left_layout.addWidget(conn_group)
        
        # 温度显示
        temp_group = QGroupBox("温度")
        temp_layout = QVBoxLayout()
        
        self.label_current_temp = QLabel("300.0")
        self.label_current_temp.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.label_current_temp.setStyleSheet("color: #e74c3c;")
        self.label_current_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp_layout.addWidget(self.label_current_temp)
        
        temp_layout.addWidget(QLabel("K", alignment=Qt.AlignmentFlag.AlignCenter))
        
        temp_group.setLayout(temp_layout)
        left_layout.addWidget(temp_group)
        
        # 目标温度设置
        target_group = QGroupBox("目标温度")
        target_layout = QFormLayout()
        
        self.spin_target = QDoubleSpinBox()
        self.spin_target.setRange(4, 500)
        self.spin_target.setValue(300)
        self.spin_target.setSuffix(" K")
        self.spin_target.setDecimals(1)
        target_layout.addRow("设定值:", self.spin_target)
        
        # 快捷温度按钮
        quick_layout = QHBoxLayout()
        for temp in [4.2, 77, 300, 400]:
            btn = QPushButton(f"{temp}K")
            btn.clicked.connect(lambda c, t=temp: self.spin_target.setValue(t))
            quick_layout.addWidget(btn)
        target_layout.addRow("快捷:", quick_layout)
        
        btn_set_target = QPushButton("🎯 设置目标温度")
        btn_set_target.clicked.connect(self.set_target_temperature)
        target_layout.addRow("", btn_set_target)
        
        target_group.setLayout(target_layout)
        left_layout.addWidget(target_group)
        
        # PID参数
        pid_group = QGroupBox("PID参数")
        pid_layout = QFormLayout()
        
        self.spin_kp = QDoubleSpinBox()
        self.spin_kp.setRange(0, 10)
        self.spin_kp.setValue(1.0)
        self.spin_kp.setSingleStep(0.1)
        pid_layout.addRow("Kp:", self.spin_kp)
        
        self.spin_ki = QDoubleSpinBox()
        self.spin_ki.setRange(0, 1)
        self.spin_ki.setValue(0.1)
        self.spin_ki.setSingleStep(0.01)
        pid_layout.addRow("Ki:", self.spin_ki)
        
        self.spin_kd = QDoubleSpinBox()
        self.spin_kd.setRange(0, 1)
        self.spin_kd.setValue(0.05)
        self.spin_kd.setSingleStep(0.01)
        pid_layout.addRow("Kd:", self.spin_kd)
        
        btn_apply_pid = QPushButton("应用PID参数")
        btn_apply_pid.clicked.connect(self.apply_pid)
        pid_layout.addRow("", btn_apply_pid)
        
        pid_group.setLayout(pid_layout)
        left_layout.addWidget(pid_group)
        
        # 数据记录
        record_group = QGroupBox("数据记录")
        record_layout = QVBoxLayout()
        
        self.btn_record = QPushButton("⏺ 开始记录")
        self.btn_record.setCheckable(True)
        self.btn_record.clicked.connect(self.toggle_recording)
        record_layout.addWidget(self.btn_record)
        
        self.label_record_count = QLabel("已记录: 0 点")
        record_layout.addWidget(self.label_record_count)
        
        btn_export = QPushButton("💾 导出数据")
        btn_export.clicked.connect(self.export_data)
        record_layout.addWidget(btn_export)
        
        record_group.setLayout(record_layout)
        left_layout.addWidget(record_group)
        
        left_layout.addStretch()
        
        # 紧急停止
        btn_stop = QPushButton("⚠ 紧急停止")
        btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover { background-color: #e74c3c; }
        """)
        btn_stop.clicked.connect(self.emergency_stop)
        left_layout.addWidget(btn_stop)
        
        main_layout.addWidget(left_panel)
        
        # 右侧图形和日志
        right_layout = QVBoxLayout()
        
        # 温度曲线
        plot_group = QGroupBox("温度曲线")
        plot_layout = QVBoxLayout()
        
        self.canvas = MplCanvas()
        plot_layout.addWidget(self.canvas)
        
        plot_group.setLayout(plot_layout)
        right_layout.addWidget(plot_group, stretch=2)
        
        # 日志
        log_group = QGroupBox("系统日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            font-family: Consolas, monospace;
            font-size: 11px;
            background-color: #2c3e50;
            color: #ecf0f1;
        """)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        right_layout.addWidget(log_group, stretch=1)
        
        main_layout.addLayout(right_layout)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
        self.label_status = QLabel("状态: 稳定")
        self.statusBar().addPermanentWidget(self.label_status)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #ecf0f1; }
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
                color: #2980b9;
            }
            QPushButton {
                padding: 8px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QDoubleSpinBox, QSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
        
        self.log("温度控制器已启动")
        self.log("模拟模式运行中")
    
    def on_temperature_update(self, temp: float):
        """温度更新"""
        # 更新显示
        self.label_current_temp.setText(f"{temp:.1f}")
        
        # 记录历史
        current_time = time.time() - self.start_time
        self.temp_history.append(temp)
        self.time_history.append(current_time)
        
        # 数据记录
        if self.is_recording:
            self.recorded_data.append({
                'time': current_time,
                'temperature': temp,
                'target': self.simulator.target_temp
            })
            self.label_record_count.setText(f"已记录: {len(self.recorded_data)} 点")
    
    def on_status_change(self, status: str):
        """状态更新"""
        self.label_status.setText(f"状态: {status}")
        
        # 更新温度显示颜色
        if status == "稳定":
            self.label_current_temp.setStyleSheet("color: #27ae60;")
        elif status == "升温中":
            self.label_current_temp.setStyleSheet("color: #e74c3c;")
        else:
            self.label_current_temp.setStyleSheet("color: #3498db;")
    
    def set_target_temperature(self):
        """设置目标温度"""
        target = self.spin_target.value()
        self.simulator.set_target(target)
        self.log(f"目标温度设置为 {target:.1f} K")
    
    def apply_pid(self):
        """应用PID参数"""
        kp = self.spin_kp.value()
        ki = self.spin_ki.value()
        kd = self.spin_kd.value()
        self.simulator.set_pid(kp, ki, kd)
        self.log(f"PID参数更新: Kp={kp}, Ki={ki}, Kd={kd}")
    
    def toggle_recording(self, checked: bool):
        """切换记录状态"""
        self.is_recording = checked
        if checked:
            self.recorded_data = []
            self.btn_record.setText("⏹ 停止记录")
            self.btn_record.setStyleSheet("background-color: #e74c3c;")
            self.log("开始记录数据")
        else:
            self.btn_record.setText("⏺ 开始记录")
            self.btn_record.setStyleSheet("")
            self.log(f"停止记录，共 {len(self.recorded_data)} 个数据点")
    
    def export_data(self):
        """导出数据"""
        if not self.recorded_data:
            QMessageBox.warning(self, "警告", "没有可导出的数据")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出数据", "temperature_data.csv", "CSV文件 (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Time(s),Temperature(K),Target(K)\n")
                    for d in self.recorded_data:
                        f.write(f"{d['time']:.2f},{d['temperature']:.2f},{d['target']:.2f}\n")
                
                self.log(f"数据已导出到 {filename}")
                QMessageBox.information(self, "成功", f"数据已导出:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))
    
    def emergency_stop(self):
        """紧急停止"""
        # 设置目标为当前温度
        current = self.simulator.current_temp
        self.simulator.set_target(current)
        self.spin_target.setValue(current)
        self.log("⚠ 紧急停止！目标温度设置为当前温度")
    
    def update_plot(self):
        """更新图形"""
        if not self.time_history:
            return
        
        self.canvas.ax.clear()
        
        times = list(self.time_history)
        temps = list(self.temp_history)
        
        # 温度曲线
        self.canvas.ax.plot(times, temps, 'b-', linewidth=1.5, label='当前温度')
        
        # 目标温度线
        target = self.simulator.target_temp
        self.canvas.ax.axhline(y=target, color='r', linestyle='--', 
                               linewidth=1, label=f'目标 {target:.1f}K')
        
        self.canvas.ax.set_xlabel('时间 (s)')
        self.canvas.ax.set_ylabel('温度 (K)')
        self.canvas.ax.set_title('温度监控')
        self.canvas.ax.legend(loc='upper right')
        self.canvas.ax.grid(True, alpha=0.3)
        
        # 设置Y轴范围
        if temps:
            y_min = min(min(temps), target) - 10
            y_max = max(max(temps), target) + 10
            self.canvas.ax.set_ylim(y_min, y_max)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
    
    def log(self, message: str):
        """添加日志"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")
    
    def closeEvent(self, event):
        """关闭窗口"""
        self.simulator.stop()
        self.plot_timer.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = TemperatureController()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

