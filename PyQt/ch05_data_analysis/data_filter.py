"""
示例程序：数据滤波与处理
所属章节：第五章 - 数据处理与分析界面

功能说明：
    演示常用的数据滤波和预处理方法：
    - 移动平均
    - Savitzky-Golay滤波
    - 巴特沃斯低通滤波
    - 基线校正
    - 异常值去除

运行方式：
    python data_filter.py
"""

import sys
import numpy as np
from scipy.signal import savgol_filter, butter, filtfilt
from scipy.ndimage import uniform_filter1d
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QGroupBox, QFormLayout,
    QSpinBox, QDoubleSpinBox, QCheckBox, QSlider
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    """Matplotlib画布"""
    
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 7), dpi=100)
        super().__init__(self.fig)


class DataFilterDemo(QMainWindow):
    """数据滤波演示"""
    
    def __init__(self):
        super().__init__()
        self.raw_data = None
        self.x_data = None
        self.filtered_data = None
        self.init_ui()
        self.generate_sample_data()
    
    def init_ui(self):
        self.setWindowTitle("数据滤波与处理")
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
                border: 2px solid #16a085;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #1abc9c;
            }
            QPushButton {
                padding: 10px;
                background-color: #1abc9c;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #16a085; }
            QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #bdc3c7;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #1abc9c;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
        """)
    
    def create_control_panel(self) -> QWidget:
        """创建控制面板"""
        panel = QWidget()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        # 数据源
        data_group = QGroupBox("测试数据")
        data_layout = QFormLayout()
        
        self.combo_signal = QComboBox()
        self.combo_signal.addItems([
            "正弦波 + 噪声",
            "多频率叠加",
            "阶跃 + 噪声",
            "光谱峰 + 基线漂移"
        ])
        self.combo_signal.currentIndexChanged.connect(self.generate_sample_data)
        data_layout.addRow("信号类型:", self.combo_signal)
        
        self.spin_noise = QDoubleSpinBox()
        self.spin_noise.setRange(0, 1)
        self.spin_noise.setValue(0.3)
        self.spin_noise.setSingleStep(0.05)
        self.spin_noise.valueChanged.connect(self.generate_sample_data)
        data_layout.addRow("噪声幅度:", self.spin_noise)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # 滤波方法
        filter_group = QGroupBox("滤波方法")
        filter_layout = QVBoxLayout()
        
        self.combo_filter = QComboBox()
        self.combo_filter.addItems([
            "无滤波",
            "移动平均",
            "Savitzky-Golay",
            "巴特沃斯低通",
            "中值滤波",
        ])
        self.combo_filter.currentIndexChanged.connect(self.update_filter_params)
        self.combo_filter.currentIndexChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.combo_filter)
        
        # 滤波参数
        param_layout = QFormLayout()
        
        self.spin_window = QSpinBox()
        self.spin_window.setRange(3, 51)
        self.spin_window.setValue(11)
        self.spin_window.setSingleStep(2)
        self.spin_window.valueChanged.connect(self.apply_filter)
        param_layout.addRow("窗口大小:", self.spin_window)
        
        self.spin_order = QSpinBox()
        self.spin_order.setRange(1, 10)
        self.spin_order.setValue(3)
        self.spin_order.valueChanged.connect(self.apply_filter)
        param_layout.addRow("阶数/多项式:", self.spin_order)
        
        self.spin_cutoff = QDoubleSpinBox()
        self.spin_cutoff.setRange(0.01, 0.5)
        self.spin_cutoff.setValue(0.1)
        self.spin_cutoff.setSingleStep(0.01)
        self.spin_cutoff.valueChanged.connect(self.apply_filter)
        param_layout.addRow("截止频率:", self.spin_cutoff)
        
        filter_layout.addLayout(param_layout)
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # 预处理选项
        preprocess_group = QGroupBox("预处理")
        preprocess_layout = QVBoxLayout()
        
        self.check_baseline = QCheckBox("基线校正")
        self.check_baseline.stateChanged.connect(self.apply_filter)
        preprocess_layout.addWidget(self.check_baseline)
        
        self.check_normalize = QCheckBox("归一化 [0, 1]")
        self.check_normalize.stateChanged.connect(self.apply_filter)
        preprocess_layout.addWidget(self.check_normalize)
        
        self.check_outliers = QCheckBox("去除异常值 (3σ)")
        self.check_outliers.stateChanged.connect(self.apply_filter)
        preprocess_layout.addWidget(self.check_outliers)
        
        preprocess_group.setLayout(preprocess_layout)
        layout.addWidget(preprocess_group)
        
        # 显示选项
        display_group = QGroupBox("显示选项")
        display_layout = QVBoxLayout()
        
        self.check_show_raw = QCheckBox("显示原始数据")
        self.check_show_raw.setChecked(True)
        self.check_show_raw.stateChanged.connect(self.update_plot)
        display_layout.addWidget(self.check_show_raw)
        
        self.check_show_diff = QCheckBox("显示差异")
        self.check_show_diff.stateChanged.connect(self.update_plot)
        display_layout.addWidget(self.check_show_diff)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        layout.addStretch()
        
        # 应用按钮
        btn_apply = QPushButton("🔄 应用滤波")
        btn_apply.clicked.connect(self.apply_filter)
        layout.addWidget(btn_apply)
        
        # 统计信息
        self.label_stats = QLabel("统计信息:")
        self.label_stats.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        self.label_stats.setWordWrap(True)
        layout.addWidget(self.label_stats)
        
        return panel
    
    def update_filter_params(self):
        """根据滤波方法更新参数可用性"""
        filter_type = self.combo_filter.currentIndex()
        
        # 移动平均: 只需要窗口
        # Savitzky-Golay: 窗口 + 阶数
        # 巴特沃斯: 截止频率 + 阶数
        # 中值滤波: 只需要窗口
        
        self.spin_window.setEnabled(filter_type in [1, 2, 4])
        self.spin_order.setEnabled(filter_type in [2, 3])
        self.spin_cutoff.setEnabled(filter_type == 3)
    
    def generate_sample_data(self):
        """生成示例数据"""
        signal_type = self.combo_signal.currentIndex()
        noise_level = self.spin_noise.value()
        
        n = 500
        self.x_data = np.linspace(0, 10, n)
        
        if signal_type == 0:  # 正弦波
            clean = np.sin(2 * np.pi * self.x_data)
            
        elif signal_type == 1:  # 多频率叠加
            clean = (np.sin(2 * np.pi * self.x_data) + 
                    0.5 * np.sin(2 * np.pi * 3 * self.x_data) +
                    0.3 * np.sin(2 * np.pi * 7 * self.x_data))
            
        elif signal_type == 2:  # 阶跃
            clean = np.zeros(n)
            clean[n//4:3*n//4] = 1
            clean = np.convolve(clean, np.ones(10)/10, mode='same')  # 平滑边缘
            
        else:  # 光谱峰 + 基线漂移
            x = self.x_data
            clean = (np.exp(-((x-3)**2)/0.3) + 
                    0.7 * np.exp(-((x-6)**2)/0.5) +
                    0.05 * x)  # 基线漂移
        
        # 添加噪声
        self.raw_data = clean + np.random.randn(n) * noise_level
        self.filtered_data = self.raw_data.copy()
        
        self.apply_filter()
    
    def apply_filter(self):
        """应用滤波"""
        if self.raw_data is None:
            return
        
        data = self.raw_data.copy()
        
        # 1. 去除异常值
        if self.check_outliers.isChecked():
            data = self.remove_outliers(data)
        
        # 2. 应用滤波
        filter_type = self.combo_filter.currentIndex()
        
        if filter_type == 1:  # 移动平均
            window = self.spin_window.value()
            data = uniform_filter1d(data, size=window)
            
        elif filter_type == 2:  # Savitzky-Golay
            window = self.spin_window.value()
            order = min(self.spin_order.value(), window - 1)
            if window % 2 == 0:
                window += 1
            data = savgol_filter(data, window, order)
            
        elif filter_type == 3:  # 巴特沃斯低通
            cutoff = self.spin_cutoff.value()
            order = self.spin_order.value()
            b, a = butter(order, cutoff, btype='low')
            data = filtfilt(b, a, data)
            
        elif filter_type == 4:  # 中值滤波
            from scipy.ndimage import median_filter
            window = self.spin_window.value()
            data = median_filter(data, size=window)
        
        # 3. 基线校正
        if self.check_baseline.isChecked():
            data = self.baseline_correction(data)
        
        # 4. 归一化
        if self.check_normalize.isChecked():
            data = self.normalize(data)
        
        self.filtered_data = data
        self.update_stats()
        self.update_plot()
    
    def remove_outliers(self, data: np.ndarray, threshold: float = 3) -> np.ndarray:
        """使用Z-score方法去除异常值"""
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        mask = z_scores < threshold
        # 用插值替换异常值
        result = data.copy()
        result[~mask] = np.interp(
            np.where(~mask)[0],
            np.where(mask)[0],
            data[mask]
        )
        return result
    
    def baseline_correction(self, data: np.ndarray) -> np.ndarray:
        """多项式基线校正"""
        x = np.arange(len(data))
        # 使用端点拟合基线
        coeffs = np.polyfit(x, data, 1)
        baseline = np.polyval(coeffs, x)
        return data - baseline
    
    def normalize(self, data: np.ndarray) -> np.ndarray:
        """归一化到[0, 1]"""
        min_val = np.min(data)
        max_val = np.max(data)
        if max_val - min_val < 1e-10:
            return data
        return (data - min_val) / (max_val - min_val)
    
    def update_stats(self):
        """更新统计信息"""
        raw = self.raw_data
        filt = self.filtered_data
        
        # 计算信噪比改善
        raw_std = np.std(raw)
        filt_std = np.std(filt - np.mean(filt))
        
        stats = f"原始数据: 均值={np.mean(raw):.3f}, 标准差={raw_std:.3f}\n"
        stats += f"滤波后: 均值={np.mean(filt):.3f}, 标准差={np.std(filt):.3f}\n"
        stats += f"噪声减少: {(1 - filt_std/raw_std)*100:.1f}%"
        
        self.label_stats.setText(stats)
    
    def update_plot(self):
        """更新图形"""
        self.canvas.fig.clear()
        
        show_diff = self.check_show_diff.isChecked()
        
        if show_diff:
            gs = self.canvas.fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.1)
            ax_main = self.canvas.fig.add_subplot(gs[0])
            ax_diff = self.canvas.fig.add_subplot(gs[1], sharex=ax_main)
        else:
            ax_main = self.canvas.fig.add_subplot(111)
        
        # 主图
        if self.check_show_raw.isChecked():
            ax_main.plot(self.x_data, self.raw_data, 'b-', alpha=0.3, 
                        linewidth=0.8, label='原始数据')
        
        ax_main.plot(self.x_data, self.filtered_data, 'r-', 
                    linewidth=1.5, label='滤波后')
        
        filter_name = self.combo_filter.currentText()
        ax_main.set_title(f'数据滤波 - {filter_name}', fontsize=14)
        ax_main.set_ylabel('振幅', fontsize=12)
        ax_main.legend(loc='best')
        ax_main.grid(True, alpha=0.3)
        
        if show_diff:
            ax_main.set_xticklabels([])
            
            diff = self.raw_data - self.filtered_data
            ax_diff.plot(self.x_data, diff, 'g-', linewidth=0.8)
            ax_diff.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
            ax_diff.set_xlabel('x', fontsize=12)
            ax_diff.set_ylabel('差异', fontsize=10)
            ax_diff.grid(True, alpha=0.3)
        else:
            ax_main.set_xlabel('x', fontsize=12)
        
        self.canvas.fig.tight_layout()
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = DataFilterDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

