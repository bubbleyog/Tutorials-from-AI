"""
示例程序：信号传递参数
所属章节：第三章 - 信号与槽机制

功能说明：
    演示信号参数传递的各种方式，包括：
    - 单参数和多参数信号
    - 不同数据类型的参数
    - 信号重载
    - 物理实验场景：光谱仪数据采集

运行方式：
    python signal_with_params.py
"""

import sys
import random
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QPushButton,
    QDoubleSpinBox, QSpinBox, QProgressBar, QTextEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
)
from PyQt6.QtCore import Qt, QObject, QTimer, pyqtSignal


class Spectrometer(QObject):
    """
    光谱仪模拟器
    
    演示使用不同参数类型的自定义信号
    """
    
    # 单参数信号
    scan_started = pyqtSignal(str)                     # 扫描开始(扫描名称)
    scan_progress = pyqtSignal(int)                    # 扫描进度(百分比)
    scan_finished = pyqtSignal(str)                    # 扫描完成(文件名)
    
    # 多参数信号
    data_point = pyqtSignal(float, float)              # 单个数据点(波长, 强度)
    wavelength_range = pyqtSignal(float, float, int)   # 波长范围(起始, 终止, 点数)
    
    # 复杂类型信号
    spectrum_data = pyqtSignal(list, list)             # 完整光谱(波长列表, 强度列表)
    scan_info = pyqtSignal(dict)                       # 扫描信息(字典)
    
    # 错误信号
    error_occurred = pyqtSignal(str, int)              # 错误(消息, 错误码)
    
    def __init__(self):
        super().__init__()
        self._is_scanning = False
        self._current_point = 0
        self._wavelengths = []
        self._intensities = []
        
        # 扫描参数
        self._start_wl = 400.0
        self._end_wl = 700.0
        self._points = 100
        self._scan_name = ""
        
        # 定时器
        self._timer = QTimer()
        self._timer.timeout.connect(self._scan_step)
    
    def set_parameters(self, start: float, end: float, points: int, name: str = "Scan"):
        """设置扫描参数"""
        self._start_wl = start
        self._end_wl = end
        self._points = points
        self._scan_name = name
        
        # 发出波长范围信号
        self.wavelength_range.emit(start, end, points)
    
    def start_scan(self):
        """开始扫描"""
        if self._is_scanning:
            self.error_occurred.emit("扫描正在进行中", 1001)
            return
        
        self._is_scanning = True
        self._current_point = 0
        self._wavelengths = []
        self._intensities = []
        
        # 发出开始信号
        self.scan_started.emit(self._scan_name)
        
        # 发出扫描信息
        self.scan_info.emit({
            "name": self._scan_name,
            "start_wavelength": self._start_wl,
            "end_wavelength": self._end_wl,
            "points": self._points,
            "step": (self._end_wl - self._start_wl) / (self._points - 1)
        })
        
        # 开始定时器
        self._timer.start(50)  # 50ms采集一个点
    
    def stop_scan(self):
        """停止扫描"""
        self._timer.stop()
        self._is_scanning = False
        self.error_occurred.emit("扫描被用户中断", 1002)
    
    def _scan_step(self):
        """扫描步进"""
        if self._current_point >= self._points:
            self._finish_scan()
            return
        
        # 计算当前波长
        wavelength = self._start_wl + (self._end_wl - self._start_wl) * \
                     self._current_point / (self._points - 1)
        
        # 模拟光谱数据（高斯峰）
        intensity = self._simulate_spectrum(wavelength)
        
        self._wavelengths.append(wavelength)
        self._intensities.append(intensity)
        
        # 发出单点数据信号
        self.data_point.emit(wavelength, intensity)
        
        # 发出进度信号
        progress = int((self._current_point + 1) / self._points * 100)
        self.scan_progress.emit(progress)
        
        self._current_point += 1
    
    def _simulate_spectrum(self, wavelength: float) -> float:
        """模拟光谱数据（多个高斯峰叠加）"""
        # 定义几个峰
        peaks = [
            (450, 0.3, 20),   # (中心, 强度, 宽度)
            (520, 0.8, 30),
            (580, 0.5, 25),
            (630, 0.6, 20),
        ]
        
        intensity = 0.05  # 基线
        for center, amp, width in peaks:
            intensity += amp * math.exp(-((wavelength - center) ** 2) / (2 * width ** 2))
        
        # 添加噪声
        intensity += random.gauss(0, 0.02)
        return max(0, intensity)
    
    def _finish_scan(self):
        """完成扫描"""
        self._timer.stop()
        self._is_scanning = False
        
        # 发出完整光谱数据
        self.spectrum_data.emit(self._wavelengths, self._intensities)
        
        # 发出完成信号
        filename = f"{self._scan_name}_{len(self._wavelengths)}pts.csv"
        self.scan_finished.emit(filename)


class SpectrometerUI(QMainWindow):
    """光谱仪控制界面"""
    
    def __init__(self):
        super().__init__()
        self.spectrometer = Spectrometer()
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        self.setWindowTitle("光谱仪控制 - 信号参数传递演示")
        self.setMinimumSize(700, 550)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        
        # 标题
        title = QLabel("📊 UV-Vis 光谱仪模拟器")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # 参数设置
        main_layout.addWidget(self.create_params_group())
        
        # 实时数据显示
        main_layout.addWidget(self.create_display_group())
        
        # 光谱预览
        main_layout.addWidget(self.create_spectrum_group())
        
        # 日志
        main_layout.addWidget(self.create_log_group())
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #8e44ad;
            }
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                color: white;
            }
            QDoubleSpinBox, QSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def create_params_group(self) -> QGroupBox:
        """参数设置组"""
        group = QGroupBox("扫描参数")
        layout = QHBoxLayout()
        
        # 起始波长
        layout.addWidget(QLabel("起始:"))
        self.spin_start = QDoubleSpinBox()
        self.spin_start.setRange(200, 800)
        self.spin_start.setValue(400)
        self.spin_start.setSuffix(" nm")
        layout.addWidget(self.spin_start)
        
        # 终止波长
        layout.addWidget(QLabel("终止:"))
        self.spin_end = QDoubleSpinBox()
        self.spin_end.setRange(200, 800)
        self.spin_end.setValue(700)
        self.spin_end.setSuffix(" nm")
        layout.addWidget(self.spin_end)
        
        # 采样点数
        layout.addWidget(QLabel("点数:"))
        self.spin_points = QSpinBox()
        self.spin_points.setRange(10, 1000)
        self.spin_points.setValue(100)
        layout.addWidget(self.spin_points)
        
        layout.addStretch()
        
        # 控制按钮
        self.btn_start = QPushButton("▶ 开始扫描")
        self.btn_start.setStyleSheet("background-color: #27ae60;")
        self.btn_start.clicked.connect(self.start_scan)
        layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏹ 停止")
        self.btn_stop.setStyleSheet("background-color: #e74c3c;")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.spectrometer.stop_scan)
        layout.addWidget(self.btn_stop)
        
        group.setLayout(layout)
        return group
    
    def create_display_group(self) -> QGroupBox:
        """实时数据显示组"""
        group = QGroupBox("实时数据")
        layout = QGridLayout()
        
        # 当前波长
        layout.addWidget(QLabel("当前波长:"), 0, 0)
        self.label_wavelength = QLabel("-- nm")
        self.label_wavelength.setStyleSheet("font-size: 16px; color: #9b59b6; font-weight: bold;")
        layout.addWidget(self.label_wavelength, 0, 1)
        
        # 当前强度
        layout.addWidget(QLabel("当前强度:"), 0, 2)
        self.label_intensity = QLabel("--")
        self.label_intensity.setStyleSheet("font-size: 16px; color: #3498db; font-weight: bold;")
        layout.addWidget(self.label_intensity, 0, 3)
        
        # 进度条
        layout.addWidget(QLabel("扫描进度:"), 1, 0)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress, 1, 1, 1, 3)
        
        group.setLayout(layout)
        return group
    
    def create_spectrum_group(self) -> QGroupBox:
        """光谱预览组"""
        group = QGroupBox("光谱预览 (ASCII)")
        layout = QVBoxLayout()
        
        self.spectrum_display = QLabel("等待扫描...")
        self.spectrum_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spectrum_display.setStyleSheet("""
            background-color: #1a1a2e;
            color: #00ff88;
            font-family: Consolas, monospace;
            padding: 15px;
            border-radius: 5px;
            font-size: 12px;
        """)
        self.spectrum_display.setMinimumHeight(80)
        layout.addWidget(self.spectrum_display)
        
        group.setLayout(layout)
        return group
    
    def create_log_group(self) -> QGroupBox:
        """日志组"""
        group = QGroupBox("信号日志")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: none;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def connect_signals(self):
        """连接光谱仪信号"""
        # 扫描开始信号 (str)
        self.spectrometer.scan_started.connect(self.on_scan_started)
        
        # 扫描进度信号 (int)
        self.spectrometer.scan_progress.connect(self.on_scan_progress)
        
        # 扫描完成信号 (str)
        self.spectrometer.scan_finished.connect(self.on_scan_finished)
        
        # 单点数据信号 (float, float)
        self.spectrometer.data_point.connect(self.on_data_point)
        
        # 波长范围信号 (float, float, int)
        self.spectrometer.wavelength_range.connect(self.on_wavelength_range)
        
        # 完整光谱信号 (list, list)
        self.spectrometer.spectrum_data.connect(self.on_spectrum_data)
        
        # 扫描信息信号 (dict)
        self.spectrometer.scan_info.connect(self.on_scan_info)
        
        # 错误信号 (str, int)
        self.spectrometer.error_occurred.connect(self.on_error)
    
    # ========== 槽函数 ==========
    
    def on_scan_started(self, name: str):
        """扫描开始槽 - 接收 str 参数"""
        self.log(f"[scan_started(str)] 开始扫描: {name}")
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
    
    def on_scan_progress(self, percent: int):
        """扫描进度槽 - 接收 int 参数"""
        self.progress.setValue(percent)
    
    def on_scan_finished(self, filename: str):
        """扫描完成槽 - 接收 str 参数"""
        self.log(f"[scan_finished(str)] 扫描完成，保存为: {filename}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
    
    def on_data_point(self, wavelength: float, intensity: float):
        """单点数据槽 - 接收 float, float 参数"""
        self.label_wavelength.setText(f"{wavelength:.1f} nm")
        self.label_intensity.setText(f"{intensity:.4f}")
    
    def on_wavelength_range(self, start: float, end: float, points: int):
        """波长范围槽 - 接收 float, float, int 参数"""
        self.log(f"[wavelength_range(float,float,int)] 范围: {start}-{end} nm, {points}点")
    
    def on_spectrum_data(self, wavelengths: list, intensities: list):
        """完整光谱槽 - 接收 list, list 参数"""
        self.log(f"[spectrum_data(list,list)] 收到 {len(wavelengths)} 个数据点")
        
        # 生成ASCII光谱图
        self.display_ascii_spectrum(wavelengths, intensities)
    
    def on_scan_info(self, info: dict):
        """扫描信息槽 - 接收 dict 参数"""
        self.log(f"[scan_info(dict)] 步长: {info['step']:.2f} nm")
    
    def on_error(self, message: str, code: int):
        """错误槽 - 接收 str, int 参数"""
        self.log(f"[error_occurred(str,int)] 错误 {code}: {message}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
    
    # ========== 辅助函数 ==========
    
    def start_scan(self):
        """开始扫描"""
        self.spectrometer.set_parameters(
            self.spin_start.value(),
            self.spin_end.value(),
            self.spin_points.value(),
            "UV-Vis_Scan"
        )
        self.spectrometer.start_scan()
    
    def display_ascii_spectrum(self, wavelengths: list, intensities: list):
        """显示ASCII光谱图"""
        if not intensities:
            return
        
        # 简化为20个柱
        n_bars = 40
        step = max(1, len(intensities) // n_bars)
        
        sampled = intensities[::step][:n_bars]
        max_int = max(sampled) if sampled else 1
        
        # 生成柱状图
        chars = "▁▂▃▄▅▆▇█"
        bars = ""
        for val in sampled:
            idx = int(val / max_int * (len(chars) - 1))
            bars += chars[idx]
        
        wl_start = wavelengths[0] if wavelengths else 0
        wl_end = wavelengths[-1] if wavelengths else 0
        
        display_text = (
            f"强度: {bars}\n"
            f"波长: {wl_start:.0f} nm {'─' * 30} {wl_end:.0f} nm"
        )
        self.spectrum_display.setText(display_text)
    
    def log(self, message: str):
        """添加日志"""
        from datetime import datetime
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time_str}] {message}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SpectrometerUI()
    window.show()
    
    # 打印信号说明
    print("=" * 60)
    print("信号参数传递演示 - 光谱仪模拟器")
    print("=" * 60)
    print("信号定义:")
    print("  - scan_started(str)           : 扫描名称")
    print("  - scan_progress(int)          : 进度百分比")
    print("  - scan_finished(str)          : 文件名")
    print("  - data_point(float, float)    : 波长, 强度")
    print("  - wavelength_range(float, float, int): 起始, 终止, 点数")
    print("  - spectrum_data(list, list)   : 波长列表, 强度列表")
    print("  - scan_info(dict)             : 扫描信息字典")
    print("  - error_occurred(str, int)    : 错误消息, 错误码")
    print("=" * 60)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

