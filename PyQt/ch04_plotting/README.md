# 第四章：Matplotlib科研绑图集成

> 本章将学习如何在PyQt中嵌入Matplotlib，实现交互式科研数据可视化

## 本章内容

- [4.1 Matplotlib嵌入PyQt基础](#41-matplotlib嵌入pyqt基础)
- [4.2 带工具栏的绑图窗口](#42-带工具栏的绑图窗口)
- [4.3 实时数据更新曲线](#43-实时数据更新曲线)
- [4.4 交互式参数调节器](#44-交互式参数调节器)
- [4.5 多子图与联动控制](#45-多子图与联动控制)
- [4.6 科研图表样式定制](#46-科研图表样式定制)
- [4.7 图表导出与保存](#47-图表导出与保存)

---

## 为什么在PyQt中使用Matplotlib？

Matplotlib是Python最流行的绑图库，将其嵌入PyQt可以实现：

1. **交互式参数调节**：通过滑块、输入框实时改变图形参数
2. **实时数据可视化**：显示仪器采集的实时数据流
3. **定制化界面**：结合PyQt控件创建专业的数据分析工具
4. **多图表联动**：多个图表同步显示不同维度的数据

---

## 4.1 Matplotlib嵌入PyQt基础

**示例程序**：[mpl_embed_basic.py](mpl_embed_basic.py)

### 核心组件

将Matplotlib嵌入PyQt需要两个关键类：

```python
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
```

| 类 | 说明 |
|---|------|
| `Figure` | Matplotlib图形对象 |
| `FigureCanvasQTAgg` | 将Figure渲染为Qt控件 |

### 基本结构

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Matplotlib画布类"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 创建Figure对象
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 添加子图
        self.axes = self.fig.add_subplot(111)
        # 初始化父类
        super().__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建画布
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        
        # 绑图
        self.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        
        # 设置为中央控件
        self.setCentralWidget(self.canvas)
```

### 更新图形

修改图形后需要调用 `draw()` 刷新显示：

```python
def update_plot(self):
    self.canvas.axes.clear()  # 清除旧图
    self.canvas.axes.plot(new_x, new_y)  # 绑制新图
    self.canvas.draw()  # 刷新显示
```

---

## 4.2 带工具栏的绑图窗口

**示例程序**：[mpl_with_toolbar.py](mpl_with_toolbar.py)

### NavigationToolbar2QT

Matplotlib提供了标准工具栏，支持缩放、平移、保存等功能：

```python
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

# 创建工具栏
self.toolbar = NavigationToolbar(self.canvas, self)
```

### 工具栏功能

| 按钮 | 功能 |
|------|------|
| 🏠 Home | 恢复原始视图 |
| ⬅️➡️ | 前进/后退视图历史 |
| ✥ Pan | 拖动平移 |
| 🔍 Zoom | 矩形缩放 |
| ⚙️ Subplots | 调整子图边距 |
| 💾 Save | 保存图片 |

### 布局示例

```python
class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建画布
        self.canvas = MplCanvas(self)
        
        # 创建工具栏
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
```

---

## 4.3 实时数据更新曲线

**示例程序**：[realtime_plot.py](realtime_plot.py)

### 使用QTimer实现实时更新

```python
from PyQt6.QtCore import QTimer

class RealtimePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.canvas = MplCanvas(self)
        self.data = []
        
        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # 每100ms更新一次
    
    def update_plot(self):
        # 添加新数据点
        self.data.append(random.random())
        
        # 保持最近100个点
        if len(self.data) > 100:
            self.data = self.data[-100:]
        
        # 更新图形
        self.canvas.axes.clear()
        self.canvas.axes.plot(self.data)
        self.canvas.draw()
```

### 优化：使用 set_data 提高性能

频繁重绑会影响性能，可以只更新数据：

```python
class OptimizedRealtimePlot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.canvas = MplCanvas(self)
        
        # 初始化空线条
        self.line, = self.canvas.axes.plot([], [])
        self.canvas.axes.set_xlim(0, 100)
        self.canvas.axes.set_ylim(0, 1)
        
        self.xdata = []
        self.ydata = []
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)
    
    def update_plot(self):
        # 添加数据
        self.xdata.append(len(self.xdata))
        self.ydata.append(random.random())
        
        # 只更新数据，不重绘整个图形
        self.line.set_data(self.xdata[-100:], self.ydata[-100:])
        
        # 调整x轴范围
        if len(self.xdata) > 100:
            self.canvas.axes.set_xlim(len(self.xdata)-100, len(self.xdata))
        
        self.canvas.draw()
```

### 使用 blit 进一步优化

对于高频更新，可以使用 blit 技术只重绘变化部分：

```python
# 保存背景
self.background = self.canvas.copy_from_bbox(self.canvas.axes.bbox)

def update_plot(self):
    # 恢复背景
    self.canvas.restore_region(self.background)
    
    # 更新数据
    self.line.set_ydata(new_data)
    
    # 只重绘线条
    self.canvas.axes.draw_artist(self.line)
    
    # blit更新
    self.canvas.blit(self.canvas.axes.bbox)
```

---

## 4.4 交互式参数调节器

**示例程序**：[interactive_params.py](interactive_params.py)

### 物理函数可视化

这是本教程最实用的功能之一：通过界面控件实时调节物理函数的参数。

### 示例：波函数可视化

```python
class WaveFunctionPlot(QMainWindow):
    """量子力学波函数可视化"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # 创建画布和控件
        self.canvas = MplCanvas(self)
        
        # 参数控件
        self.spin_n = QSpinBox()  # 量子数n
        self.spin_n.setRange(1, 10)
        self.spin_n.valueChanged.connect(self.update_plot)
        
        self.spin_l = QDoubleSpinBox()  # 势阱宽度L
        self.spin_l.setRange(0.1, 10)
        self.spin_l.valueChanged.connect(self.update_plot)
        
        # 初始绑图
        self.update_plot()
    
    def update_plot(self):
        n = self.spin_n.value()
        L = self.spin_l.value()
        
        x = np.linspace(0, L, 500)
        psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
        
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, psi, 'b-', linewidth=2)
        self.canvas.axes.plot(x, psi**2, 'r--', linewidth=1.5, label='|ψ|²')
        self.canvas.axes.set_xlabel('x')
        self.canvas.axes.set_ylabel('ψ(x)')
        self.canvas.axes.set_title(f'无限深势阱波函数 (n={n})')
        self.canvas.axes.legend()
        self.canvas.axes.grid(True, alpha=0.3)
        self.canvas.draw()
```

### 使用滑动条调节参数

```python
# 创建滑动条
self.slider_freq = QSlider(Qt.Orientation.Horizontal)
self.slider_freq.setRange(1, 100)
self.slider_freq.setValue(10)
self.slider_freq.valueChanged.connect(self.on_freq_changed)

def on_freq_changed(self, value):
    freq = value / 10.0  # 转换为实际频率
    self.update_plot(freq)
```

---

## 4.5 多子图与联动控制

**示例程序**：[multi_subplot.py](multi_subplot.py)

### 创建多子图

```python
class MultiSubplotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(10, 8))
        
        # 创建2x2子图
        self.axes = self.fig.subplots(2, 2)
        
        super().__init__(self.fig)
```

### 子图布局方式

```python
# 方式1：规则网格
self.fig, self.axes = plt.subplots(2, 2)

# 方式2：使用GridSpec自定义布局
from matplotlib.gridspec import GridSpec
gs = GridSpec(3, 3, figure=self.fig)
self.ax1 = self.fig.add_subplot(gs[0, :])    # 第一行，跨所有列
self.ax2 = self.fig.add_subplot(gs[1:, 0])   # 左下角
self.ax3 = self.fig.add_subplot(gs[1:, 1:])  # 右下角
```

### 联动控制示例

```python
class LinkedPlots(QMainWindow):
    """多图联动：时域-频域分析"""
    
    def update_plots(self):
        # 生成信号
        t = np.linspace(0, 1, 1000)
        freq = self.spin_freq.value()
        signal = np.sin(2 * np.pi * freq * t)
        
        # 子图1：时域波形
        self.axes[0, 0].clear()
        self.axes[0, 0].plot(t, signal)
        self.axes[0, 0].set_title('时域信号')
        
        # 子图2：频谱
        fft = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), t[1]-t[0])
        self.axes[0, 1].clear()
        self.axes[0, 1].plot(freqs[:len(freqs)//2], np.abs(fft)[:len(fft)//2])
        self.axes[0, 1].set_title('频谱')
        
        # 子图3：相位
        self.axes[1, 0].clear()
        self.axes[1, 0].plot(freqs[:len(freqs)//2], np.angle(fft)[:len(fft)//2])
        self.axes[1, 0].set_title('相位')
        
        # 子图4：功率谱
        self.axes[1, 1].clear()
        self.axes[1, 1].semilogy(freqs[:len(freqs)//2], np.abs(fft)[:len(fft)//2]**2)
        self.axes[1, 1].set_title('功率谱')
        
        self.fig.tight_layout()
        self.canvas.draw()
```

---

## 4.6 科研图表样式定制

**示例程序**：[scientific_style.py](scientific_style.py)

### 设置全局样式

```python
import matplotlib.pyplot as plt

# 使用预设样式
plt.style.use('seaborn-v0_8-whitegrid')

# 或自定义样式
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.figsize': (8, 6),
    'figure.dpi': 100,
    'lines.linewidth': 2,
    'lines.markersize': 8,
})
```

### 科研论文风格

```python
def setup_publication_style():
    """设置适合论文发表的图表样式"""
    plt.rcParams.update({
        # 字体设置
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        
        # 字号设置
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        
        # 图形大小（适合双栏论文）
        'figure.figsize': (3.5, 2.8),  # 单栏宽度约3.5英寸
        'figure.dpi': 300,
        
        # 线条和标记
        'lines.linewidth': 1.5,
        'lines.markersize': 5,
        
        # 坐标轴
        'axes.linewidth': 0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        
        # 图例
        'legend.frameon': True,
        'legend.framealpha': 0.8,
        'legend.edgecolor': 'gray',
    })
```

### 颜色方案

```python
# 色盲友好的颜色方案
colors_colorblind = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#F0E442']

# 经典科研配色
colors_classic = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# 使用颜色循环
from cycler import cycler
plt.rcParams['axes.prop_cycle'] = cycler(color=colors_colorblind)
```

### LaTeX公式支持

```python
# 启用LaTeX渲染
plt.rcParams['text.usetex'] = True  # 需要安装LaTeX

# 或使用mathtext（不需要LaTeX）
ax.set_xlabel(r'$\omega$ (rad/s)')
ax.set_ylabel(r'$|\chi(\omega)|$ (a.u.)')
ax.set_title(r'$\chi = \chi_0 / (1 - i\omega\tau)$')
```

---

## 4.7 图表导出与保存

**示例程序**：[plot_export.py](plot_export.py)

### 保存图片

```python
# 保存为各种格式
self.canvas.figure.savefig('plot.png', dpi=300, bbox_inches='tight')
self.canvas.figure.savefig('plot.pdf', bbox_inches='tight')
self.canvas.figure.savefig('plot.svg', bbox_inches='tight')
self.canvas.figure.savefig('plot.eps', bbox_inches='tight')
```

### savefig 参数说明

| 参数 | 说明 |
|------|------|
| `dpi` | 分辨率（PNG/JPG） |
| `bbox_inches='tight'` | 自动裁剪空白边距 |
| `transparent=True` | 透明背景 |
| `facecolor` | 背景颜色 |
| `pad_inches` | 边距大小 |

### 使用文件对话框

```python
from PyQt6.QtWidgets import QFileDialog

def save_figure(self):
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "保存图片",
        "",
        "PNG图片 (*.png);;PDF文档 (*.pdf);;SVG矢量图 (*.svg);;所有文件 (*)"
    )
    
    if filename:
        self.canvas.figure.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"图片已保存: {filename}")
```

### 导出数据

```python
import numpy as np

def export_data(self):
    """导出绘图数据为CSV"""
    filename, _ = QFileDialog.getSaveFileName(
        self, "导出数据", "", "CSV文件 (*.csv)"
    )
    
    if filename:
        # 获取线条数据
        line = self.canvas.axes.get_lines()[0]
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        
        # 保存为CSV
        data = np.column_stack([x_data, y_data])
        np.savetxt(filename, data, delimiter=',', header='x,y', comments='')
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **基础嵌入**：FigureCanvas和Figure的使用
2. **工具栏**：NavigationToolbar添加交互功能
3. **实时更新**：QTimer驱动的动态图表
4. **交互调参**：控件与图表参数联动
5. **多子图**：GridSpec布局和联动控制
6. **专业样式**：科研论文级别的图表定制
7. **导出保存**：多格式输出和数据导出

### 性能优化建议

| 场景 | 建议 |
|------|------|
| 低频更新（<1Hz） | 直接使用 clear() + plot() + draw() |
| 中频更新（1-10Hz） | 使用 set_data() 只更新数据 |
| 高频更新（>10Hz） | 使用 blit 技术或考虑 PyQtGraph |
| 大数据量 | 降采样显示，或使用 PyQtGraph |

### 练习题

1. 创建一个阻尼振荡可视化工具：
   - 可调节阻尼系数、频率、初始振幅
   - 同时显示位移、速度、能量曲线

2. 创建一个FFT分析器：
   - 导入音频或生成测试信号
   - 显示时域和频域图
   - 可调窗函数类型

---

## 下一章预告

[第五章：数据处理与分析界面](../ch05_data_analysis/) - 学习文件操作、曲线拟合界面和多线程数据处理。

