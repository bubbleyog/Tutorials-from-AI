# 第一章：PyQt基础入门

> 本章将带你了解PyQt的核心概念，完成环境配置，并编写第一个GUI程序

## 本章内容

- [1.1 环境安装与配置](#11-环境安装与配置)
- [1.2 PyQt架构与核心概念](#12-pyqt架构与核心概念)
- [1.3 第一个PyQt窗口](#13-第一个pyqt窗口)
- [1.4 常用控件详解](#14-常用控件详解)
- [1.5 控件属性与方法](#15-控件属性与方法)

---

## 1.1 环境安装与配置

### 安装PyQt6

PyQt6是Qt框架的Python绑定，提供了强大的跨平台GUI开发能力。

```bash
# 确保Python版本 >= 3.10
python --version

# 安装PyQt6
pip install PyQt6

# 安装科学计算相关包（本教程需要）
pip install numpy matplotlib scipy pyserial
```

### 验证安装

运行以下脚本检查环境是否配置正确：

```bash
python install_check.py
```

**示例程序**：[install_check.py](install_check.py)

```python
"""检查PyQt6及相关包是否正确安装"""
import sys

def check_package(name: str) -> bool:
    """检查包是否可导入"""
    try:
        __import__(name)
        return True
    except ImportError:
        return False

# 检查必要的包
packages = {
    "PyQt6": "PyQt6",
    "NumPy": "numpy", 
    "Matplotlib": "matplotlib",
    "SciPy": "scipy",
    "PySerial": "serial"
}

print("=" * 50)
print("PyQt科研应用教程 - 环境检查")
print("=" * 50)

all_ok = True
for display_name, import_name in packages.items():
    status = "✓ 已安装" if check_package(import_name) else "✗ 未安装"
    if "未安装" in status:
        all_ok = False
    print(f"{display_name:15} {status}")

print("=" * 50)
if all_ok:
    print("环境配置完成，可以开始学习！")
else:
    print("请安装缺失的包：pip install -r requirements.txt")
```

---

## 1.2 PyQt架构与核心概念

### Qt与PyQt的关系

- **Qt**：由Qt公司开发的跨平台C++ GUI框架
- **PyQt**：Qt的Python绑定，由Riverbank Computing开发
- **PyQt6**：对应Qt6版本，是目前最新的主要版本

### 核心组件

#### 1. QApplication - 应用程序对象

每个PyQt程序必须创建一个`QApplication`实例，它负责：
- 管理应用程序的控制流和主要设置
- 处理系统事件
- 管理应用程序范围的资源

```python
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)  # 创建应用程序对象
# ... 创建窗口和控件 ...
sys.exit(app.exec())  # 进入事件循环
```

#### 2. QWidget - 基础控件类

`QWidget`是所有用户界面对象的基类：
- 可以接收鼠标、键盘和其他系统事件
- 可以在屏幕上绑制自己
- 可以包含其他控件（作为容器）

#### 3. QMainWindow - 主窗口类

`QMainWindow`提供了标准的主窗口结构：
- 菜单栏（Menu Bar）
- 工具栏（Tool Bars）
- 状态栏（Status Bar）
- 中央控件区（Central Widget）
- 停靠窗口区（Dock Widgets）

```
┌─────────────────────────────────────┐
│           菜单栏 (Menu Bar)          │
├─────────────────────────────────────┤
│           工具栏 (Tool Bar)          │
├─────────────────────────────────────┤
│                                     │
│                                     │
│        中央控件 (Central Widget)      │
│                                     │
│                                     │
├─────────────────────────────────────┤
│          状态栏 (Status Bar)         │
└─────────────────────────────────────┘
```

### 事件循环

PyQt程序运行在一个**事件循环**中：

1. 程序启动，进入`app.exec()`
2. 等待事件发生（用户点击、键盘输入、定时器等）
3. 事件被分发到对应的控件
4. 控件处理事件（调用槽函数）
5. 返回步骤2，继续等待

```
     ┌──────────────┐
     │   程序启动    │
     └──────┬───────┘
            ▼
     ┌──────────────┐
┌───►│   等待事件    │◄──────────────┐
│    └──────┬───────┘               │
│           ▼                       │
│    ┌──────────────┐               │
│    │   事件发生    │               │
│    └──────┬───────┘               │
│           ▼                       │
│    ┌──────────────┐               │
│    │  分发到控件   │               │
│    └──────┬───────┘               │
│           ▼                       │
│    ┌──────────────┐               │
│    │   处理事件    │───────────────┘
│    └──────┬───────┘
│           │ (程序退出)
│           ▼
│    ┌──────────────┐
└────│   程序结束    │
     └──────────────┘
```

---

## 1.3 第一个PyQt窗口

让我们创建一个简单的窗口程序来熟悉PyQt的基本结构。

**示例程序**：[first_window.py](first_window.py)

### 最简窗口

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget

# 1. 创建应用程序对象
app = QApplication(sys.argv)

# 2. 创建窗口
window = QWidget()
window.setWindowTitle("我的第一个PyQt窗口")
window.setGeometry(100, 100, 400, 300)  # x, y, width, height

# 3. 显示窗口
window.show()

# 4. 进入事件循环
sys.exit(app.exec())
```

### 使用类封装窗口

在实际开发中，我们通常使用类来组织代码：

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt


class FirstWindow(QWidget):
    """第一个PyQt窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle("PyQt6 入门示例")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建标签
        label = QLabel("欢迎学习PyQt编程！", self)
        label.setGeometry(100, 50, 200, 30)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建按钮
        button = QPushButton("点击我", self)
        button.setGeometry(150, 120, 100, 40)
        button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        """按钮点击事件处理"""
        print("按钮被点击了！")


def main():
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### 代码解析

| 代码 | 说明 |
|------|------|
| `super().__init__()` | 调用父类构造函数，初始化QWidget |
| `setWindowTitle()` | 设置窗口标题 |
| `setGeometry(x, y, w, h)` | 设置窗口位置和大小 |
| `QLabel("文本", self)` | 创建标签，`self`指定父控件 |
| `button.clicked.connect()` | 连接按钮点击信号到槽函数 |

### 运行效果

```bash
python first_window.py
```

你将看到一个带有标签和按钮的窗口，点击按钮会在控制台输出信息。

---

## 1.4 常用控件详解

PyQt提供了丰富的控件，本节介绍物理研究中最常用的几种。

**示例程序**：[basic_widgets.py](basic_widgets.py)

### 控件概览

| 控件类 | 用途 | 物理应用场景 |
|--------|------|-------------|
| `QLabel` | 显示文本或图片 | 显示参数名称、单位 |
| `QPushButton` | 按钮 | 开始测量、停止采集 |
| `QLineEdit` | 单行文本输入 | 输入文件名、备注 |
| `QSpinBox` | 整数输入框 | 采样点数、平均次数 |
| `QDoubleSpinBox` | 浮点数输入框 | 频率、电压、温度设定 |
| `QComboBox` | 下拉选择框 | 选择量程、通道 |
| `QCheckBox` | 复选框 | 启用/禁用功能 |
| `QSlider` | 滑动条 | 调节参数值 |

### QLabel - 标签

```python
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

# 创建标签
label = QLabel("电压 (V):", self)

# 设置对齐方式
label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

# 设置样式
label.setStyleSheet("font-size: 14px; color: #333;")
```

### QPushButton - 按钮

```python
from PyQt6.QtWidgets import QPushButton

# 创建按钮
btn_start = QPushButton("开始测量", self)
btn_stop = QPushButton("停止", self)

# 设置启用/禁用状态
btn_stop.setEnabled(False)

# 连接点击信号
btn_start.clicked.connect(self.start_measurement)
```

### QLineEdit - 单行输入框

```python
from PyQt6.QtWidgets import QLineEdit

# 创建输入框
input_name = QLineEdit(self)

# 设置占位符文本
input_name.setPlaceholderText("请输入样品名称...")

# 获取输入内容
text = input_name.text()

# 文本变化信号
input_name.textChanged.connect(self.on_text_changed)
```

### QSpinBox / QDoubleSpinBox - 数值输入框

```python
from PyQt6.QtWidgets import QSpinBox, QDoubleSpinBox

# 整数输入框
spin_points = QSpinBox(self)
spin_points.setRange(1, 10000)      # 范围
spin_points.setValue(100)           # 默认值
spin_points.setSuffix(" 点")        # 后缀

# 浮点数输入框（更常用于物理参数）
spin_freq = QDoubleSpinBox(self)
spin_freq.setRange(0.1, 1000.0)     # 范围
spin_freq.setValue(10.0)            # 默认值
spin_freq.setDecimals(2)            # 小数位数
spin_freq.setSuffix(" Hz")          # 后缀
spin_freq.setSingleStep(0.1)        # 步进值

# 值变化信号
spin_freq.valueChanged.connect(self.on_freq_changed)
```

### QComboBox - 下拉选择框

```python
from PyQt6.QtWidgets import QComboBox

# 创建下拉框
combo_range = QComboBox(self)

# 添加选项
combo_range.addItems(["1V", "10V", "100V", "1000V"])

# 获取当前选择
current_text = combo_range.currentText()    # "10V"
current_index = combo_range.currentIndex()  # 1

# 选择变化信号
combo_range.currentIndexChanged.connect(self.on_range_changed)
```

### QCheckBox - 复选框

```python
from PyQt6.QtWidgets import QCheckBox

# 创建复选框
check_auto = QCheckBox("自动量程", self)

# 设置选中状态
check_auto.setChecked(True)

# 获取状态
is_checked = check_auto.isChecked()  # True/False

# 状态变化信号
check_auto.stateChanged.connect(self.on_auto_changed)
```

### QSlider - 滑动条

```python
from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt

# 创建水平滑动条
slider = QSlider(Qt.Orientation.Horizontal, self)

# 设置范围和值
slider.setRange(0, 100)
slider.setValue(50)

# 设置刻度
slider.setTickPosition(QSlider.TickPosition.TicksBelow)
slider.setTickInterval(10)

# 值变化信号
slider.valueChanged.connect(self.on_slider_changed)
```

### 综合示例

```python
class WidgetDemo(QWidget):
    """控件演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("常用控件演示")
        self.setGeometry(100, 100, 400, 350)
        
        # 标签
        QLabel("频率:", self).move(20, 20)
        
        # 浮点数输入框
        self.spin_freq = QDoubleSpinBox(self)
        self.spin_freq.setGeometry(80, 15, 120, 30)
        self.spin_freq.setRange(0.1, 1000.0)
        self.spin_freq.setValue(10.0)
        self.spin_freq.setSuffix(" Hz")
        
        # 下拉框
        QLabel("量程:", self).move(20, 60)
        self.combo_range = QComboBox(self)
        self.combo_range.setGeometry(80, 55, 120, 30)
        self.combo_range.addItems(["1V", "10V", "100V"])
        
        # 复选框
        self.check_auto = QCheckBox("自动保存数据", self)
        self.check_auto.move(20, 100)
        
        # 按钮
        self.btn_start = QPushButton("开始", self)
        self.btn_start.setGeometry(80, 150, 100, 35)
        self.btn_start.clicked.connect(self.on_start)
    
    def on_start(self):
        freq = self.spin_freq.value()
        range_val = self.combo_range.currentText()
        auto_save = self.check_auto.isChecked()
        print(f"频率: {freq} Hz, 量程: {range_val}, 自动保存: {auto_save}")
```

---

## 1.5 控件属性与方法

本节深入介绍控件的通用属性和方法。

**示例程序**：[widget_properties.py](widget_properties.py)

### 通用属性

所有继承自`QWidget`的控件都具有以下通用属性：

#### 大小与位置

```python
# 设置位置和大小（绝对定位）
widget.setGeometry(x, y, width, height)

# 仅设置位置
widget.move(x, y)

# 仅设置大小
widget.resize(width, height)

# 设置固定大小（不可调整）
widget.setFixedSize(width, height)

# 设置最小/最大大小
widget.setMinimumSize(min_w, min_h)
widget.setMaximumSize(max_w, max_h)

# 获取大小
size = widget.size()
width = widget.width()
height = widget.height()
```

#### 可见性与启用状态

```python
# 显示/隐藏控件
widget.show()
widget.hide()
widget.setVisible(True)  # 等同于 show()

# 启用/禁用控件
widget.setEnabled(True)   # 启用
widget.setEnabled(False)  # 禁用（灰色不可交互）

# 检查状态
is_visible = widget.isVisible()
is_enabled = widget.isEnabled()
```

#### 样式设置

```python
# 使用CSS样式表
widget.setStyleSheet("""
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
    color: #333;
""")

# 设置字体
from PyQt6.QtGui import QFont
font = QFont("微软雅黑", 12)
font.setBold(True)
widget.setFont(font)
```

#### 提示信息

```python
# 设置工具提示（鼠标悬停显示）
widget.setToolTip("这是一个频率输入框，范围：0.1-1000 Hz")

# 设置状态栏提示（需要在QMainWindow中）
widget.setStatusTip("输入测量频率")

# 设置"这是什么"帮助
widget.setWhatsThis("详细的帮助信息...")
```

### 物理实验参数输入面板示例

```python
class ParameterPanel(QWidget):
    """实验参数输入面板"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("实验参数设置")
        self.setFixedSize(350, 400)
        self.init_ui()
    
    def init_ui(self):
        # === 温度设置 ===
        lbl_temp = QLabel("目标温度:", self)
        lbl_temp.setGeometry(20, 20, 80, 25)
        
        self.spin_temp = QDoubleSpinBox(self)
        self.spin_temp.setGeometry(110, 20, 120, 25)
        self.spin_temp.setRange(4.0, 400.0)
        self.spin_temp.setValue(300.0)
        self.spin_temp.setSuffix(" K")
        self.spin_temp.setDecimals(1)
        self.spin_temp.setToolTip("设置目标温度 (4K - 400K)")
        
        # === 磁场设置 ===
        lbl_field = QLabel("磁场强度:", self)
        lbl_field.setGeometry(20, 60, 80, 25)
        
        self.spin_field = QDoubleSpinBox(self)
        self.spin_field.setGeometry(110, 60, 120, 25)
        self.spin_field.setRange(0.0, 14.0)
        self.spin_field.setValue(0.0)
        self.spin_field.setSuffix(" T")
        self.spin_field.setDecimals(3)
        
        # === 扫描模式 ===
        lbl_mode = QLabel("扫描模式:", self)
        lbl_mode.setGeometry(20, 100, 80, 25)
        
        self.combo_mode = QComboBox(self)
        self.combo_mode.setGeometry(110, 100, 120, 25)
        self.combo_mode.addItems(["连续扫描", "步进扫描", "单点测量"])
        
        # === 采样设置 ===
        lbl_points = QLabel("采样点数:", self)
        lbl_points.setGeometry(20, 140, 80, 25)
        
        self.spin_points = QSpinBox(self)
        self.spin_points.setGeometry(110, 140, 120, 25)
        self.spin_points.setRange(10, 10000)
        self.spin_points.setValue(1000)
        
        # === 选项 ===
        self.check_avg = QCheckBox("启用平均", self)
        self.check_avg.setGeometry(20, 180, 100, 25)
        self.check_avg.setChecked(True)
        
        self.check_log = QCheckBox("记录日志", self)
        self.check_log.setGeometry(130, 180, 100, 25)
        
        # === 备注 ===
        lbl_note = QLabel("备注:", self)
        lbl_note.setGeometry(20, 220, 80, 25)
        
        self.input_note = QLineEdit(self)
        self.input_note.setGeometry(110, 220, 200, 25)
        self.input_note.setPlaceholderText("输入实验备注...")
        
        # === 按钮 ===
        self.btn_apply = QPushButton("应用设置", self)
        self.btn_apply.setGeometry(60, 280, 100, 35)
        self.btn_apply.clicked.connect(self.apply_settings)
        
        self.btn_reset = QPushButton("重置", self)
        self.btn_reset.setGeometry(180, 280, 100, 35)
        self.btn_reset.clicked.connect(self.reset_settings)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel { font-size: 13px; }
            QPushButton { 
                font-size: 13px; 
                background-color: #4a90d9;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #357abd; }
            QPushButton:pressed { background-color: #2a5f8f; }
        """)
    
    def apply_settings(self):
        """应用当前设置"""
        settings = {
            "temperature": self.spin_temp.value(),
            "magnetic_field": self.spin_field.value(),
            "scan_mode": self.combo_mode.currentText(),
            "sample_points": self.spin_points.value(),
            "averaging": self.check_avg.isChecked(),
            "logging": self.check_log.isChecked(),
            "note": self.input_note.text()
        }
        print("应用设置:")
        for key, value in settings.items():
            print(f"  {key}: {value}")
    
    def reset_settings(self):
        """重置为默认值"""
        self.spin_temp.setValue(300.0)
        self.spin_field.setValue(0.0)
        self.combo_mode.setCurrentIndex(0)
        self.spin_points.setValue(1000)
        self.check_avg.setChecked(True)
        self.check_log.setChecked(False)
        self.input_note.clear()
        print("设置已重置")
```

### 键盘快捷键

```python
from PyQt6.QtGui import QShortcut, QKeySequence

# 创建快捷键
shortcut_start = QShortcut(QKeySequence("Ctrl+S"), self)
shortcut_start.activated.connect(self.start_measurement)

shortcut_quit = QShortcut(QKeySequence("Ctrl+Q"), self)
shortcut_quit.activated.connect(self.close)
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **环境配置**：安装PyQt6及相关科学计算包
2. **核心概念**：QApplication、QWidget、事件循环
3. **窗口创建**：使用类封装窗口，组织代码结构
4. **常用控件**：标签、按钮、输入框、下拉框、复选框等
5. **控件属性**：大小、位置、样式、启用状态等

### 练习题

1. 创建一个窗口，包含两个`QDoubleSpinBox`用于输入质量和速度，点击按钮计算动能 $E_k = \frac{1}{2}mv^2$

2. 创建一个"光谱采集参数"面板，包含：
   - 起始波长/终止波长（QDoubleSpinBox）
   - 积分时间（QSpinBox）
   - 平均次数（QSpinBox）
   - 狭缝宽度选择（QComboBox）

---

## 下一章预告

[第二章：布局管理与界面设计](../ch02_layout/) - 学习如何使用布局管理器创建美观、自适应的界面。

