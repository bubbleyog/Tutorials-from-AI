"""
示例程序：数据采集系统
所属章节：第七章 - 仪器控制界面实战

功能说明：
    模拟多通道数据采集系统：
    - 多通道实时显示
    - 采样率配置
    - 触发模式
    - 数据记录和导出

运行方式：
    python data_acquisition.py
"""

import sys
import time
import numpy as np
from datetime import datetime
from collections import deque
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDoubleSpinBox, QGroupBox, QFormLayout,
    QComboBox, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QColor

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DataAcquisitionThread(QThread):
    """数据采集线程"""
    
    data_ready = pyqtSignal(np.ndarray)
    
    def __init__(self, channels: int, sample_rate: float):
        super().__init__()
        self.channels = channels
        self.sample_rate = sample_rate
        self.running = False
        self.t = 0
    
    def run(self):
        self.running = True
        buffer_size = int(self.sample_rate * 0.05)  # 50ms缓冲
        
        while self.running:
            # 模拟数据采集
            t = np.arange(buffer_size) / self.sample_rate + self.t
            self.t += buffer_size / self.sample_rate
            
            data = np.zeros((self.channels, buffer_size))
            
            # 生成模拟信号
            for i in range(self.channels):
                freq = (i + 1) * 5  # 5, 10, 15, 20 Hz
                amp = 1 + i * 0.5
                noise = np.random.randn(buffer_size) * 0.1
                data[i] = amp * np.sin(2 * np.pi * freq * t) + noise
            
            self.data_ready.emit(data)
            
            # 控制采集速率
            self.msleep(50)
    
    def stop(self):
        self.running = False
        self.wait()


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self):
        self.fig = Figure(figsize=(12, 6), dpi=100)
        super().__init__(self.fig)


class DataAcquisition(QMainWindow):
    """数据采集系统"""
    
    CHANNEL_COLORS = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', 
                      '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
    
    def __init__(self):
        super().__init__()
        
        self.num_channels = 4
        self.sample_rate = 1000
        self.buffer_size = 2000  # 显示2秒数据
        
        # 数据缓冲区
        self.data_buffers = [deque(maxlen=self.buffer_size) for _ in range(8)]
        self.time_buffer = deque(maxlen=self.buffer_size)
        
        # 采集线程
        self.daq_thread = None
        self.is_acquiring = False
        
        # 记录
        self.is_recording = False
        self.recorded_data = []
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("多通道数据采集系统")
        self.setMinimumSize(1200, 800)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # 采集设置
        acq_group = QGroupBox("采集设置")
        acq_layout = QFormLayout()
        
        self.spin_channels = QSpinBox()
        self.spin_channels.setRange(1, 8)
        self.spin_channels.setValue(4)
        acq_layout.addRow("通道数:", self.spin_channels)
        
        self.combo_sample_rate = QComboBox()
        self.combo_sample_rate.addItems(['100', '500', '1000', '2000', '5000', '10000'])
        self.combo_sample_rate.setCurrentText('1000')
        acq_layout.addRow("采样率 (Hz):", self.combo_sample_rate)
        
        self.combo_trigger = QComboBox()
        self.combo_trigger.addItems(['连续', '边沿触发', '电平触发'])
        acq_layout.addRow("触发模式:", self.combo_trigger)
        
        self.spin_trigger_level = QDoubleSpinBox()
        self.spin_trigger_level.setRange(-10, 10)
        self.spin_trigger_level.setValue(0)
        self.spin_trigger_level.setSuffix(" V")
        acq_layout.addRow("触发电平:", self.spin_trigger_level)
        
        acq_group.setLayout(acq_layout)
        left_layout.addWidget(acq_group)
        
        # 通道设置
        channel_group = QGroupBox("通道显示")
        channel_layout = QVBoxLayout()
        
        self.channel_checks = []
        for i in range(8):
            check = QCheckBox(f"CH{i+1}")
            check.setChecked(i < 4)
            check.setStyleSheet(f"color: {self.CHANNEL_COLORS[i]}; font-weight: bold;")
            self.channel_checks.append(check)
            channel_layout.addWidget(check)
        
        channel_group.setLayout(channel_layout)
        left_layout.addWidget(channel_group)
        
        # 控制按钮
        control_group = QGroupBox("控制")
        control_layout = QVBoxLayout()
        
        self.btn_start = QPushButton("▶ 开始采集")
        self.btn_start.clicked.connect(self.toggle_acquisition)
        control_layout.addWidget(self.btn_start)
        
        self.btn_single = QPushButton("📷 单次采集")
        self.btn_single.clicked.connect(self.single_acquisition)
        control_layout.addWidget(self.btn_single)
        
        control_group.setLayout(control_layout)
        left_layout.addWidget(control_group)
        
        # 记录
        record_group = QGroupBox("数据记录")
        record_layout = QVBoxLayout()
        
        self.btn_record = QPushButton("⏺ 开始记录")
        self.btn_record.setCheckable(True)
        self.btn_record.clicked.connect(self.toggle_recording)
        record_layout.addWidget(self.btn_record)
        
        self.label_record_info = QLabel("已记录: 0 点")
        record_layout.addWidget(self.label_record_info)
        
        self.progress_record = QProgressBar()
        self.progress_record.setRange(0, 100)
        record_layout.addWidget(self.progress_record)
        
        btn_export = QPushButton("💾 导出数据")
        btn_export.clicked.connect(self.export_data)
        record_layout.addWidget(btn_export)
        
        record_group.setLayout(record_layout)
        left_layout.addWidget(record_group)
        
        left_layout.addStretch()
        
        # 统计信息
        stats_group = QGroupBox("实时统计")
        stats_layout = QVBoxLayout()
        
        self.stats_table = QTableWidget(8, 4)
        self.stats_table.setHorizontalHeaderLabels(['通道', '均值', '最大', '最小'])
        self.stats_table.setMaximumHeight(200)
        
        for i in range(8):
            self.stats_table.setItem(i, 0, QTableWidgetItem(f"CH{i+1}"))
            self.stats_table.setItem(i, 1, QTableWidgetItem("-"))
            self.stats_table.setItem(i, 2, QTableWidgetItem("-"))
            self.stats_table.setItem(i, 3, QTableWidgetItem("-"))
        
        stats_layout.addWidget(self.stats_table)
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        main_layout.addWidget(left_panel)
        
        # 右侧波形显示
        right_layout = QVBoxLayout()
        
        # 波形画布
        self.canvas = MplCanvas()
        right_layout.addWidget(self.canvas)
        
        # 显示设置
        display_layout = QHBoxLayout()
        
        display_layout.addWidget(QLabel("时间范围:"))
        self.combo_time_range = QComboBox()
        self.combo_time_range.addItems(['0.5s', '1s', '2s', '5s', '10s'])
        self.combo_time_range.setCurrentText('2s')
        self.combo_time_range.currentIndexChanged.connect(self.update_buffer_size)
        display_layout.addWidget(self.combo_time_range)
        
        display_layout.addWidget(QLabel("Y轴范围:"))
        self.spin_y_min = QDoubleSpinBox()
        self.spin_y_min.setRange(-100, 100)
        self.spin_y_min.setValue(-5)
        display_layout.addWidget(self.spin_y_min)
        
        display_layout.addWidget(QLabel("~"))
        self.spin_y_max = QDoubleSpinBox()
        self.spin_y_max.setRange(-100, 100)
        self.spin_y_max.setValue(5)
        display_layout.addWidget(self.spin_y_max)
        
        self.check_auto_scale = QCheckBox("自动缩放")
        self.check_auto_scale.setChecked(True)
        display_layout.addWidget(self.check_auto_scale)
        
        display_layout.addStretch()
        
        right_layout.addLayout(display_layout)
        
        main_layout.addLayout(right_layout)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
        self.label_status = QLabel("状态: 停止")
        self.statusBar().addPermanentWidget(self.label_status)
        
        # 绘图更新定时器
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(50)  # 20fps
        
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #34495e;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #34495e;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #3498db;
            }
            QLabel { color: white; }
            QPushButton {
                padding: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:checked { background-color: #e74c3c; }
            QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 4px;
            }
            QCheckBox { color: white; }
            QTableWidget {
                background-color: #2c3e50;
                color: white;
                gridline-color: #34495e;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
            }
            QProgressBar {
                border: 1px solid #34495e;
                border-radius: 3px;
                background-color: #2c3e50;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
            }
        """)
    
    def update_buffer_size(self):
        """更新缓冲区大小"""
        time_range_text = self.combo_time_range.currentText()
        time_range = float(time_range_text.replace('s', ''))
        self.buffer_size = int(time_range * self.sample_rate)
        
        # 重新初始化缓冲区
        self.data_buffers = [deque(maxlen=self.buffer_size) for _ in range(8)]
        self.time_buffer = deque(maxlen=self.buffer_size)
    
    def toggle_acquisition(self):
        """切换采集状态"""
        if self.is_acquiring:
            self.stop_acquisition()
        else:
            self.start_acquisition()
    
    def start_acquisition(self):
        """开始采集"""
        self.num_channels = self.spin_channels.value()
        self.sample_rate = int(self.combo_sample_rate.currentText())
        self.update_buffer_size()
        
        # 清空缓冲区
        for buf in self.data_buffers:
            buf.clear()
        self.time_buffer.clear()
        
        # 创建并启动采集线程
        self.daq_thread = DataAcquisitionThread(self.num_channels, self.sample_rate)
        self.daq_thread.data_ready.connect(self.on_data_ready)
        self.daq_thread.start()
        
        self.is_acquiring = True
        self.btn_start.setText("⏹ 停止采集")
        self.label_status.setText("状态: 采集中")
        self.label_status.setStyleSheet("color: #2ecc71;")
    
    def stop_acquisition(self):
        """停止采集"""
        if self.daq_thread:
            self.daq_thread.stop()
            self.daq_thread = None
        
        self.is_acquiring = False
        self.btn_start.setText("▶ 开始采集")
        self.label_status.setText("状态: 停止")
        self.label_status.setStyleSheet("color: #e74c3c;")
    
    def single_acquisition(self):
        """单次采集"""
        if self.is_acquiring:
            return
        
        # 模拟单次采集
        num_samples = 1000
        t = np.arange(num_samples) / 1000
        
        for buf in self.data_buffers:
            buf.clear()
        self.time_buffer.clear()
        
        for i in range(num_samples):
            self.time_buffer.append(t[i])
            for ch in range(self.num_channels):
                freq = (ch + 1) * 5
                value = (1 + ch * 0.5) * np.sin(2 * np.pi * freq * t[i])
                self.data_buffers[ch].append(value)
        
        self.update_plot()
        self.statusBar().showMessage("单次采集完成", 2000)
    
    def on_data_ready(self, data: np.ndarray):
        """接收采集数据"""
        channels, samples = data.shape
        
        # 更新时间缓冲区
        current_time = len(self.time_buffer) / self.sample_rate
        for i in range(samples):
            self.time_buffer.append(current_time + i / self.sample_rate)
        
        # 更新数据缓冲区
        for ch in range(channels):
            for value in data[ch]:
                self.data_buffers[ch].append(value)
        
        # 记录数据
        if self.is_recording:
            for i in range(samples):
                point = {'time': self.time_buffer[-samples + i]}
                for ch in range(channels):
                    point[f'ch{ch+1}'] = data[ch, i]
                self.recorded_data.append(point)
            
            self.label_record_info.setText(f"已记录: {len(self.recorded_data)} 点")
            
            # 更新进度（假设记录10万点）
            progress = min(100, len(self.recorded_data) // 1000)
            self.progress_record.setValue(progress)
        
        # 更新统计
        self.update_statistics(data)
    
    def update_statistics(self, data: np.ndarray):
        """更新统计信息"""
        for ch in range(data.shape[0]):
            ch_data = data[ch]
            self.stats_table.item(ch, 1).setText(f"{np.mean(ch_data):.3f}")
            self.stats_table.item(ch, 2).setText(f"{np.max(ch_data):.3f}")
            self.stats_table.item(ch, 3).setText(f"{np.min(ch_data):.3f}")
    
    def update_plot(self):
        """更新波形显示"""
        self.canvas.fig.clear()
        ax = self.canvas.fig.add_subplot(111)
        ax.set_facecolor('#1a1a2e')
        
        if not self.time_buffer:
            self.canvas.draw()
            return
        
        t = list(self.time_buffer)
        
        for ch in range(8):
            if self.channel_checks[ch].isChecked() and self.data_buffers[ch]:
                data = list(self.data_buffers[ch])
                if len(data) == len(t):
                    ax.plot(t, data, color=self.CHANNEL_COLORS[ch], 
                           linewidth=1, label=f'CH{ch+1}')
        
        ax.set_xlabel('时间 (s)', color='white')
        ax.set_ylabel('电压 (V)', color='white')
        ax.set_title('实时波形', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3, color='gray')
        ax.legend(loc='upper right')
        
        if self.check_auto_scale.isChecked():
            ax.autoscale()
        else:
            ax.set_ylim(self.spin_y_min.value(), self.spin_y_max.value())
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
    
    def toggle_recording(self, checked: bool):
        """切换记录状态"""
        self.is_recording = checked
        if checked:
            self.recorded_data = []
            self.btn_record.setText("⏹ 停止记录")
            self.progress_record.setValue(0)
        else:
            self.btn_record.setText("⏺ 开始记录")
    
    def export_data(self):
        """导出数据"""
        if not self.recorded_data:
            QMessageBox.warning(self, "警告", "没有可导出的数据")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出数据", "daq_data.csv", "CSV文件 (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    # 写入表头
                    headers = ['Time(s)'] + [f'CH{i+1}(V)' for i in range(self.num_channels)]
                    f.write(','.join(headers) + '\n')
                    
                    # 写入数据
                    for point in self.recorded_data:
                        values = [f"{point['time']:.6f}"]
                        for ch in range(self.num_channels):
                            values.append(f"{point.get(f'ch{ch+1}', 0):.6f}")
                        f.write(','.join(values) + '\n')
                
                QMessageBox.information(self, "成功", f"数据已导出:\n{filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))
    
    def closeEvent(self, event):
        """关闭窗口"""
        self.stop_acquisition()
        self.plot_timer.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DataAcquisition()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

