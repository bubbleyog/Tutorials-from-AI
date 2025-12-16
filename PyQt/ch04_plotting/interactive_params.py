"""
示例程序：交互式参数调节器
所属章节：第四章 - Matplotlib科研绑图集成

功能说明：
    演示通过界面控件实时调节物理函数参数：
    - 量子力学：无限深势阱波函数
    - 电磁学：阻尼振荡
    - 热力学：麦克斯韦-玻尔兹曼分布

运行方式：
    python interactive_params.py
"""

import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QSlider,
    QGroupBox, QFormLayout, QTabWidget, QComboBox
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


class QuantumWellVisualizer(QMainWindow):
    """
    量子力学：无限深势阱波函数可视化
    
    演示如何通过滑动条和SpinBox实时调节量子数n和势阱宽度L
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plot()
    
    def init_ui(self):
        self.setWindowTitle("量子力学 - 无限深势阱波函数")
        self.setMinimumSize(900, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧：控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧：图形
        plot_layout = QVBoxLayout()
        
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        
        main_layout.addLayout(plot_layout, stretch=1)
        
        # 样式
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f3f4; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2980b9;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #2c3e50;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #bdc3c7;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(280)
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("⚛️ 波函数参数")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        
        # 量子数n
        n_group = QGroupBox("量子数 n")
        n_layout = QVBoxLayout()
        
        self.slider_n = QSlider(Qt.Orientation.Horizontal)
        self.slider_n.setRange(1, 10)
        self.slider_n.setValue(1)
        self.slider_n.valueChanged.connect(self.update_plot)
        
        self.label_n = QLabel("n = 1")
        self.label_n.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
        self.label_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        n_layout.addWidget(self.label_n)
        n_layout.addWidget(self.slider_n)
        n_group.setLayout(n_layout)
        layout.addWidget(n_group)
        
        # 势阱宽度L
        L_group = QGroupBox("势阱宽度 L")
        L_layout = QFormLayout()
        
        self.spin_L = QDoubleSpinBox()
        self.spin_L.setRange(0.5, 5.0)
        self.spin_L.setValue(1.0)
        self.spin_L.setSingleStep(0.1)
        self.spin_L.setSuffix(" nm")
        self.spin_L.valueChanged.connect(self.update_plot)
        L_layout.addRow("L =", self.spin_L)
        
        L_group.setLayout(L_layout)
        layout.addWidget(L_group)
        
        # 显示选项
        display_group = QGroupBox("显示选项")
        display_layout = QVBoxLayout()
        
        self.combo_display = QComboBox()
        self.combo_display.addItems([
            "波函数 ψ(x)",
            "概率密度 |ψ|²",
            "两者都显示"
        ])
        self.combo_display.setCurrentIndex(2)
        self.combo_display.currentIndexChanged.connect(self.update_plot)
        display_layout.addWidget(self.combo_display)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # 公式
        formula_group = QGroupBox("波函数公式")
        formula_layout = QVBoxLayout()
        
        formula = QLabel(
            "ψₙ(x) = √(2/L) · sin(nπx/L)\n\n"
            "能量本征值:\n"
            "Eₙ = n²π²ℏ²/(2mL²)"
        )
        formula.setStyleSheet("font-size: 12px; color: #2c3e50;")
        formula_layout.addWidget(formula)
        
        # 能量显示
        self.label_energy = QLabel("E₁ = 0.376 eV")
        self.label_energy.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        formula_layout.addWidget(self.label_energy)
        
        formula_group.setLayout(formula_layout)
        layout.addWidget(formula_group)
        
        layout.addStretch()
        
        return panel
    
    def update_plot(self):
        """更新图形"""
        n = self.slider_n.value()
        L = self.spin_L.value()  # nm
        display_mode = self.combo_display.currentIndex()
        
        # 更新标签
        self.label_n.setText(f"n = {n}")
        
        # 计算能量 (使用电子质量)
        hbar = 1.054571817e-34  # J·s
        m_e = 9.1093837015e-31  # kg
        L_m = L * 1e-9  # 转换为米
        E_J = (n**2 * np.pi**2 * hbar**2) / (2 * m_e * L_m**2)
        E_eV = E_J / 1.602176634e-19
        self.label_energy.setText(f"E{n} = {E_eV:.3f} eV")
        
        # 生成波函数
        x = np.linspace(0, L, 500)
        psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
        prob = psi**2
        
        # 绑图
        self.canvas.axes.clear()
        
        if display_mode == 0:  # 只显示波函数
            self.canvas.axes.plot(x, psi, 'b-', linewidth=2, label='ψ(x)')
            self.canvas.axes.fill_between(x, psi, alpha=0.3)
        elif display_mode == 1:  # 只显示概率密度
            self.canvas.axes.plot(x, prob, 'r-', linewidth=2, label='|ψ|²')
            self.canvas.axes.fill_between(x, prob, alpha=0.3, color='red')
        else:  # 两者都显示
            self.canvas.axes.plot(x, psi, 'b-', linewidth=2, label='ψ(x)')
            self.canvas.axes.plot(x, prob, 'r--', linewidth=1.5, label='|ψ|²')
        
        # 绘制势阱边界
        y_max = max(abs(psi).max(), prob.max()) * 1.2
        self.canvas.axes.axvline(x=0, color='black', linewidth=3)
        self.canvas.axes.axvline(x=L, color='black', linewidth=3)
        
        # 标注节点
        if n > 1:
            for i in range(1, n):
                x_node = i * L / n
                self.canvas.axes.axvline(x=x_node, color='gray', linestyle=':', alpha=0.5)
                self.canvas.axes.plot(x_node, 0, 'ko', markersize=6)
        
        self.canvas.axes.set_xlabel('x (nm)', fontsize=12)
        self.canvas.axes.set_ylabel('波函数 / 概率密度', fontsize=12)
        self.canvas.axes.set_title(f'无限深势阱波函数 (n={n}, L={L} nm)', fontsize=14)
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.axes.set_xlim(-0.1, L + 0.1)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class DampedOscillatorVisualizer(QMainWindow):
    """
    电磁学/力学：阻尼振荡可视化
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plot()
    
    def init_ui(self):
        self.setWindowTitle("阻尼振荡 - 参数可视化")
        self.setMinimumSize(900, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 控制面板
        panel = QWidget()
        panel.setFixedWidth(280)
        panel_layout = QVBoxLayout(panel)
        
        title = QLabel("🔄 阻尼振荡参数")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        panel_layout.addWidget(title)
        
        # 参数组
        param_group = QGroupBox("物理参数")
        form = QFormLayout()
        
        # 阻尼系数
        self.slider_gamma = QSlider(Qt.Orientation.Horizontal)
        self.slider_gamma.setRange(0, 100)
        self.slider_gamma.setValue(20)
        self.slider_gamma.valueChanged.connect(self.update_plot)
        self.label_gamma = QLabel("γ = 0.20")
        form.addRow(self.label_gamma, self.slider_gamma)
        
        # 角频率
        self.slider_omega = QSlider(Qt.Orientation.Horizontal)
        self.slider_omega.setRange(10, 100)
        self.slider_omega.setValue(50)
        self.slider_omega.valueChanged.connect(self.update_plot)
        self.label_omega = QLabel("ω₀ = 5.0 rad/s")
        form.addRow(self.label_omega, self.slider_omega)
        
        # 初始振幅
        self.spin_A0 = QDoubleSpinBox()
        self.spin_A0.setRange(0.1, 5.0)
        self.spin_A0.setValue(1.0)
        self.spin_A0.valueChanged.connect(self.update_plot)
        form.addRow("初始振幅 A₀:", self.spin_A0)
        
        param_group.setLayout(form)
        panel_layout.addWidget(param_group)
        
        # 阻尼类型指示
        self.label_damping_type = QLabel("欠阻尼")
        self.label_damping_type.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #27ae60; padding: 10px;"
        )
        self.label_damping_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(self.label_damping_type)
        
        # 公式
        formula_group = QGroupBox("运动方程")
        formula_layout = QVBoxLayout()
        formula = QLabel(
            "x(t) = A₀ e^(-γt) cos(ωt)\n\n"
            "ω = √(ω₀² - γ²)\n\n"
            "阻尼类型:\n"
            "• γ < ω₀: 欠阻尼\n"
            "• γ = ω₀: 临界阻尼\n"
            "• γ > ω₀: 过阻尼"
        )
        formula.setStyleSheet("font-size: 11px;")
        formula_layout.addWidget(formula)
        formula_group.setLayout(formula_layout)
        panel_layout.addWidget(formula_group)
        
        panel_layout.addStretch()
        main_layout.addWidget(panel)
        
        # 图形
        plot_layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        main_layout.addLayout(plot_layout, stretch=1)
        
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
            }
        """)
    
    def update_plot(self):
        """更新图形"""
        gamma = self.slider_gamma.value() / 100  # 0-1
        omega0 = self.slider_omega.value() / 10   # 1-10 rad/s
        A0 = self.spin_A0.value()
        
        # 更新标签
        self.label_gamma.setText(f"γ = {gamma:.2f}")
        self.label_omega.setText(f"ω₀ = {omega0:.1f} rad/s")
        
        t = np.linspace(0, 10, 1000)
        
        self.canvas.axes.clear()
        
        # 判断阻尼类型并计算
        if gamma < omega0:
            # 欠阻尼
            omega = np.sqrt(omega0**2 - gamma**2)
            x = A0 * np.exp(-gamma * t) * np.cos(omega * t)
            envelope = A0 * np.exp(-gamma * t)
            
            self.canvas.axes.plot(t, x, 'b-', linewidth=2, label='x(t)')
            self.canvas.axes.plot(t, envelope, 'r--', linewidth=1, label='包络线')
            self.canvas.axes.plot(t, -envelope, 'r--', linewidth=1)
            
            self.label_damping_type.setText("欠阻尼 (γ < ω₀)")
            self.label_damping_type.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #27ae60; padding: 10px;"
            )
        elif abs(gamma - omega0) < 0.01:
            # 临界阻尼
            x = A0 * (1 + gamma * t) * np.exp(-gamma * t)
            
            self.canvas.axes.plot(t, x, 'g-', linewidth=2, label='x(t) 临界阻尼')
            
            self.label_damping_type.setText("临界阻尼 (γ = ω₀)")
            self.label_damping_type.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #f39c12; padding: 10px;"
            )
        else:
            # 过阻尼
            beta = np.sqrt(gamma**2 - omega0**2)
            x = A0 * np.exp(-gamma * t) * (np.exp(beta * t) + np.exp(-beta * t)) / 2
            
            self.canvas.axes.plot(t, x, 'm-', linewidth=2, label='x(t) 过阻尼')
            
            self.label_damping_type.setText("过阻尼 (γ > ω₀)")
            self.label_damping_type.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #e74c3c; padding: 10px;"
            )
        
        self.canvas.axes.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
        self.canvas.axes.set_xlabel('时间 t (s)', fontsize=12)
        self.canvas.axes.set_ylabel('位移 x', fontsize=12)
        self.canvas.axes.set_title(f'阻尼振荡 (γ={gamma:.2f}, ω₀={omega0:.1f})', fontsize=14)
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.axes.set_xlim(0, 10)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


class MaxwellBoltzmannVisualizer(QMainWindow):
    """
    热力学：麦克斯韦-玻尔兹曼速度分布
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_plot()
    
    def init_ui(self):
        self.setWindowTitle("麦克斯韦-玻尔兹曼速度分布")
        self.setMinimumSize(900, 650)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 控制面板
        panel = QWidget()
        panel.setFixedWidth(280)
        panel_layout = QVBoxLayout(panel)
        
        title = QLabel("🌡️ 分布参数")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        panel_layout.addWidget(title)
        
        # 温度设置
        temp_group = QGroupBox("温度设置")
        temp_form = QFormLayout()
        
        self.spin_T = QDoubleSpinBox()
        self.spin_T.setRange(50, 1000)
        self.spin_T.setValue(300)
        self.spin_T.setSuffix(" K")
        self.spin_T.valueChanged.connect(self.update_plot)
        temp_form.addRow("温度 T:", self.spin_T)
        
        temp_group.setLayout(temp_form)
        panel_layout.addWidget(temp_group)
        
        # 气体选择
        gas_group = QGroupBox("气体类型")
        gas_layout = QVBoxLayout()
        
        self.combo_gas = QComboBox()
        self.combo_gas.addItems([
            "氢气 H₂ (M=2)",
            "氦气 He (M=4)",
            "氮气 N₂ (M=28)",
            "氧气 O₂ (M=32)",
            "氩气 Ar (M=40)",
        ])
        self.combo_gas.currentIndexChanged.connect(self.update_plot)
        gas_layout.addWidget(self.combo_gas)
        
        gas_group.setLayout(gas_layout)
        panel_layout.addWidget(gas_group)
        
        # 统计信息
        stats_group = QGroupBox("统计量")
        stats_layout = QVBoxLayout()
        
        self.label_vp = QLabel("最概然速度: -- m/s")
        self.label_vmean = QLabel("平均速度: -- m/s")
        self.label_vrms = QLabel("方均根速度: -- m/s")
        
        for label in [self.label_vp, self.label_vmean, self.label_vrms]:
            label.setStyleSheet("font-size: 12px; padding: 3px;")
            stats_layout.addWidget(label)
        
        stats_group.setLayout(stats_layout)
        panel_layout.addWidget(stats_group)
        
        # 公式
        formula_group = QGroupBox("分布函数")
        formula_layout = QVBoxLayout()
        formula = QLabel(
            "f(v) = 4π (M/2πRT)^(3/2)\n"
            "       × v² exp(-Mv²/2RT)\n\n"
            "vₚ = √(2RT/M)\n"
            "⟨v⟩ = √(8RT/πM)\n"
            "vᵣₘₛ = √(3RT/M)"
        )
        formula.setStyleSheet("font-size: 11px;")
        formula_layout.addWidget(formula)
        formula_group.setLayout(formula_layout)
        panel_layout.addWidget(formula_group)
        
        panel_layout.addStretch()
        main_layout.addWidget(panel)
        
        # 图形
        plot_layout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        main_layout.addLayout(plot_layout, stretch=1)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e74c3c;
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
    
    def update_plot(self):
        """更新图形"""
        T = self.spin_T.value()  # K
        
        # 分子量映射
        masses = {0: 2, 1: 4, 2: 28, 3: 32, 4: 40}  # g/mol
        M = masses.get(self.combo_gas.currentIndex(), 28)
        
        # 常数
        R = 8.314  # J/(mol·K)
        M_kg = M / 1000  # kg/mol
        
        # 计算特征速度
        v_p = np.sqrt(2 * R * T / M_kg)  # 最概然速度
        v_mean = np.sqrt(8 * R * T / (np.pi * M_kg))  # 平均速度
        v_rms = np.sqrt(3 * R * T / M_kg)  # 方均根速度
        
        # 更新统计信息
        self.label_vp.setText(f"最概然速度 vₚ: {v_p:.1f} m/s")
        self.label_vmean.setText(f"平均速度 ⟨v⟩: {v_mean:.1f} m/s")
        self.label_vrms.setText(f"方均根速度 vᵣₘₛ: {v_rms:.1f} m/s")
        
        # 计算分布函数
        v = np.linspace(0, 3 * v_rms, 500)
        coeff = 4 * np.pi * (M_kg / (2 * np.pi * R * T)) ** 1.5
        f_v = coeff * v**2 * np.exp(-M_kg * v**2 / (2 * R * T))
        
        # 绑图
        self.canvas.axes.clear()
        
        self.canvas.axes.plot(v, f_v * 1000, 'b-', linewidth=2, 
                               label=f'{self.combo_gas.currentText()}')
        self.canvas.axes.fill_between(v, f_v * 1000, alpha=0.3)
        
        # 标注特征速度
        f_vp = coeff * v_p**2 * np.exp(-M_kg * v_p**2 / (2 * R * T)) * 1000
        self.canvas.axes.axvline(x=v_p, color='r', linestyle='--', linewidth=1, label=f'vₚ={v_p:.0f}')
        self.canvas.axes.axvline(x=v_mean, color='g', linestyle='--', linewidth=1, label=f'⟨v⟩={v_mean:.0f}')
        self.canvas.axes.axvline(x=v_rms, color='purple', linestyle='--', linewidth=1, label=f'vᵣₘₛ={v_rms:.0f}')
        
        self.canvas.axes.set_xlabel('速度 v (m/s)', fontsize=12)
        self.canvas.axes.set_ylabel('f(v) × 10³ (s/m)', fontsize=12)
        self.canvas.axes.set_title(f'麦克斯韦-玻尔兹曼分布 (T={T} K)', fontsize=14)
        self.canvas.axes.legend(loc='upper right')
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.axes.set_xlim(0, 3 * v_rms)
        self.canvas.axes.set_ylim(0, None)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    
    # 创建三个物理可视化窗口
    quantum = QuantumWellVisualizer()
    quantum.show()
    
    oscillator = DampedOscillatorVisualizer()
    oscillator.move(100, 50)
    oscillator.show()
    
    maxwell = MaxwellBoltzmannVisualizer()
    maxwell.move(200, 100)
    maxwell.show()
    
    print("=" * 50)
    print("交互式物理参数可视化")
    print("=" * 50)
    print("示例:")
    print("  1. 量子力学 - 无限深势阱波函数")
    print("  2. 力学 - 阻尼振荡")
    print("  3. 热力学 - 麦克斯韦-玻尔兹曼分布")
    print("=" * 50)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

