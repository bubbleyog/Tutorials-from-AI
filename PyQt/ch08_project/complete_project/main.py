"""
完整项目示例：低温测量系统控制软件
所属章节：第八章 - 项目实战与部署

功能说明：
    整合教程所有知识的完整项目：
    - 仪器管理（温控器、电源、万用表）
    - 数据采集与显示
    - 配置管理
    - 日志系统
    - 深色主题UI

运行方式：
    python main.py
"""

import sys
import os
import logging
from datetime import datetime
from collections import deque
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QGroupBox, QFormLayout, QDoubleSpinBox,
    QTextEdit, QTabWidget, QStatusBar, QDockWidget, QToolBar,
    QComboBox, QSpinBox, QCheckBox, QProgressBar, QSplitter,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QIcon

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ============================================================
# 日志配置
# ============================================================

def setup_logging():
    """配置日志系统"""
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/app.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================
# 模拟仪器类
# ============================================================

class SimulatedTemperatureController:
    """模拟温度控制器"""
    
    def __init__(self):
        self.temperature = 300.0
        self.target = 300.0
        self.connected = False
    
    def connect(self):
        self.connected = True
        logger.info("温度控制器已连接")
    
    def disconnect(self):
        self.connected = False
        logger.info("温度控制器已断开")
    
    def read_temperature(self) -> float:
        if not self.connected:
            return 0
        # 模拟PID控制
        error = self.target - self.temperature
        self.temperature += error * 0.1 + np.random.randn() * 0.1
        return self.temperature
    
    def set_target(self, temp: float):
        self.target = temp
        logger.info(f"温度目标设置为 {temp:.1f} K")


class SimulatedPowerSupply:
    """模拟电源"""
    
    def __init__(self):
        self.voltage = 0.0
        self.current = 0.0
        self.output = False
        self.connected = False
    
    def connect(self):
        self.connected = True
        logger.info("电源已连接")
    
    def disconnect(self):
        self.connected = False
        logger.info("电源已断开")
    
    def set_voltage(self, v: float):
        self.voltage = v
        if self.output:
            self.current = v / 100 + np.random.randn() * 0.001
    
    def set_output(self, on: bool):
        self.output = on
        logger.info(f"电源输出: {'ON' if on else 'OFF'}")


class SimulatedMultimeter:
    """模拟万用表"""
    
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
        logger.info("万用表已连接")
    
    def disconnect(self):
        self.connected = False
        logger.info("万用表已断开")
    
    def read_voltage(self) -> float:
        if not self.connected:
            return 0
        return 1.5 + np.random.randn() * 0.01
    
    def read_resistance(self) -> float:
        if not self.connected:
            return 0
        return 1000 + np.random.randn() * 10


# ============================================================
# 数据采集线程
# ============================================================

class DataAcquisitionThread(QThread):
    """数据采集线程"""
    
    data_ready = pyqtSignal(dict)
    
    def __init__(self, temp_ctrl, power, dmm):
        super().__init__()
        self.temp_ctrl = temp_ctrl
        self.power = power
        self.dmm = dmm
        self.running = False
        self.interval = 100  # ms
    
    def run(self):
        self.running = True
        while self.running:
            data = {
                'timestamp': datetime.now(),
                'temperature': self.temp_ctrl.read_temperature() if self.temp_ctrl.connected else 0,
                'voltage': self.dmm.read_voltage() if self.dmm.connected else 0,
                'resistance': self.dmm.read_resistance() if self.dmm.connected else 0,
                'power_voltage': self.power.voltage if self.power.connected else 0,
                'power_current': self.power.current if self.power.connected else 0,
            }
            self.data_ready.emit(data)
            self.msleep(self.interval)
    
    def stop(self):
        self.running = False
        self.wait()


# ============================================================
# 图形组件
# ============================================================

class RealtimePlot(FigureCanvas):
    """实时绘图组件"""
    
    def __init__(self, title: str, ylabel: str, color: str = '#3498db'):
        self.fig = Figure(figsize=(6, 3), dpi=100)
        super().__init__(self.fig)
        
        self.ax = self.fig.add_subplot(111)
        self.title = title
        self.ylabel = ylabel
        self.color = color
        
        self.data = deque(maxlen=200)
        self.times = deque(maxlen=200)
        
        self.setup_plot()
    
    def setup_plot(self):
        self.ax.set_facecolor('#1a1a2e')
        self.fig.set_facecolor('#16213e')
        self.ax.set_title(self.title, color='white', fontsize=10)
        self.ax.set_ylabel(self.ylabel, color='white', fontsize=9)
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.grid(True, alpha=0.3, color='gray')
        
        self.line, = self.ax.plot([], [], color=self.color, linewidth=1.5)
        self.fig.tight_layout()
    
    def update_data(self, value: float):
        self.times.append(len(self.times))
        self.data.append(value)
        
        if len(self.data) > 1:
            self.line.set_data(list(self.times), list(self.data))
            self.ax.relim()
            self.ax.autoscale_view()
            self.draw()


# ============================================================
# 主窗口
# ============================================================

class CryoMeasurementSystem(QMainWindow):
    """低温测量系统主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 创建仪器
        self.temp_ctrl = SimulatedTemperatureController()
        self.power = SimulatedPowerSupply()
        self.dmm = SimulatedMultimeter()
        
        # 数据采集
        self.daq_thread = DataAcquisitionThread(
            self.temp_ctrl, self.power, self.dmm
        )
        self.daq_thread.data_ready.connect(self.on_data_received)
        
        # 数据存储
        self.recorded_data = []
        self.is_recording = False
        
        self.init_ui()
        
        logger.info("低温测量系统已启动")
    
    def init_ui(self):
        self.setWindowTitle("低温测量系统控制软件")
        self.setMinimumSize(1400, 900)
        
        # 工具栏
        self.create_toolbar()
        
        # 中心组件
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧图形和数据
        right_layout = QVBoxLayout()
        
        # 实时图形
        right_layout.addWidget(self.create_plot_panel(), stretch=2)
        
        # 数据表格和日志
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        bottom_splitter.addWidget(self.create_data_table())
        bottom_splitter.addWidget(self.create_log_panel())
        bottom_splitter.setSizes([500, 500])
        
        right_layout.addWidget(bottom_splitter, stretch=1)
        
        main_layout.addLayout(right_layout, stretch=1)
        
        # 状态栏
        self.create_status_bar()
        
        # 应用深色主题
        self.apply_dark_theme()
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)
        
        # 连接所有仪器
        action_connect_all = QAction("🔌 连接所有", self)
        action_connect_all.triggered.connect(self.connect_all_instruments)
        toolbar.addAction(action_connect_all)
        
        # 断开所有仪器
        action_disconnect_all = QAction("⏏️ 断开所有", self)
        action_disconnect_all.triggered.connect(self.disconnect_all_instruments)
        toolbar.addAction(action_disconnect_all)
        
        toolbar.addSeparator()
        
        # 开始采集
        self.action_start = QAction("▶ 开始采集", self)
        self.action_start.triggered.connect(self.start_acquisition)
        toolbar.addAction(self.action_start)
        
        # 停止采集
        self.action_stop = QAction("⏹ 停止采集", self)
        self.action_stop.triggered.connect(self.stop_acquisition)
        self.action_stop.setEnabled(False)
        toolbar.addAction(self.action_stop)
        
        toolbar.addSeparator()
        
        # 数据记录
        self.action_record = QAction("⏺ 记录", self)
        self.action_record.setCheckable(True)
        self.action_record.triggered.connect(self.toggle_recording)
        toolbar.addAction(self.action_record)
        
        # 导出数据
        action_export = QAction("💾 导出", self)
        action_export.triggered.connect(self.export_data)
        toolbar.addAction(action_export)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(320)
        layout = QVBoxLayout(panel)
        
        # 温度控制
        temp_group = QGroupBox("温度控制")
        temp_layout = QVBoxLayout()
        
        # 当前温度
        self.label_temp = QLabel("-- K")
        self.label_temp.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.label_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_temp.setStyleSheet("color: #e74c3c;")
        temp_layout.addWidget(self.label_temp)
        
        # 目标温度
        target_layout = QFormLayout()
        self.spin_target_temp = QDoubleSpinBox()
        self.spin_target_temp.setRange(4, 400)
        self.spin_target_temp.setValue(300)
        self.spin_target_temp.setSuffix(" K")
        target_layout.addRow("目标温度:", self.spin_target_temp)
        temp_layout.addLayout(target_layout)
        
        btn_set_temp = QPushButton("设置目标温度")
        btn_set_temp.clicked.connect(self.set_target_temperature)
        temp_layout.addWidget(btn_set_temp)
        
        temp_group.setLayout(temp_layout)
        layout.addWidget(temp_group)
        
        # 电源控制
        power_group = QGroupBox("电源控制")
        power_layout = QFormLayout()
        
        self.spin_voltage = QDoubleSpinBox()
        self.spin_voltage.setRange(0, 30)
        self.spin_voltage.setValue(0)
        self.spin_voltage.setSuffix(" V")
        self.spin_voltage.valueChanged.connect(self.set_voltage)
        power_layout.addRow("电压:", self.spin_voltage)
        
        self.label_current = QLabel("0.000 A")
        power_layout.addRow("电流:", self.label_current)
        
        self.check_output = QCheckBox("输出开关")
        self.check_output.stateChanged.connect(self.toggle_output)
        power_layout.addRow("", self.check_output)
        
        power_group.setLayout(power_layout)
        layout.addWidget(power_group)
        
        # 万用表
        dmm_group = QGroupBox("万用表")
        dmm_layout = QFormLayout()
        
        self.label_dmm_voltage = QLabel("-- V")
        dmm_layout.addRow("电压:", self.label_dmm_voltage)
        
        self.label_dmm_resistance = QLabel("-- Ω")
        dmm_layout.addRow("电阻:", self.label_dmm_resistance)
        
        dmm_group.setLayout(dmm_layout)
        layout.addWidget(dmm_group)
        
        # 采集设置
        acq_group = QGroupBox("采集设置")
        acq_layout = QFormLayout()
        
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(50, 5000)
        self.spin_interval.setValue(100)
        self.spin_interval.setSuffix(" ms")
        acq_layout.addRow("采集间隔:", self.spin_interval)
        
        acq_group.setLayout(acq_layout)
        layout.addWidget(acq_group)
        
        layout.addStretch()
        
        return panel
    
    def create_plot_panel(self) -> QWidget:
        """创建图形面板"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # 温度图
        self.plot_temp = RealtimePlot("温度", "T (K)", "#e74c3c")
        layout.addWidget(self.plot_temp)
        
        # 电压图
        self.plot_voltage = RealtimePlot("电压", "V (V)", "#3498db")
        layout.addWidget(self.plot_voltage)
        
        # 电阻图
        self.plot_resistance = RealtimePlot("电阻", "R (Ω)", "#2ecc71")
        layout.addWidget(self.plot_resistance)
        
        return panel
    
    def create_data_table(self) -> QGroupBox:
        """创建数据表格"""
        group = QGroupBox("实时数据")
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget(0, 6)
        self.data_table.setHorizontalHeaderLabels([
            '时间', '温度(K)', '电压(V)', '电阻(Ω)', '电源电压(V)', '电源电流(A)'
        ])
        self.data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.data_table.setMaximumHeight(200)
        
        layout.addWidget(self.data_table)
        
        self.label_record_count = QLabel("记录: 0 条")
        layout.addWidget(self.label_record_count)
        
        group.setLayout(layout)
        return group
    
    def create_log_panel(self) -> QGroupBox:
        """创建日志面板"""
        group = QGroupBox("系统日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 仪器状态
        self.label_temp_status = QLabel("温控器: ●")
        self.label_temp_status.setStyleSheet("color: #e74c3c;")
        self.status_bar.addWidget(self.label_temp_status)
        
        self.label_power_status = QLabel("电源: ●")
        self.label_power_status.setStyleSheet("color: #e74c3c;")
        self.status_bar.addWidget(self.label_power_status)
        
        self.label_dmm_status = QLabel("万用表: ●")
        self.label_dmm_status.setStyleSheet("color: #e74c3c;")
        self.status_bar.addWidget(self.label_dmm_status)
        
        # 采集状态
        self.label_acq_status = QLabel("采集: 停止")
        self.status_bar.addPermanentWidget(self.label_acq_status)
    
    def apply_dark_theme(self):
        """应用深色主题"""
        self.setStyleSheet("""
            QMainWindow { background-color: #0f3460; }
            QWidget { color: white; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #16213e;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #16213e;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #e94560;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff6b6b; }
            QPushButton:disabled { background-color: #555; }
            QDoubleSpinBox, QSpinBox, QComboBox {
                padding: 5px;
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #16213e;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #1a1a2e;
                color: #ecf0f1;
                border: 1px solid #16213e;
                font-family: Consolas, monospace;
            }
            QTableWidget {
                background-color: #1a1a2e;
                color: white;
                gridline-color: #16213e;
            }
            QHeaderView::section {
                background-color: #16213e;
                color: white;
                padding: 5px;
            }
            QToolBar {
                background-color: #16213e;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
            QToolBar QToolButton {
                background-color: transparent;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
            }
            QToolBar QToolButton:hover {
                background-color: #e94560;
            }
            QStatusBar {
                background-color: #16213e;
            }
            QCheckBox { color: white; }
        """)
    
    # ========== 事件处理 ==========
    
    def connect_all_instruments(self):
        """连接所有仪器"""
        self.temp_ctrl.connect()
        self.power.connect()
        self.dmm.connect()
        
        self.update_status_indicators()
        self.log("所有仪器已连接")
    
    def disconnect_all_instruments(self):
        """断开所有仪器"""
        self.temp_ctrl.disconnect()
        self.power.disconnect()
        self.dmm.disconnect()
        
        self.update_status_indicators()
        self.log("所有仪器已断开")
    
    def update_status_indicators(self):
        """更新状态指示器"""
        color_on = "color: #2ecc71;"
        color_off = "color: #e74c3c;"
        
        self.label_temp_status.setStyleSheet(
            color_on if self.temp_ctrl.connected else color_off
        )
        self.label_power_status.setStyleSheet(
            color_on if self.power.connected else color_off
        )
        self.label_dmm_status.setStyleSheet(
            color_on if self.dmm.connected else color_off
        )
    
    def start_acquisition(self):
        """开始采集"""
        self.daq_thread.interval = self.spin_interval.value()
        self.daq_thread.start()
        
        self.action_start.setEnabled(False)
        self.action_stop.setEnabled(True)
        self.label_acq_status.setText("采集: 运行中")
        self.label_acq_status.setStyleSheet("color: #2ecc71;")
        
        self.log("开始数据采集")
    
    def stop_acquisition(self):
        """停止采集"""
        self.daq_thread.stop()
        
        self.action_start.setEnabled(True)
        self.action_stop.setEnabled(False)
        self.label_acq_status.setText("采集: 停止")
        self.label_acq_status.setStyleSheet("color: #e74c3c;")
        
        self.log("停止数据采集")
    
    def on_data_received(self, data: dict):
        """接收数据"""
        # 更新显示
        self.label_temp.setText(f"{data['temperature']:.1f} K")
        self.label_current.setText(f"{data['power_current']:.4f} A")
        self.label_dmm_voltage.setText(f"{data['voltage']:.4f} V")
        self.label_dmm_resistance.setText(f"{data['resistance']:.1f} Ω")
        
        # 更新图形
        self.plot_temp.update_data(data['temperature'])
        self.plot_voltage.update_data(data['voltage'])
        self.plot_resistance.update_data(data['resistance'])
        
        # 记录数据
        if self.is_recording:
            self.recorded_data.append(data)
            self.label_record_count.setText(f"记录: {len(self.recorded_data)} 条")
            
            # 更新表格（最近10条）
            if len(self.recorded_data) % 10 == 0:
                self.update_data_table()
    
    def update_data_table(self):
        """更新数据表格"""
        self.data_table.setRowCount(min(10, len(self.recorded_data)))
        
        for i, data in enumerate(self.recorded_data[-10:]):
            self.data_table.setItem(i, 0, QTableWidgetItem(
                data['timestamp'].strftime('%H:%M:%S')
            ))
            self.data_table.setItem(i, 1, QTableWidgetItem(f"{data['temperature']:.2f}"))
            self.data_table.setItem(i, 2, QTableWidgetItem(f"{data['voltage']:.4f}"))
            self.data_table.setItem(i, 3, QTableWidgetItem(f"{data['resistance']:.1f}"))
            self.data_table.setItem(i, 4, QTableWidgetItem(f"{data['power_voltage']:.2f}"))
            self.data_table.setItem(i, 5, QTableWidgetItem(f"{data['power_current']:.4f}"))
    
    def set_target_temperature(self):
        """设置目标温度"""
        temp = self.spin_target_temp.value()
        self.temp_ctrl.set_target(temp)
        self.log(f"目标温度设置为 {temp:.1f} K")
    
    def set_voltage(self, value: float):
        """设置电压"""
        self.power.set_voltage(value)
    
    def toggle_output(self, state: int):
        """切换输出"""
        self.power.set_output(state == Qt.CheckState.Checked.value)
    
    def toggle_recording(self, checked: bool):
        """切换记录"""
        self.is_recording = checked
        if checked:
            self.recorded_data = []
            self.log("开始记录数据")
        else:
            self.log(f"停止记录，共 {len(self.recorded_data)} 条")
    
    def export_data(self):
        """导出数据"""
        if not self.recorded_data:
            QMessageBox.warning(self, "警告", "没有可导出的数据")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出数据",
            f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV文件 (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Time,Temperature(K),Voltage(V),Resistance(Ohm),"
                           "PowerVoltage(V),PowerCurrent(A)\n")
                    for d in self.recorded_data:
                        f.write(f"{d['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')},"
                               f"{d['temperature']:.4f},{d['voltage']:.6f},"
                               f"{d['resistance']:.2f},{d['power_voltage']:.4f},"
                               f"{d['power_current']:.6f}\n")
                
                self.log(f"数据已导出到 {filename}")
                QMessageBox.information(self, "成功", f"数据已导出:\n{filename}")
                
            except Exception as e:
                logger.error(f"导出失败: {e}")
                QMessageBox.critical(self, "错误", str(e))
    
    def log(self, message: str):
        """添加日志"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")
        logger.info(message)
    
    def closeEvent(self, event):
        """关闭窗口"""
        if self.daq_thread.isRunning():
            self.daq_thread.stop()
        
        self.disconnect_all_instruments()
        logger.info("应用程序已关闭")
        event.accept()


# ============================================================
# 主函数
# ============================================================

def main():
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("低温测量系统")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Physics Lab")
    
    # 创建主窗口
    window = CryoMeasurementSystem()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

