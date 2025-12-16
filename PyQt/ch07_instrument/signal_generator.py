"""
示例程序：信号发生器控制
所属章节：第七章 - 仪器控制界面实战

功能说明：
    模拟信号发生器控制界面：
    - 多种波形类型
    - 频率、幅度、偏置调节
    - 实时波形预览
    - 多通道输出

运行方式：
    python signal_generator.py
"""

import sys
import numpy as np
from scipy import signal as sig
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDoubleSpinBox, QGroupBox, QFormLayout,
    QComboBox, QSlider, QCheckBox, QTabWidget, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self):
        self.fig = Figure(figsize=(10, 5), dpi=100)
        super().__init__(self.fig)


class ChannelWidget(QWidget):
    """单通道控制组件"""
    
    def __init__(self, channel_name: str, color: str):
        super().__init__()
        self.channel_name = channel_name
        self.color = color
        self.output_enabled = False
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 输出开关
        header = QHBoxLayout()
        
        self.check_output = QCheckBox(f"{self.channel_name} 输出")
        self.check_output.setStyleSheet(f"color: {self.color}; font-weight: bold;")
        header.addWidget(self.check_output)
        
        self.label_status = QLabel("OFF")
        self.label_status.setStyleSheet("color: #e74c3c;")
        header.addWidget(self.label_status)
        
        header.addStretch()
        layout.addLayout(header)
        
        # 波形类型
        form = QFormLayout()
        
        self.combo_waveform = QComboBox()
        self.combo_waveform.addItems(["正弦波", "方波", "三角波", "锯齿波", "噪声"])
        form.addRow("波形:", self.combo_waveform)
        
        # 频率
        freq_layout = QHBoxLayout()
        self.spin_freq = QDoubleSpinBox()
        self.spin_freq.setRange(0.1, 10000)
        self.spin_freq.setValue(100)
        self.spin_freq.setSuffix(" Hz")
        freq_layout.addWidget(self.spin_freq)
        
        self.combo_freq_unit = QComboBox()
        self.combo_freq_unit.addItems(["Hz", "kHz", "MHz"])
        self.combo_freq_unit.currentIndexChanged.connect(self.update_freq_range)
        freq_layout.addWidget(self.combo_freq_unit)
        form.addRow("频率:", freq_layout)
        
        # 幅度
        self.spin_amplitude = QDoubleSpinBox()
        self.spin_amplitude.setRange(0, 10)
        self.spin_amplitude.setValue(1.0)
        self.spin_amplitude.setSuffix(" Vpp")
        self.spin_amplitude.setSingleStep(0.1)
        form.addRow("幅度:", self.spin_amplitude)
        
        # 偏置
        self.spin_offset = QDoubleSpinBox()
        self.spin_offset.setRange(-10, 10)
        self.spin_offset.setValue(0)
        self.spin_offset.setSuffix(" V")
        self.spin_offset.setSingleStep(0.1)
        form.addRow("偏置:", self.spin_offset)
        
        # 占空比（方波）
        self.spin_duty = QSpinBox()
        self.spin_duty.setRange(1, 99)
        self.spin_duty.setValue(50)
        self.spin_duty.setSuffix(" %")
        form.addRow("占空比:", self.spin_duty)
        
        # 相位
        self.spin_phase = QDoubleSpinBox()
        self.spin_phase.setRange(0, 360)
        self.spin_phase.setValue(0)
        self.spin_phase.setSuffix(" °")
        form.addRow("相位:", self.spin_phase)
        
        layout.addLayout(form)
        
        # 连接信号
        self.check_output.stateChanged.connect(self.toggle_output)
        self.combo_waveform.currentIndexChanged.connect(self.on_waveform_changed)
        
        self.on_waveform_changed()
    
    def update_freq_range(self):
        """更新频率范围"""
        unit = self.combo_freq_unit.currentText()
        if unit == "Hz":
            self.spin_freq.setRange(0.1, 10000)
            self.spin_freq.setSuffix(" Hz")
        elif unit == "kHz":
            self.spin_freq.setRange(0.001, 100)
            self.spin_freq.setSuffix(" kHz")
        else:
            self.spin_freq.setRange(0.001, 10)
            self.spin_freq.setSuffix(" MHz")
    
    def toggle_output(self, state):
        """切换输出状态"""
        self.output_enabled = state == Qt.CheckState.Checked.value
        if self.output_enabled:
            self.label_status.setText("ON")
            self.label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.label_status.setText("OFF")
            self.label_status.setStyleSheet("color: #e74c3c;")
    
    def on_waveform_changed(self):
        """波形类型改变"""
        is_square = self.combo_waveform.currentText() == "方波"
        self.spin_duty.setEnabled(is_square)
    
    def get_frequency(self) -> float:
        """获取频率（Hz）"""
        freq = self.spin_freq.value()
        unit = self.combo_freq_unit.currentText()
        if unit == "kHz":
            freq *= 1000
        elif unit == "MHz":
            freq *= 1000000
        return freq
    
    def get_parameters(self) -> dict:
        """获取所有参数"""
        return {
            'waveform': self.combo_waveform.currentText(),
            'frequency': self.get_frequency(),
            'amplitude': self.spin_amplitude.value(),
            'offset': self.spin_offset.value(),
            'duty': self.spin_duty.value(),
            'phase': self.spin_phase.value(),
            'enabled': self.output_enabled,
            'color': self.color
        }


class SignalGenerator(QMainWindow):
    """信号发生器控制界面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # 波形更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_waveform)
        self.update_timer.start(100)
    
    def init_ui(self):
        self.setWindowTitle("信号发生器")
        self.setMinimumSize(1100, 750)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧通道控制
        left_panel = QWidget()
        left_panel.setFixedWidth(320)
        left_layout = QVBoxLayout(left_panel)
        
        # 通道标签页
        channel_tabs = QTabWidget()
        
        self.channel1 = ChannelWidget("CH1", "#e74c3c")
        self.channel2 = ChannelWidget("CH2", "#3498db")
        
        channel_tabs.addTab(self.channel1, "通道 1")
        channel_tabs.addTab(self.channel2, "通道 2")
        
        left_layout.addWidget(channel_tabs)
        
        # 同步设置
        sync_group = QGroupBox("同步设置")
        sync_layout = QVBoxLayout()
        
        self.check_sync = QCheckBox("CH2 同步到 CH1")
        sync_layout.addWidget(self.check_sync)
        
        phase_layout = QHBoxLayout()
        phase_layout.addWidget(QLabel("相位差:"))
        self.spin_phase_diff = QSpinBox()
        self.spin_phase_diff.setRange(0, 360)
        self.spin_phase_diff.setValue(90)
        self.spin_phase_diff.setSuffix(" °")
        phase_layout.addWidget(self.spin_phase_diff)
        sync_layout.addLayout(phase_layout)
        
        sync_group.setLayout(sync_layout)
        left_layout.addWidget(sync_group)
        
        # 调制设置
        mod_group = QGroupBox("调制 (AM)")
        mod_layout = QFormLayout()
        
        self.check_am = QCheckBox("启用AM调制")
        mod_layout.addRow("", self.check_am)
        
        self.spin_mod_freq = QDoubleSpinBox()
        self.spin_mod_freq.setRange(0.1, 1000)
        self.spin_mod_freq.setValue(10)
        self.spin_mod_freq.setSuffix(" Hz")
        mod_layout.addRow("调制频率:", self.spin_mod_freq)
        
        self.spin_mod_depth = QSpinBox()
        self.spin_mod_depth.setRange(0, 100)
        self.spin_mod_depth.setValue(50)
        self.spin_mod_depth.setSuffix(" %")
        mod_layout.addRow("调制深度:", self.spin_mod_depth)
        
        mod_group.setLayout(mod_layout)
        left_layout.addWidget(mod_group)
        
        left_layout.addStretch()
        
        # 全局控制
        btn_all_on = QPushButton("全部输出 ON")
        btn_all_on.clicked.connect(self.all_output_on)
        left_layout.addWidget(btn_all_on)
        
        btn_all_off = QPushButton("全部输出 OFF")
        btn_all_off.setStyleSheet("background-color: #e74c3c;")
        btn_all_off.clicked.connect(self.all_output_off)
        left_layout.addWidget(btn_all_off)
        
        main_layout.addWidget(left_panel)
        
        # 右侧波形显示
        right_layout = QVBoxLayout()
        
        # 时域波形
        time_group = QGroupBox("时域波形")
        time_layout = QVBoxLayout()
        
        self.canvas_time = MplCanvas()
        time_layout.addWidget(self.canvas_time)
        
        time_group.setLayout(time_layout)
        right_layout.addWidget(time_group)
        
        # 频谱
        freq_group = QGroupBox("频谱")
        freq_layout = QVBoxLayout()
        
        self.canvas_freq = MplCanvas()
        freq_layout.addWidget(self.canvas_freq)
        
        freq_group.setLayout(freq_layout)
        right_layout.addWidget(freq_group)
        
        main_layout.addLayout(right_layout)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #16213e;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #0f3460;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #e94560;
            }
            QLabel { color: white; }
            QPushButton {
                padding: 10px;
                background-color: #e94560;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff6b6b; }
            QComboBox, QDoubleSpinBox, QSpinBox {
                padding: 5px;
                background-color: #16213e;
                color: white;
                border: 1px solid #0f3460;
                border-radius: 4px;
            }
            QCheckBox { color: white; }
            QTabWidget::pane {
                border: 2px solid #16213e;
                background-color: #0f3460;
            }
            QTabBar::tab {
                background-color: #16213e;
                color: white;
                padding: 8px 15px;
            }
            QTabBar::tab:selected {
                background-color: #e94560;
            }
        """)
    
    def generate_waveform(self, params: dict, t: np.ndarray) -> np.ndarray:
        """生成波形"""
        waveform = params['waveform']
        freq = params['frequency']
        amp = params['amplitude'] / 2  # Vpp to amplitude
        offset = params['offset']
        duty = params['duty'] / 100
        phase = np.radians(params['phase'])
        
        # 归一化时间以适应显示
        display_freq = min(freq, 1000)  # 限制显示频率
        
        if waveform == "正弦波":
            y = amp * np.sin(2 * np.pi * display_freq * t + phase) + offset
        elif waveform == "方波":
            y = amp * sig.square(2 * np.pi * display_freq * t + phase, duty) + offset
        elif waveform == "三角波":
            y = amp * sig.sawtooth(2 * np.pi * display_freq * t + phase, 0.5) + offset
        elif waveform == "锯齿波":
            y = amp * sig.sawtooth(2 * np.pi * display_freq * t + phase) + offset
        elif waveform == "噪声":
            y = amp * np.random.randn(len(t)) + offset
        else:
            y = np.zeros_like(t)
        
        # AM调制
        if self.check_am.isChecked() and params == self.channel1.get_parameters():
            mod_freq = self.spin_mod_freq.value()
            mod_depth = self.spin_mod_depth.value() / 100
            modulation = 1 + mod_depth * np.sin(2 * np.pi * mod_freq * t)
            y = (y - offset) * modulation + offset
        
        return y
    
    def update_waveform(self):
        """更新波形显示"""
        # 时间轴
        t = np.linspace(0, 0.02, 2000)  # 20ms, 2000点
        
        # 清空画布
        self.canvas_time.fig.clear()
        ax_time = self.canvas_time.fig.add_subplot(111)
        ax_time.set_facecolor('#0a0a1a')
        
        self.canvas_freq.fig.clear()
        ax_freq = self.canvas_freq.fig.add_subplot(111)
        ax_freq.set_facecolor('#0a0a1a')
        
        # 通道1
        params1 = self.channel1.get_parameters()
        if params1['enabled']:
            y1 = self.generate_waveform(params1, t)
            ax_time.plot(t * 1000, y1, color=params1['color'], 
                        linewidth=1, label='CH1')
            
            # FFT
            fft = np.abs(np.fft.fft(y1))[:len(y1)//2]
            freqs = np.fft.fftfreq(len(y1), t[1]-t[0])[:len(y1)//2]
            ax_freq.plot(freqs[:500], fft[:500], color=params1['color'], 
                        linewidth=1, label='CH1')
        
        # 通道2
        params2 = self.channel2.get_parameters()
        if self.check_sync.isChecked():
            params2['frequency'] = params1['frequency']
            params2['phase'] = params1['phase'] + self.spin_phase_diff.value()
        
        if params2['enabled']:
            y2 = self.generate_waveform(params2, t)
            ax_time.plot(t * 1000, y2, color=params2['color'], 
                        linewidth=1, label='CH2')
            
            # FFT
            fft = np.abs(np.fft.fft(y2))[:len(y2)//2]
            freqs = np.fft.fftfreq(len(y2), t[1]-t[0])[:len(y2)//2]
            ax_freq.plot(freqs[:500], fft[:500], color=params2['color'], 
                        linewidth=1, label='CH2')
        
        # 时域图设置
        ax_time.set_xlabel('时间 (ms)', color='white')
        ax_time.set_ylabel('电压 (V)', color='white')
        ax_time.set_title('时域波形', color='white')
        ax_time.tick_params(colors='white')
        ax_time.grid(True, alpha=0.3, color='gray')
        ax_time.legend(loc='upper right')
        ax_time.set_xlim(0, 20)
        
        # 频域图设置
        ax_freq.set_xlabel('频率 (Hz)', color='white')
        ax_freq.set_ylabel('幅度', color='white')
        ax_freq.set_title('频谱', color='white')
        ax_freq.tick_params(colors='white')
        ax_freq.grid(True, alpha=0.3, color='gray')
        ax_freq.legend(loc='upper right')
        
        self.canvas_time.fig.tight_layout()
        self.canvas_freq.fig.tight_layout()
        
        self.canvas_time.draw()
        self.canvas_freq.draw()
    
    def all_output_on(self):
        """全部输出ON"""
        self.channel1.check_output.setChecked(True)
        self.channel2.check_output.setChecked(True)
    
    def all_output_off(self):
        """全部输出OFF"""
        self.channel1.check_output.setChecked(False)
        self.channel2.check_output.setChecked(False)


def main():
    app = QApplication(sys.argv)
    window = SignalGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

