"""
示例程序：多子图与联动控制
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示多子图布局和联动控制：
    - 创建多子图布局
    - GridSpec自定义布局
    - 时域-频域联动分析
    - 多参数同时可视化

运行方式：
    python multi_subplot.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDoubleSpinBox, QSpinBox, QSlider,
    QGroupBox, QFormLayout, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec


class MultiSubplotCanvas(FigureCanvas):
    """多子图画布"""
    
    def __init__(self, parent=None, width=12, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)


class SignalAnalyzer(QMainWindow):
    """
    信号分析器
    
    时域-频域联动分析：展示信号的时域波形、频谱、相位和功率谱
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plots()
    
    def init_ui(self):
        self.setWindowTitle("信号分析器 - 时域/频域联动")
        self.setMinimumSize(1100, 750)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 图形区域
        plot_layout = QVBoxLayout()
        
        # 创建多子图画布
        self.canvas = MultiSubplotCanvas(self, width=12, height=8, dpi=100)
        
        # 创建2x2子图
        self.axes = self.canvas.fig.subplots(2, 2)
        self.ax_time = self.axes[0, 0]
        self.ax_spectrum = self.axes[0, 1]
        self.ax_phase = self.axes[1, 0]
        self.ax_power = self.axes[1, 1]
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
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
            QDoubleSpinBox, QSpinBox, QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(260)
        layout = QVBoxLayout(panel)
        
        title = QLabel("📊 信号参数")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 基波参数
        fund_group = QGroupBox("基波")
        form1 = QFormLayout()
        
        self.spin_f1 = QDoubleSpinBox()
        self.spin_f1.setRange(1, 50)
        self.spin_f1.setValue(5)
        self.spin_f1.setSuffix(" Hz")
        self.spin_f1.valueChanged.connect(self.update_plots)
        form1.addRow("频率 f₁:", self.spin_f1)
        
        self.spin_a1 = QDoubleSpinBox()
        self.spin_a1.setRange(0, 5)
        self.spin_a1.setValue(1)
        self.spin_a1.valueChanged.connect(self.update_plots)
        form1.addRow("振幅 A₁:", self.spin_a1)
        
        fund_group.setLayout(form1)
        layout.addWidget(fund_group)
        
        # 二次谐波
        harm_group = QGroupBox("二次谐波")
        form2 = QFormLayout()
        
        self.check_harmonic = QCheckBox("启用")
        self.check_harmonic.setChecked(True)
        self.check_harmonic.stateChanged.connect(self.update_plots)
        form2.addRow("", self.check_harmonic)
        
        self.spin_a2 = QDoubleSpinBox()
        self.spin_a2.setRange(0, 2)
        self.spin_a2.setValue(0.5)
        self.spin_a2.valueChanged.connect(self.update_plots)
        form2.addRow("振幅 A₂:", self.spin_a2)
        
        harm_group.setLayout(form2)
        layout.addWidget(harm_group)
        
        # 噪声
        noise_group = QGroupBox("噪声")
        form3 = QFormLayout()
        
        self.spin_noise = QDoubleSpinBox()
        self.spin_noise.setRange(0, 1)
        self.spin_noise.setValue(0.1)
        self.spin_noise.setSingleStep(0.05)
        self.spin_noise.valueChanged.connect(self.update_plots)
        form3.addRow("噪声幅度:", self.spin_noise)
        
        noise_group.setLayout(form3)
        layout.addWidget(noise_group)
        
        # 采样参数
        sample_group = QGroupBox("采样参数")
        form4 = QFormLayout()
        
        self.spin_fs = QSpinBox()
        self.spin_fs.setRange(100, 10000)
        self.spin_fs.setValue(1000)
        self.spin_fs.setSuffix(" Hz")
        self.spin_fs.valueChanged.connect(self.update_plots)
        form4.addRow("采样率:", self.spin_fs)
        
        self.spin_duration = QDoubleSpinBox()
        self.spin_duration.setRange(0.1, 5)
        self.spin_duration.setValue(1)
        self.spin_duration.setSuffix(" s")
        self.spin_duration.valueChanged.connect(self.update_plots)
        form4.addRow("时长:", self.spin_duration)
        
        sample_group.setLayout(form4)
        layout.addWidget(sample_group)
        
        layout.addStretch()
        
        # 更新按钮
        btn_update = QPushButton("🔄 重新生成")
        btn_update.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_update.clicked.connect(self.update_plots)
        layout.addWidget(btn_update)
        
        return panel
    
    def update_plots(self):
        """更新所有子图"""
        # 获取参数
        f1 = self.spin_f1.value()
        a1 = self.spin_a1.value()
        a2 = self.spin_a2.value() if self.check_harmonic.isChecked() else 0
        noise_amp = self.spin_noise.value()
        fs = self.spin_fs.value()
        duration = self.spin_duration.value()
        
        # 生成信号
        t = np.linspace(0, duration, int(fs * duration))
        signal = a1 * np.sin(2 * np.pi * f1 * t)
        
        if a2 > 0:
            signal += a2 * np.sin(2 * np.pi * 2 * f1 * t)  # 二次谐波
        
        signal += np.random.randn(len(t)) * noise_amp
        
        # 计算FFT
        n = len(t)
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(n, 1/fs)
        
        # 只取正频率部分
        positive_mask = freqs >= 0
        freqs_pos = freqs[positive_mask]
        fft_pos = fft[positive_mask]
        amplitude = np.abs(fft_pos) * 2 / n
        phase = np.angle(fft_pos)
        power = amplitude ** 2
        
        # ===== 子图1: 时域波形 =====
        self.ax_time.clear()
        self.ax_time.plot(t, signal, 'b-', linewidth=0.8)
        self.ax_time.set_xlabel('时间 (s)')
        self.ax_time.set_ylabel('振幅')
        self.ax_time.set_title('时域波形')
        self.ax_time.grid(True, alpha=0.3)
        self.ax_time.set_xlim(0, min(0.5, duration))  # 只显示前0.5秒
        
        # ===== 子图2: 幅度谱 =====
        self.ax_spectrum.clear()
        self.ax_spectrum.plot(freqs_pos, amplitude, 'r-', linewidth=1)
        self.ax_spectrum.set_xlabel('频率 (Hz)')
        self.ax_spectrum.set_ylabel('幅度')
        self.ax_spectrum.set_title('幅度谱')
        self.ax_spectrum.grid(True, alpha=0.3)
        self.ax_spectrum.set_xlim(0, min(100, fs/2))
        
        # 标注峰值
        peak_freq = freqs_pos[np.argmax(amplitude)]
        peak_amp = np.max(amplitude)
        self.ax_spectrum.annotate(f'{peak_freq:.1f} Hz', 
                                   xy=(peak_freq, peak_amp),
                                   xytext=(peak_freq + 10, peak_amp),
                                   fontsize=9,
                                   arrowprops=dict(arrowstyle='->', color='gray'))
        
        # ===== 子图3: 相位谱 =====
        self.ax_phase.clear()
        # 只显示有意义的相位（振幅大于阈值的部分）
        threshold = 0.01
        phase_display = np.where(amplitude > threshold, phase, np.nan)
        self.ax_phase.plot(freqs_pos, np.degrees(phase_display), 'g-', linewidth=1)
        self.ax_phase.set_xlabel('频率 (Hz)')
        self.ax_phase.set_ylabel('相位 (度)')
        self.ax_phase.set_title('相位谱')
        self.ax_phase.grid(True, alpha=0.3)
        self.ax_phase.set_xlim(0, min(100, fs/2))
        self.ax_phase.set_ylim(-180, 180)
        
        # ===== 子图4: 功率谱 (对数) =====
        self.ax_power.clear()
        self.ax_power.semilogy(freqs_pos, power + 1e-10, 'm-', linewidth=1)
        self.ax_power.set_xlabel('频率 (Hz)')
        self.ax_power.set_ylabel('功率 (对数)')
        self.ax_power.set_title('功率谱')
        self.ax_power.grid(True, alpha=0.3)
        self.ax_power.set_xlim(0, min(100, fs/2))
        
        # 调整布局
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class GridSpecDemo(QMainWindow):
    """
    GridSpec自定义布局演示
    
    展示如何使用GridSpec创建不规则的子图布局
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plots()
    
    def init_ui(self):
        self.setWindowTitle("GridSpec 自定义布局 - 相空间分析")
        self.setMinimumSize(1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 控制面板
        panel = QWidget()
        panel.setFixedWidth(220)
        panel_layout = QVBoxLayout(panel)
        
        title = QLabel("🎯 相空间参数")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        panel_layout.addWidget(title)
        
        param_group = QGroupBox("振子参数")
        form = QFormLayout()
        
        self.spin_omega = QDoubleSpinBox()
        self.spin_omega.setRange(0.5, 5)
        self.spin_omega.setValue(1)
        self.spin_omega.setSuffix(" rad/s")
        self.spin_omega.valueChanged.connect(self.update_plots)
        form.addRow("角频率 ω:", self.spin_omega)
        
        self.spin_gamma = QDoubleSpinBox()
        self.spin_gamma.setRange(0, 1)
        self.spin_gamma.setValue(0.1)
        self.spin_gamma.setSingleStep(0.05)
        self.spin_gamma.valueChanged.connect(self.update_plots)
        form.addRow("阻尼 γ:", self.spin_gamma)
        
        self.spin_x0 = QDoubleSpinBox()
        self.spin_x0.setRange(-5, 5)
        self.spin_x0.setValue(2)
        self.spin_x0.valueChanged.connect(self.update_plots)
        form.addRow("初始位置:", self.spin_x0)
        
        self.spin_v0 = QDoubleSpinBox()
        self.spin_v0.setRange(-5, 5)
        self.spin_v0.setValue(0)
        self.spin_v0.valueChanged.connect(self.update_plots)
        form.addRow("初始速度:", self.spin_v0)
        
        param_group.setLayout(form)
        panel_layout.addWidget(param_group)
        
        panel_layout.addStretch()
        main_layout.addWidget(panel)
        
        # 创建画布
        self.canvas = MultiSubplotCanvas(self, width=10, height=7, dpi=100)
        
        # 使用GridSpec创建不规则布局
        gs = GridSpec(3, 3, figure=self.canvas.fig)
        
        # 主图（相空间）: 左侧2/3宽度，占2行
        self.ax_phase = self.canvas.fig.add_subplot(gs[0:2, 0:2])
        
        # 右上: x(t)
        self.ax_xt = self.canvas.fig.add_subplot(gs[0, 2])
        
        # 右中: v(t)
        self.ax_vt = self.canvas.fig.add_subplot(gs[1, 2])
        
        # 底部: 能量
        self.ax_energy = self.canvas.fig.add_subplot(gs[2, :])
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        main_layout.addLayout(plot_layout, stretch=1)
        
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
            }
        """)
    
    def update_plots(self):
        """更新所有图形"""
        omega = self.spin_omega.value()
        gamma = self.spin_gamma.value()
        x0 = self.spin_x0.value()
        v0 = self.spin_v0.value()
        
        # 模拟阻尼谐振子
        t = np.linspace(0, 30, 1000)
        
        if gamma < omega:
            # 欠阻尼
            omega_d = np.sqrt(omega**2 - gamma**2)
            A = np.sqrt(x0**2 + ((v0 + gamma*x0)/omega_d)**2)
            phi = np.arctan2(omega_d * x0, v0 + gamma * x0)
            
            x = A * np.exp(-gamma * t) * np.cos(omega_d * t - phi)
            v = -A * np.exp(-gamma * t) * (gamma * np.cos(omega_d * t - phi) + 
                                            omega_d * np.sin(omega_d * t - phi))
        else:
            # 简单处理其他情况
            x = x0 * np.exp(-gamma * t) * np.cos(omega * t)
            v = -x0 * np.exp(-gamma * t) * (gamma * np.cos(omega * t) + 
                                             omega * np.sin(omega * t))
        
        # 计算能量
        E_kinetic = 0.5 * v**2
        E_potential = 0.5 * omega**2 * x**2
        E_total = E_kinetic + E_potential
        
        # ===== 主图: 相空间 =====
        self.ax_phase.clear()
        self.ax_phase.plot(x, v, 'b-', linewidth=1.5, label='相轨迹')
        self.ax_phase.plot(x[0], v[0], 'go', markersize=10, label='起点')
        self.ax_phase.plot(x[-1], v[-1], 'r^', markersize=10, label='终点')
        self.ax_phase.set_xlabel('位置 x', fontsize=12)
        self.ax_phase.set_ylabel('速度 v', fontsize=12)
        self.ax_phase.set_title('相空间轨迹', fontsize=14, fontweight='bold')
        self.ax_phase.legend(loc='upper right')
        self.ax_phase.grid(True, alpha=0.3)
        self.ax_phase.set_aspect('equal', adjustable='box')
        self.ax_phase.axhline(y=0, color='gray', linewidth=0.5)
        self.ax_phase.axvline(x=0, color='gray', linewidth=0.5)
        
        # ===== 右上: x(t) =====
        self.ax_xt.clear()
        self.ax_xt.plot(t, x, 'b-', linewidth=1)
        self.ax_xt.set_xlabel('t')
        self.ax_xt.set_ylabel('x')
        self.ax_xt.set_title('位置 x(t)')
        self.ax_xt.grid(True, alpha=0.3)
        
        # ===== 右中: v(t) =====
        self.ax_vt.clear()
        self.ax_vt.plot(t, v, 'r-', linewidth=1)
        self.ax_vt.set_xlabel('t')
        self.ax_vt.set_ylabel('v')
        self.ax_vt.set_title('速度 v(t)')
        self.ax_vt.grid(True, alpha=0.3)
        
        # ===== 底部: 能量 =====
        self.ax_energy.clear()
        self.ax_energy.fill_between(t, 0, E_kinetic, alpha=0.5, label='动能')
        self.ax_energy.fill_between(t, E_kinetic, E_kinetic + E_potential, alpha=0.5, label='势能')
        self.ax_energy.plot(t, E_total, 'k-', linewidth=2, label='总能量')
        self.ax_energy.set_xlabel('时间 t', fontsize=12)
        self.ax_energy.set_ylabel('能量', fontsize=12)
        self.ax_energy.set_title('能量随时间变化', fontsize=14)
        self.ax_energy.legend(loc='upper right')
        self.ax_energy.grid(True, alpha=0.3)
        self.ax_energy.set_xlim(0, 30)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    
    # 信号分析器
    analyzer = SignalAnalyzer()
    analyzer.show()
    
    # GridSpec演示
    gridspec = GridSpecDemo()
    gridspec.move(100, 50)
    gridspec.show()
    
    print("=" * 50)
    print("多子图与联动控制演示")
    print("=" * 50)
    print("示例:")
    print("  1. 信号分析器 - 时域/频域4子图联动")
    print("  2. GridSpec - 自定义布局相空间分析")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

