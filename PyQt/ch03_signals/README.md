# 第三章：信号与槽机制

> 本章将深入学习PyQt的核心机制——信号与槽，掌握事件驱动编程模型

## 本章内容

- [3.1 信号与槽基础](#31-信号与槽基础)
- [3.2 连接内置信号](#32-连接内置信号)
- [3.3 自定义信号](#33-自定义信号)
- [3.4 信号传递参数](#34-信号传递参数)
- [3.5 Lambda表达式与信号](#35-lambda表达式与信号)

---

## 信号与槽概述

**信号与槽**（Signals and Slots）是Qt框架的核心特性，用于对象之间的通信。

### 基本概念

- **信号（Signal）**：当某个事件发生时发出的通知
- **槽（Slot）**：接收信号并执行响应的函数
- **连接（Connect）**：将信号与槽关联起来

```
┌──────────────┐    信号发出     ┌──────────────┐
│    发送者    │ ──────────────► │    接收者    │
│   (Sender)   │                 │  (Receiver)  │
│              │    clicked()    │              │
│  QPushButton ├────────────────►│  自定义槽    │
│              │                 │  on_click()  │
└──────────────┘                 └──────────────┘
```

### 为什么使用信号与槽？

1. **松耦合**：发送者不需要知道接收者是谁
2. **类型安全**：编译/运行时检查参数类型
3. **灵活性**：一个信号可连接多个槽，多个信号可连接同一个槽
4. **跨线程**：支持线程间安全通信

---

## 3.1 信号与槽基础

**示例程序**：[signal_slot_basic.py](signal_slot_basic.py)

### 基本语法

```python
# 连接信号与槽
sender.signal.connect(receiver.slot)

# 断开连接
sender.signal.disconnect(receiver.slot)

# 发出信号（自定义信号）
self.my_signal.emit()
```

### 简单示例

```python
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        button = QPushButton("点击我")
        
        # 连接按钮的clicked信号到自定义槽函数
        button.clicked.connect(self.on_button_clicked)
        
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)
    
    def on_button_clicked(self):
        """槽函数：响应按钮点击"""
        print("按钮被点击了！")
```

### 信号与槽的连接方式

```python
# 方式1：连接到实例方法
button.clicked.connect(self.on_click)

# 方式2：连接到普通函数
def handle_click():
    print("clicked")
button.clicked.connect(handle_click)

# 方式3：连接到Lambda表达式
button.clicked.connect(lambda: print("clicked"))

# 方式4：连接到另一个信号（信号链）
button.clicked.connect(another_button.click)
```

### 一对多连接

一个信号可以连接到多个槽，按连接顺序依次执行：

```python
button.clicked.connect(self.slot_1)
button.clicked.connect(self.slot_2)
button.clicked.connect(self.slot_3)
# 点击按钮时，依次执行 slot_1, slot_2, slot_3
```

### 多对一连接

多个信号可以连接到同一个槽：

```python
button1.clicked.connect(self.handle_click)
button2.clicked.connect(self.handle_click)
button3.clicked.connect(self.handle_click)
# 任意按钮点击都会调用 handle_click
```

---

## 3.2 连接内置信号

**示例程序**：[builtin_signals.py](builtin_signals.py)

### 常用控件的内置信号

| 控件 | 信号 | 触发时机 |
|------|------|----------|
| `QPushButton` | `clicked` | 按钮被点击 |
| `QPushButton` | `pressed` | 按钮被按下 |
| `QPushButton` | `released` | 按钮被释放 |
| `QLineEdit` | `textChanged` | 文本改变 |
| `QLineEdit` | `returnPressed` | 按下回车 |
| `QLineEdit` | `editingFinished` | 编辑完成（失去焦点） |
| `QSpinBox` | `valueChanged` | 值改变 |
| `QDoubleSpinBox` | `valueChanged` | 值改变 |
| `QComboBox` | `currentIndexChanged` | 选项改变 |
| `QComboBox` | `currentTextChanged` | 文本改变 |
| `QCheckBox` | `stateChanged` | 状态改变 |
| `QCheckBox` | `toggled` | 切换状态 |
| `QSlider` | `valueChanged` | 值改变 |
| `QSlider` | `sliderMoved` | 滑块移动 |
| `QSlider` | `sliderReleased` | 滑块释放 |

### QPushButton 信号示例

```python
button = QPushButton("测试")

# 点击信号（最常用）
button.clicked.connect(self.on_clicked)

# 按下信号
button.pressed.connect(self.on_pressed)

# 释放信号
button.released.connect(self.on_released)

# 切换信号（需要 setCheckable(True)）
button.setCheckable(True)
button.toggled.connect(self.on_toggled)
```

### QLineEdit 信号示例

```python
line_edit = QLineEdit()

# 文本改变时（每输入一个字符都会触发）
line_edit.textChanged.connect(self.on_text_changed)

# 按下回车时
line_edit.returnPressed.connect(self.on_return_pressed)

# 编辑完成时（失去焦点或按回车）
line_edit.editingFinished.connect(self.on_editing_finished)
```

### QSpinBox / QDoubleSpinBox 信号示例

```python
spin = QDoubleSpinBox()
spin.setRange(0, 100)

# 值改变时
spin.valueChanged.connect(self.on_value_changed)

def on_value_changed(self, value: float):
    print(f"新值: {value}")
```

### QComboBox 信号示例

```python
combo = QComboBox()
combo.addItems(["选项A", "选项B", "选项C"])

# 索引改变
combo.currentIndexChanged.connect(self.on_index_changed)

# 文本改变
combo.currentTextChanged.connect(self.on_text_changed)

def on_index_changed(self, index: int):
    print(f"选择了索引: {index}")

def on_text_changed(self, text: str):
    print(f"选择了: {text}")
```

### QSlider 信号示例

```python
slider = QSlider(Qt.Orientation.Horizontal)
slider.setRange(0, 100)

# 值改变（拖动或程序设置都会触发）
slider.valueChanged.connect(self.on_value_changed)

# 滑块移动（仅拖动时触发）
slider.sliderMoved.connect(self.on_slider_moved)

# 滑块释放（停止拖动时触发）
slider.sliderReleased.connect(self.on_slider_released)
```

---

## 3.3 自定义信号

**示例程序**：[custom_signal.py](custom_signal.py)

### 为什么需要自定义信号？

内置信号可能无法满足所有需求，例如：
- 需要传递特定类型的数据
- 需要在特定条件下触发
- 组件间通信需要自定义协议

### 定义自定义信号

使用 `pyqtSignal` 定义信号，必须作为**类属性**：

```python
from PyQt6.QtCore import pyqtSignal, QObject

class DataProcessor(QObject):
    # 定义信号（类属性）
    data_ready = pyqtSignal()              # 无参数信号
    progress_updated = pyqtSignal(int)     # 带int参数
    result_ready = pyqtSignal(str, float)  # 带多个参数
    
    def process(self):
        # 发出信号
        self.progress_updated.emit(50)
        
        # 处理完成
        self.result_ready.emit("完成", 3.14159)
```

### 信号参数类型

```python
from PyQt6.QtCore import pyqtSignal

class MyClass(QObject):
    # 无参数
    signal_void = pyqtSignal()
    
    # 基本类型
    signal_int = pyqtSignal(int)
    signal_float = pyqtSignal(float)
    signal_str = pyqtSignal(str)
    signal_bool = pyqtSignal(bool)
    
    # 多参数
    signal_multi = pyqtSignal(str, int, float)
    
    # 列表/字典
    signal_list = pyqtSignal(list)
    signal_dict = pyqtSignal(dict)
    
    # 自定义对象
    signal_object = pyqtSignal(object)
```

### 发出信号

```python
class TemperatureMonitor(QObject):
    """温度监测器示例"""
    
    # 定义信号
    temperature_changed = pyqtSignal(float)  # 温度变化
    alarm_triggered = pyqtSignal(str, float) # 报警（原因，温度）
    
    def __init__(self):
        super().__init__()
        self._temperature = 25.0
        self._threshold = 100.0
    
    def set_temperature(self, temp: float):
        """设置温度并发出相应信号"""
        self._temperature = temp
        
        # 发出温度变化信号
        self.temperature_changed.emit(temp)
        
        # 检查是否超过阈值
        if temp > self._threshold:
            self.alarm_triggered.emit("温度过高", temp)
```

### 连接自定义信号

```python
# 创建温度监测器
monitor = TemperatureMonitor()

# 连接信号到槽
monitor.temperature_changed.connect(self.update_display)
monitor.alarm_triggered.connect(self.show_alarm)

def update_display(self, temp: float):
    self.label.setText(f"当前温度: {temp:.1f}°C")

def show_alarm(self, reason: str, temp: float):
    print(f"警告: {reason}，当前温度 {temp:.1f}°C")
```

---

## 3.4 信号传递参数

**示例程序**：[signal_with_params.py](signal_with_params.py)

### 信号参数的传递

当信号携带参数时，连接的槽函数必须接收这些参数：

```python
class DataSource(QObject):
    data_received = pyqtSignal(str, float, int)
    
    def send_data(self):
        self.data_received.emit("传感器A", 25.5, 100)

# 槽函数必须接收相应参数
def on_data_received(name: str, value: float, count: int):
    print(f"{name}: {value}, 计数: {count}")

source = DataSource()
source.data_received.connect(on_data_received)
```

### 忽略部分参数

如果槽函数不需要所有参数，可以使用Lambda忽略：

```python
# 信号带3个参数，但槽函数只需要第一个
source.data_received.connect(lambda name, val, cnt: self.show_name(name))
```

### 信号重载（多种参数组合）

PyQt允许定义同名信号的不同参数版本：

```python
class MultiSignal(QObject):
    # 定义重载信号
    value_changed = pyqtSignal([int], [str], [int, str])
    
    def emit_int(self, value: int):
        self.value_changed[int].emit(value)
    
    def emit_str(self, value: str):
        self.value_changed[str].emit(value)
    
    def emit_both(self, num: int, text: str):
        self.value_changed[int, str].emit(num, text)
```

### 物理实验数据传递示例

```python
class Spectrometer(QObject):
    """光谱仪数据信号示例"""
    
    # 单点数据
    data_point = pyqtSignal(float, float)  # (波长, 强度)
    
    # 完整光谱
    spectrum_ready = pyqtSignal(list, list)  # (波长列表, 强度列表)
    
    # 测量状态
    measurement_status = pyqtSignal(dict)  # 状态字典
    
    def acquire_spectrum(self):
        wavelengths = [400, 450, 500, 550, 600]
        intensities = [0.2, 0.5, 0.8, 0.6, 0.3]
        
        # 发送每个数据点
        for wl, intensity in zip(wavelengths, intensities):
            self.data_point.emit(wl, intensity)
        
        # 发送完整光谱
        self.spectrum_ready.emit(wavelengths, intensities)
        
        # 发送状态
        self.measurement_status.emit({
            "points": len(wavelengths),
            "range": (400, 600),
            "complete": True
        })
```

---

## 3.5 Lambda表达式与信号

**示例程序**：[lambda_signals.py](lambda_signals.py)

### 为什么使用Lambda？

1. **传递额外参数**：当槽函数需要信号之外的参数时
2. **简化代码**：避免创建大量简单的槽函数
3. **灵活处理**：对信号参数进行转换或过滤

### Lambda基础用法

```python
# 无参数信号，调用需要参数的函数
button.clicked.connect(lambda: self.process_item(item_id))

# 忽略信号参数
slider.valueChanged.connect(lambda _: self.update_ui())

# 转换信号参数
spin.valueChanged.connect(lambda v: self.set_temperature(v * 0.1))
```

### 传递额外参数

```python
# 问题：如何知道是哪个按钮被点击？
for i in range(5):
    btn = QPushButton(f"按钮 {i}")
    # 错误！所有按钮都会传递 i=4（最后的值）
    # btn.clicked.connect(lambda: print(i))
    
    # 正确：使用默认参数捕获当前值
    btn.clicked.connect(lambda checked, idx=i: print(f"按钮 {idx} 被点击"))
```

### 常见Lambda模式

```python
# 1. 调用方法并传递固定参数
button.clicked.connect(lambda: self.open_file("config.ini"))

# 2. 更新标签显示
slider.valueChanged.connect(lambda v: label.setText(f"值: {v}"))

# 3. 条件执行
checkbox.toggled.connect(lambda checked: widget.setEnabled(checked))

# 4. 多步操作
button.clicked.connect(lambda: (self.save_data(), self.update_ui()))

# 5. 信号参数转换
spin_celsius.valueChanged.connect(
    lambda c: spin_fahrenheit.setValue(c * 9/5 + 32)
)
```

### 使用functools.partial替代Lambda

对于复杂情况，`functools.partial`可能更清晰：

```python
from functools import partial

def handle_button(button_id: int, action: str):
    print(f"按钮 {button_id}: {action}")

# 使用partial
button.clicked.connect(partial(handle_button, 1, "click"))

# 等价的Lambda
button.clicked.connect(lambda: handle_button(1, "click"))
```

### 注意事项

1. **避免在循环中直接使用变量**：

```python
# 错误
for i in range(3):
    buttons[i].clicked.connect(lambda: print(i))  # 都会打印2

# 正确
for i in range(3):
    buttons[i].clicked.connect(lambda _, idx=i: print(idx))
```

2. **Lambda中的self引用**：

```python
# Lambda会保持对self的引用，可能导致对象无法被垃圾回收
# 如果担心内存泄漏，使用weakref或在适当时机断开连接
```

---

## 信号槽高级用法

### 使用装饰器@pyqtSlot

装饰器可以明确标记槽函数，提供类型检查：

```python
from PyQt6.QtCore import pyqtSlot

class MyWidget(QWidget):
    @pyqtSlot()
    def on_button_clicked(self):
        """无参数槽"""
        pass
    
    @pyqtSlot(int)
    def on_value_changed(self, value: int):
        """接收int参数的槽"""
        pass
    
    @pyqtSlot(str, result=bool)
    def validate_input(self, text: str) -> bool:
        """带返回值的槽"""
        return len(text) > 0
```

### 断开信号连接

```python
# 断开特定连接
button.clicked.disconnect(self.on_click)

# 断开信号的所有连接
button.clicked.disconnect()

# 安全断开（可能未连接时）
try:
    button.clicked.disconnect(self.on_click)
except TypeError:
    pass  # 未连接时会抛出异常
```

### 阻塞信号

临时阻止信号发出，避免循环触发：

```python
# 阻塞信号
spin.blockSignals(True)
spin.setValue(50)  # 不会触发valueChanged
spin.blockSignals(False)

# 使用上下文管理器（自定义）
class SignalBlocker:
    def __init__(self, widget):
        self.widget = widget
    
    def __enter__(self):
        self.widget.blockSignals(True)
        return self
    
    def __exit__(self, *args):
        self.widget.blockSignals(False)

# 使用
with SignalBlocker(spin):
    spin.setValue(50)
```

### 信号连接的自动断开

当接收者被销毁时，连接会自动断开。但Lambda连接需要手动管理：

```python
# 保存连接以便后续断开
self._connections = []
conn = button.clicked.connect(lambda: self.do_something())
self._connections.append((button.clicked, conn))

# 清理时断开
def cleanup(self):
    for signal, slot in self._connections:
        signal.disconnect(slot)
```

---

## 本章小结

通过本章学习，你应该掌握了：

1. **信号与槽基础**：connect/disconnect/emit的使用
2. **内置信号**：各种控件的常用信号
3. **自定义信号**：pyqtSignal的定义和发出
4. **参数传递**：信号携带数据的处理
5. **Lambda技巧**：灵活的信号处理方式

### 信号槽使用建议

| 场景 | 建议 |
|------|------|
| 简单响应 | 直接连接到实例方法 |
| 需要额外参数 | 使用Lambda或partial |
| 复杂数据传递 | 自定义信号+自定义类型 |
| 跨线程通信 | 信号槽（自动队列连接） |
| 多个控件相同处理 | sender()识别发送者 |

### 练习题

1. 创建一个温度转换器界面：
   - 输入摄氏度，自动计算并显示华氏度
   - 使用信号槽实现实时联动

2. 创建一个简单的事件日志系统：
   - 多个按钮触发不同事件
   - 自定义信号传递事件信息
   - 日志区域显示所有事件

---

## 下一章预告

[第四章：Matplotlib科研绑图集成](../ch04_plotting/) - 学习如何在PyQt中嵌入Matplotlib，实现交互式科研数据可视化。

