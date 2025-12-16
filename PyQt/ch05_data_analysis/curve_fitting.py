"""
示例程序：曲线拟合界面
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示科研数据的曲线拟合：
    - 多种拟合函数（高斯、洛伦兹、指数、多项式）
    - 初始参数估计
    - 拟合结果评估（R²、残差）
    - 可视化显示

运行方式：
    python curve_fitting.py
"""

import sys
import numpy as np
from scipy.optimize import curve_fit
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QDoubleSpinBox, QTextEdit, QSpinBox, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# ============================================================
# 拟合函数定义
# ============================================================

def gaussian(x, A, mu, sigma, C):
    """高斯函数"""
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2)) + C

def lorentzian(x, A, x0, gamma, C):
    """洛伦兹函数"""
    return A * (gamma/2)**2 / ((x - x0)**2 + (gamma/2)**2) + C

def exponential(x, A, tau, C):
    """指数衰减"""
    return A * np.exp(-x / tau) + C

def linear(x, a, b):
    """线性函数"""
    return a * x + b

def polynomial(x, *coeffs):
    """多项式"""
    return sum(c * x**i for i, c in enumerate(coeffs))

def power_law(x, A, n, C):
    """幂律函数"""
    return A * np.power(np.abs(x) + 1e-10, n) + C

def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2, C):
    """双高斯函数"""
    return (A1 * np.exp(-(x - mu1)**2 / (2 * sigma1**2)) +
            A2 * np.exp(-(x - mu2)**2 / (2 * sigma2**2)) + C)


FIT_FUNCTIONS = {
    "高斯 (Gaussian)": {
        "func": gaussian,
        "params": ["振幅 A", "中心 μ", "宽度 σ", "基线 C"],
        "p0_func": lambda x, y: [y.max() - y.min(), x[np.argmax(y)], (x.max()-x.min())/10, y.min()],
    },
    "洛伦兹 (Lorentzian)": {
        "func": lorentzian,
        "params": ["振幅 A", "中心 x₀", "半宽 Γ", "基线 C"],
        "p0_func": lambda x, y: [y.max() - y.min(), x[np.argmax(y)], (x.max()-x.min())/10, y.min()],
    },
    "指数衰减 (Exponential)": {
        "func": exponential,
        "params": ["振幅 A", "时间常数 τ", "基线 C"],
        "p0_func": lambda x, y: [y[0] - y[-1], (x.max()-x.min())/3, y[-1]],
    },
    "线性 (Linear)": {
        "func": linear,
        "params": ["斜率 a", "截距 b"],
        "p0_func": lambda x, y: [(y[-1]-y[0])/(x[-1]-x[0]), y[0]],
    },
    "二次多项式": {
        "func": lambda x, a, b, c: a*x**2 + b*x + c,
        "params": ["a (x²)", "b (x)", "c (常数)"],
        "p0_func": lambda x, y: [0, (y[-1]-y[0])/(x[-1]-x[0]), y[0]],
    },
    "幂律 (Power Law)": {
        "func": power_law,
        "params": ["振幅 A", "指数 n", "基线 C"],
        "p0_func": lambda x, y: [y.max(), 1, y.min()],
    },
}


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 7), dpi=100)
        super().__init__(self.fig)


class CurveFittingApp(QMainWindow):
    """曲线拟合应用"""
    
    def __init__(self):
        super().__init__()
        self.x_data = None
        self.y_data = None
        self.fit_result = None
        self.init_ui()
        self.generate_sample_data()
    
    def init_ui(self):
        self.setWindowTitle("曲线拟合工具")
        self.setMinimumSize(1100, 750)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        
        # 左侧控制面板
        main_layout.addWidget(self.create_control_panel(), stretch=0)
        
        # 右侧图形
        plot_layout = QVBoxLayout()
        
        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
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
                color: #8e44ad;
            }
            QPushButton {
                padding: 10px;
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8e44ad; }
            QComboBox, QDoubleSpinBox, QSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        # 数据源
        data_group = QGroupBox("数据源")
        data_layout = QVBoxLayout()
        
        self.combo_data = QComboBox()
        self.combo_data.addItems([
            "高斯峰 + 噪声",
            "洛伦兹峰 + 噪声",
            "指数衰减 + 噪声",
            "双峰光谱",
            "自定义数据"
        ])
        self.combo_data.currentIndexChanged.connect(self.generate_sample_data)
        data_layout.addWidget(self.combo_data)
        
        noise_layout = QHBoxLayout()
        noise_layout.addWidget(QLabel("噪声:"))
        self.spin_noise = QDoubleSpinBox()
        self.spin_noise.setRange(0, 0.5)
        self.spin_noise.setValue(0.05)
        self.spin_noise.setSingleStep(0.01)
        self.spin_noise.valueChanged.connect(self.generate_sample_data)
        noise_layout.addWidget(self.spin_noise)
        data_layout.addLayout(noise_layout)
        
        btn_import = QPushButton("📂 导入数据")
        btn_import.clicked.connect(self.import_data)
        data_layout.addWidget(btn_import)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # 拟合设置
        fit_group = QGroupBox("拟合设置")
        fit_layout = QVBoxLayout()
        
        fit_layout.addWidget(QLabel("拟合函数:"))
        self.combo_func = QComboBox()
        self.combo_func.addItems(list(FIT_FUNCTIONS.keys()))
        self.combo_func.currentIndexChanged.connect(self.update_param_display)
        fit_layout.addWidget(self.combo_func)
        
        # 参数显示区
        self.label_params = QLabel("参数: A, μ, σ, C")
        self.label_params.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        self.label_params.setWordWrap(True)
        fit_layout.addWidget(self.label_params)
        
        btn_fit = QPushButton("🔬 执行拟合")
        btn_fit.setStyleSheet("background-color: #27ae60;")
        btn_fit.clicked.connect(self.perform_fit)
        fit_layout.addWidget(btn_fit)
        
        fit_group.setLayout(fit_layout)
        layout.addWidget(fit_group)
        
        # 拟合结果
        result_group = QGroupBox("拟合结果")
        result_layout = QVBoxLayout()
        
        self.text_result = QTextEdit()
        self.text_result.setReadOnly(True)
        self.text_result.setMaximumHeight(200)
        self.text_result.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 11px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        result_layout.addWidget(self.text_result)
        
        self.check_show_residual = QCheckBox("显示残差")
        self.check_show_residual.stateChanged.connect(self.update_plot)
        result_layout.addWidget(self.check_show_residual)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()
        
        # 导出
        btn_export = QPushButton("💾 导出结果")
        btn_export.clicked.connect(self.export_results)
        layout.addWidget(btn_export)
        
        return panel
    
    def update_param_display(self):
        """更新参数显示"""
        func_name = self.combo_func.currentText()
        if func_name in FIT_FUNCTIONS:
            params = FIT_FUNCTIONS[func_name]["params"]
            self.label_params.setText("参数: " + ", ".join(params))
    
    def generate_sample_data(self):
        """生成示例数据"""
        data_type = self.combo_data.currentIndex()
        noise = self.spin_noise.value()
        
        if data_type == 0:  # 高斯峰
            x = np.linspace(-5, 5, 200)
            y = 2.0 * np.exp(-(x - 0.5)**2 / (2 * 0.8**2)) + 0.3
            y += np.random.randn(len(x)) * noise
            
        elif data_type == 1:  # 洛伦兹峰
            x = np.linspace(-5, 5, 200)
            gamma = 0.8
            y = 2.0 * (gamma/2)**2 / ((x - 0.5)**2 + (gamma/2)**2) + 0.2
            y += np.random.randn(len(x)) * noise
            
        elif data_type == 2:  # 指数衰减
            x = np.linspace(0, 10, 200)
            y = 3.0 * np.exp(-x / 2.5) + 0.5
            y += np.random.randn(len(x)) * noise
            
        elif data_type == 3:  # 双峰光谱
            x = np.linspace(400, 700, 300)
            y = (0.8 * np.exp(-((x - 480)**2) / (2 * 20**2)) +
                 1.2 * np.exp(-((x - 580)**2) / (2 * 25**2)) + 0.1)
            y += np.random.randn(len(x)) * noise
            
        else:
            return
        
        self.x_data = x
        self.y_data = y
        self.fit_result = None
        self.text_result.clear()
        self.update_plot()
    
    def import_data(self):
        """导入数据"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "导入数据", "", "CSV文件 (*.csv);;文本文件 (*.txt);;所有文件 (*)"
        )
        
        if filename:
            try:
                data = np.loadtxt(filename, delimiter=',', skiprows=1)
                self.x_data = data[:, 0]
                self.y_data = data[:, 1]
                self.fit_result = None
                self.text_result.clear()
                self.update_plot()
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "导入错误", str(e))
    
    def perform_fit(self):
        """执行拟合"""
        if self.x_data is None or self.y_data is None:
            return
        
        func_name = self.combo_func.currentText()
        func_info = FIT_FUNCTIONS.get(func_name)
        
        if not func_info:
            return
        
        try:
            # 获取初始参数
            p0 = func_info["p0_func"](self.x_data, self.y_data)
            
            # 执行拟合
            popt, pcov = curve_fit(
                func_info["func"], 
                self.x_data, 
                self.y_data, 
                p0=p0,
                maxfev=5000
            )
            
            # 计算误差
            perr = np.sqrt(np.diag(pcov))
            
            # 计算拟合值
            y_fit = func_info["func"](self.x_data, *popt)
            
            # 计算R²
            ss_res = np.sum((self.y_data - y_fit)**2)
            ss_tot = np.sum((self.y_data - np.mean(self.y_data))**2)
            r_squared = 1 - ss_res / ss_tot
            
            # 计算卡方
            chi_squared = np.sum((self.y_data - y_fit)**2) / len(self.y_data)
            
            # 存储结果
            self.fit_result = {
                "func_name": func_name,
                "popt": popt,
                "perr": perr,
                "y_fit": y_fit,
                "r_squared": r_squared,
                "chi_squared": chi_squared,
                "residuals": self.y_data - y_fit
            }
            
            # 显示结果
            self.display_results(func_info["params"])
            self.update_plot()
            
        except Exception as e:
            self.text_result.setText(f"拟合失败:\n{str(e)}")
    
    def display_results(self, param_names: list):
        """显示拟合结果"""
        if not self.fit_result:
            return
        
        result = self.fit_result
        text = f"═══ {result['func_name']} 拟合结果 ═══\n\n"
        
        text += "拟合参数:\n"
        for name, val, err in zip(param_names, result['popt'], result['perr']):
            text += f"  {name}: {val:.6g} ± {err:.6g}\n"
        
        text += f"\n评估指标:\n"
        text += f"  R² = {result['r_squared']:.6f}\n"
        text += f"  χ² = {result['chi_squared']:.6g}\n"
        
        text += f"\n残差统计:\n"
        res = result['residuals']
        text += f"  均值 = {np.mean(res):.6g}\n"
        text += f"  标准差 = {np.std(res):.6g}\n"
        text += f"  最大 = {np.max(np.abs(res)):.6g}\n"
        
        self.text_result.setText(text)
    
    def update_plot(self):
        """更新图形"""
        if self.x_data is None:
            return
        
        self.canvas.fig.clear()
        
        show_residual = self.check_show_residual.isChecked() and self.fit_result
        
        if show_residual:
            gs = self.canvas.fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.1)
            ax_main = self.canvas.fig.add_subplot(gs[0])
            ax_res = self.canvas.fig.add_subplot(gs[1], sharex=ax_main)
        else:
            ax_main = self.canvas.fig.add_subplot(111)
        
        # 绑制数据点
        ax_main.scatter(self.x_data, self.y_data, c='#3498db', s=20, alpha=0.6, label='数据')
        
        # 绑制拟合曲线
        if self.fit_result:
            ax_main.plot(self.x_data, self.fit_result['y_fit'], 'r-', 
                        linewidth=2, label=f"拟合 (R²={self.fit_result['r_squared']:.4f})")
        
        ax_main.set_ylabel('y', fontsize=12)
        ax_main.set_title('曲线拟合', fontsize=14)
        ax_main.legend(loc='best')
        ax_main.grid(True, alpha=0.3)
        
        if show_residual:
            ax_main.set_xticklabels([])
            
            # 绑制残差
            ax_res.scatter(self.x_data, self.fit_result['residuals'], 
                          c='#27ae60', s=15, alpha=0.6)
            ax_res.axhline(y=0, color='gray', linestyle='--', linewidth=1)
            ax_res.set_xlabel('x', fontsize=12)
            ax_res.set_ylabel('残差', fontsize=10)
            ax_res.grid(True, alpha=0.3)
        else:
            ax_main.set_xlabel('x', fontsize=12)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()
    
    def export_results(self):
        """导出结果"""
        if not self.fit_result:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "请先执行拟合")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出结果", "fit_result.txt", "文本文件 (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.text_result.toPlainText())
                    f.write("\n\n原始数据和拟合值:\n")
                    f.write("x, y_data, y_fit, residual\n")
                    for x, y, yf, r in zip(self.x_data, self.y_data, 
                                           self.fit_result['y_fit'],
                                           self.fit_result['residuals']):
                        f.write(f"{x:.6g}, {y:.6g}, {yf:.6g}, {r:.6g}\n")
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(self, "导出成功", f"结果已保存到:\n{filename}")
                
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(self, "导出错误", str(e))


def main():
    app = QApplication(sys.argv)
    window = CurveFittingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

