# 第五章：数据处理与分析界面

> 本章将学习构建用于物理数据处理的GUI工具，包括文件操作、曲线拟合和多线程处理

## 本章内容

- [5.1 文件对话框与数据导入](#51-文件对话框与数据导入)
- [5.2 表格控件显示数据](#52-表格控件显示数据)
- [5.3 曲线拟合界面](#53-曲线拟合界面)
- [5.4 数据滤波与处理](#54-数据滤波与处理)
- [5.5 多线程防止界面冻结](#55-多线程防止界面冻结)
- [5.6 进度条与状态反馈](#56-进度条与状态反馈)

---

## 5.1 文件对话框与数据导入

**示例程序**：[file_dialog.py](file_dialog.py)

### QFileDialog - 文件对话框

PyQt提供了标准的文件对话框，用于打开和保存文件。

#### 打开单个文件

```python
from PyQt6.QtWidgets import QFileDialog

def open_file(self):
    filename, _ = QFileDialog.getOpenFileName(
        self,                           # 父窗口
        "打开文件",                      # 对话框标题
        "",                             # 默认目录
        "数据文件 (*.csv *.txt);;所有文件 (*)"  # 文件过滤器
    )
    
    if filename:
        print(f"选择的文件: {filename}")
```

#### 打开多个文件

```python
def open_files(self):
    filenames, _ = QFileDialog.getOpenFileNames(
        self,
        "选择多个文件",
        "",
        "数据文件 (*.csv *.txt)"
    )
    
    for filename in filenames:
        print(filename)
```

#### 保存文件

```python
def save_file(self):
    filename, _ = QFileDialog.getSaveFileName(
        self,
        "保存文件",
        "data.csv",           # 默认文件名
        "CSV文件 (*.csv);;文本文件 (*.txt)"
    )
    
    if filename:
        # 保存数据...
        pass
```

#### 选择目录

```python
def select_folder(self):
    folder = QFileDialog.getExistingDirectory(
        self,
        "选择目录"
    )
    
    if folder:
        print(f"选择的目录: {folder}")
```

### 文件过滤器格式

```python
# 单个过滤器
"CSV文件 (*.csv)"

# 多个过滤器（用;;分隔）
"CSV文件 (*.csv);;Excel文件 (*.xlsx);;所有文件 (*)"

# 多个扩展名
"数据文件 (*.csv *.txt *.dat)"
```

### 读取数据文件

```python
import numpy as np

def load_csv(self, filename: str):
    """加载CSV文件"""
    try:
        # 使用NumPy加载
        data = np.loadtxt(filename, delimiter=',', skiprows=1)
        return data
    except Exception as e:
        QMessageBox.critical(self, "错误", f"加载失败: {e}")
        return None
```

---

## 5.2 表格控件显示数据

**示例程序**：[table_view.py](table_view.py)

### QTableWidget vs QTableView

| 控件 | 特点 | 适用场景 |
|------|------|----------|
| `QTableWidget` | 简单易用，直接操作单元格 | 小数据量、简单表格 |
| `QTableView` | 使用Model/View架构 | 大数据量、复杂数据结构 |

### QTableWidget 基本用法

```python
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

# 创建表格
table = QTableWidget()
table.setRowCount(10)
table.setColumnCount(3)

# 设置表头
table.setHorizontalHeaderLabels(["时间", "温度", "电压"])

# 设置单元格内容
table.setItem(0, 0, QTableWidgetItem("0.0"))
table.setItem(0, 1, QTableWidgetItem("300.5"))
table.setItem(0, 2, QTableWidgetItem("1.234"))

# 获取单元格内容
value = table.item(0, 1).text()  # "300.5"
```

### 加载NumPy数组到表格

```python
def load_array_to_table(self, data: np.ndarray, headers: list):
    """将NumPy数组加载到表格"""
    rows, cols = data.shape
    
    self.table.setRowCount(rows)
    self.table.setColumnCount(cols)
    self.table.setHorizontalHeaderLabels(headers)
    
    for i in range(rows):
        for j in range(cols):
            item = QTableWidgetItem(f"{data[i, j]:.6g}")
            self.table.setItem(i, j, item)
```

### 表格样式设置

```python
# 调整列宽
table.setColumnWidth(0, 100)
table.resizeColumnsToContents()

# 交替行颜色
table.setAlternatingRowColors(True)

# 选择模式
table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

# 禁止编辑
table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
```

---

## 5.3 曲线拟合界面

**示例程序**：[curve_fitting.py](curve_fitting.py)

### scipy.optimize.curve_fit

曲线拟合是物理数据分析的核心功能。

```python
from scipy.optimize import curve_fit
import numpy as np

# 定义拟合函数
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# 拟合数据
popt, pcov = curve_fit(gaussian, x_data, y_data, p0=[1, 0, 1])

# popt: 最优参数 [A, mu, sigma]
# pcov: 协方差矩阵（对角线的平方根是参数误差）
perr = np.sqrt(np.diag(pcov))
```

### 常用拟合函数

```python
# 线性
def linear(x, a, b):
    return a * x + b

# 多项式
def polynomial(x, *coeffs):
    return sum(c * x**i for i, c in enumerate(coeffs))

# 高斯
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# 洛伦兹
def lorentzian(x, A, x0, gamma):
    return A * (gamma/2)**2 / ((x - x0)**2 + (gamma/2)**2)

# 指数衰减
def exponential(x, A, tau, C):
    return A * np.exp(-x / tau) + C

# 幂律
def power_law(x, A, n):
    return A * x**n
```

### 拟合结果评估

```python
# R²值
def r_squared(y_data, y_fit):
    ss_res = np.sum((y_data - y_fit) ** 2)
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
    return 1 - ss_res / ss_tot

# 残差
residuals = y_data - y_fit

# 卡方
chi_squared = np.sum((y_data - y_fit)**2 / y_fit)
```

---

## 5.4 数据滤波与处理

**示例程序**：[data_filter.py](data_filter.py)

### 常用滤波方法

#### 移动平均滤波

```python
def moving_average(data, window_size):
    """简单移动平均"""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
```

#### Savitzky-Golay滤波

```python
from scipy.signal import savgol_filter

# 平滑数据同时保留峰形
smoothed = savgol_filter(data, window_length=11, polyorder=3)
```

#### 巴特沃斯低通滤波

```python
from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, cutoff, fs, order=5):
    """巴特沃斯低通滤波"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)
```

#### FFT滤波

```python
def fft_filter(data, threshold):
    """FFT频域滤波"""
    fft = np.fft.fft(data)
    fft[np.abs(fft) < threshold] = 0
    return np.real(np.fft.ifft(fft))
```

### 数据预处理

```python
# 去除异常值
def remove_outliers(data, threshold=3):
    """使用Z-score去除异常值"""
    z_scores = np.abs((data - np.mean(data)) / np.std(data))
    return data[z_scores < threshold]

# 归一化
def normalize(data):
    """归一化到[0, 1]"""
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# 基线校正
def baseline_correction(data, order=1):
    """多项式基线校正"""
    x = np.arange(len(data))
    coeffs = np.polyfit(x, data, order)
    baseline = np.polyval(coeffs, x)
    return data - baseline
```

---

## 5.5 多线程防止界面冻结

**示例程序**：[threading_demo.py](threading_demo.py)

### 为什么需要多线程？

PyQt的GUI运行在主线程中。如果在主线程执行耗时操作，界面会"冻结"无响应。

### QThread 基本用法

```python
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    """工作线程"""
    
    # 定义信号
    progress = pyqtSignal(int)
    result = pyqtSignal(object)
    finished = pyqtSignal()
    
    def __init__(self, data):
        super().__init__()
        self.data = data
    
    def run(self):
        """线程执行的任务"""
        result = []
        for i, item in enumerate(self.data):
            # 处理数据
            processed = item * 2
            result.append(processed)
            
            # 发送进度信号
            progress = int((i + 1) / len(self.data) * 100)
            self.progress.emit(progress)
        
        # 发送结果
        self.result.emit(result)
        self.finished.emit()
```

### 使用工作线程

```python
class MainWindow(QMainWindow):
    def start_processing(self):
        # 创建线程
        self.thread = WorkerThread(self.data)
        
        # 连接信号
        self.thread.progress.connect(self.update_progress)
        self.thread.result.connect(self.on_result)
        self.thread.finished.connect(self.on_finished)
        
        # 启动线程
        self.thread.start()
        
        # 禁用开始按钮
        self.btn_start.setEnabled(False)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def on_result(self, result):
        self.data = result
        self.update_display()
    
    def on_finished(self):
        self.btn_start.setEnabled(True)
```

### 线程安全注意事项

1. **不要在工作线程中直接操作GUI控件**
2. **使用信号槽进行线程间通信**
3. **注意数据的线程安全访问**

---

## 5.6 进度条与状态反馈

**示例程序**：[progress_bar.py](progress_bar.py)

### QProgressBar

```python
from PyQt6.QtWidgets import QProgressBar

# 创建进度条
progress = QProgressBar()
progress.setRange(0, 100)
progress.setValue(50)

# 显示百分比文本
progress.setFormat("%v / %m (%p%)")

# 不确定进度（忙碌指示）
progress.setRange(0, 0)  # 设置范围为0-0
```

### QProgressDialog

用于模态进度对话框：

```python
from PyQt6.QtWidgets import QProgressDialog

dialog = QProgressDialog("处理中...", "取消", 0, 100, self)
dialog.setWindowModality(Qt.WindowModality.WindowModal)
dialog.show()

for i in range(100):
    if dialog.wasCanceled():
        break
    dialog.setValue(i)
    QApplication.processEvents()

dialog.close()
```

### 状态栏反馈

```python
# 临时消息（自动消失）
self.statusBar().showMessage("操作完成", 3000)  # 显示3秒

# 永久控件
self.label_status = QLabel("就绪")
self.statusBar().addPermanentWidget(self.label_status)
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **文件操作**：打开、保存、选择目录
2. **表格控件**：显示和编辑数据表格
3. **曲线拟合**：高斯、洛伦兹、指数等拟合
4. **数据滤波**：移动平均、Savitzky-Golay、FFT滤波
5. **多线程**：QThread防止界面冻结
6. **进度反馈**：进度条和状态栏

### 数据处理工作流

```
┌─────────────────┐
│   导入数据       │ ← QFileDialog + np.loadtxt
└────────┬────────┘
         ▼
┌─────────────────┐
│   显示数据       │ ← QTableWidget
└────────┬────────┘
         ▼
┌─────────────────┐
│   预处理/滤波    │ ← Savitzky-Golay, 基线校正
└────────┬────────┘
         ▼
┌─────────────────┐
│   曲线拟合       │ ← curve_fit
└────────┬────────┘
         ▼
┌─────────────────┐
│   可视化结果     │ ← Matplotlib
└────────┬────────┘
         ▼
┌─────────────────┐
│   导出结果       │ ← QFileDialog + np.savetxt
└─────────────────┘
```

### 练习题

1. 创建一个光谱数据分析工具：
   - 导入CSV格式的光谱数据
   - 使用Savitzky-Golay滤波平滑
   - 自动寻峰并进行高斯拟合
   - 导出峰位置和强度

2. 创建一个批量数据处理器：
   - 选择多个数据文件
   - 使用多线程并行处理
   - 显示总体进度

---

## 下一章预告

[第六章：仪器通信基础](../ch06_communication/) - 学习串口和网络通信，为仪器控制做准备。

