# 第二章：布局管理与界面设计

> 本章将学习PyQt的布局系统，掌握创建美观、自适应界面的技巧

## 本章内容

- [2.1 水平与垂直布局](#21-水平与垂直布局)
- [2.2 网格布局](#22-网格布局)
- [2.3 表单布局](#23-表单布局)
- [2.4 嵌套布局与复杂界面](#24-嵌套布局与复杂界面)
- [2.5 分组框与标签页](#25-分组框与标签页)
- [2.6 使用Qt Designer设计界面](#26-使用qt-designer设计界面)

---

## 为什么需要布局管理器？

在第一章中，我们使用`setGeometry(x, y, w, h)`来定位控件，这种**绝对定位**方式有明显缺点：

1. **窗口大小改变时**，控件位置和大小不会自动调整
2. **不同分辨率屏幕**上显示效果不一致
3. **维护困难**，添加或删除控件需要重新计算位置

**布局管理器**（Layout Manager）可以自动管理控件的位置和大小，是PyQt界面开发的核心技术。

---

## 2.1 水平与垂直布局

**示例程序**：[hbox_vbox_demo.py](hbox_vbox_demo.py)

### QHBoxLayout - 水平布局

将控件从左到右水平排列。

```python
from PyQt6.QtWidgets import QHBoxLayout, QPushButton

layout = QHBoxLayout()
layout.addWidget(QPushButton("按钮1"))
layout.addWidget(QPushButton("按钮2"))
layout.addWidget(QPushButton("按钮3"))
```

```
┌─────────────────────────────────────────┐
│  [按钮1]    [按钮2]    [按钮3]           │
└─────────────────────────────────────────┘
```

### QVBoxLayout - 垂直布局

将控件从上到下垂直排列。

```python
from PyQt6.QtWidgets import QVBoxLayout, QPushButton

layout = QVBoxLayout()
layout.addWidget(QPushButton("按钮1"))
layout.addWidget(QPushButton("按钮2"))
layout.addWidget(QPushButton("按钮3"))
```

```
┌───────────────┐
│   [按钮1]     │
│   [按钮2]     │
│   [按钮3]     │
└───────────────┘
```

### 布局常用方法

| 方法 | 说明 |
|------|------|
| `addWidget(widget)` | 添加控件 |
| `addLayout(layout)` | 添加子布局（嵌套） |
| `addStretch(n)` | 添加弹性空间，n为权重 |
| `addSpacing(px)` | 添加固定间距（像素） |
| `setSpacing(px)` | 设置控件间的默认间距 |
| `setContentsMargins(l, t, r, b)` | 设置布局边距 |

### 弹性空间 addStretch

`addStretch()`用于创建可伸缩的空白区域，实现灵活的控件对齐：

```python
# 按钮靠右对齐
layout = QHBoxLayout()
layout.addStretch(1)      # 左边填充弹性空间
layout.addWidget(btn_ok)
layout.addWidget(btn_cancel)
```

```
┌────────────────────────────────────────┐
│                        [确定] [取消]    │
└────────────────────────────────────────┘
```

```python
# 按钮居中对齐
layout = QHBoxLayout()
layout.addStretch(1)
layout.addWidget(btn_ok)
layout.addWidget(btn_cancel)
layout.addStretch(1)      # 两边都有弹性空间
```

```
┌────────────────────────────────────────┐
│           [确定] [取消]                 │
└────────────────────────────────────────┘
```

### 控件对齐

可以在`addWidget`时指定对齐方式：

```python
from PyQt6.QtCore import Qt

layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
layout.addWidget(input, alignment=Qt.AlignmentFlag.AlignRight)
```

常用对齐标志：
- `Qt.AlignmentFlag.AlignLeft` / `AlignRight` / `AlignHCenter`
- `Qt.AlignmentFlag.AlignTop` / `AlignBottom` / `AlignVCenter`
- `Qt.AlignmentFlag.AlignCenter` (水平+垂直居中)

---

## 2.2 网格布局

**示例程序**：[grid_layout_demo.py](grid_layout_demo.py)

### QGridLayout - 网格布局

将控件放置在行列网格中，适合创建计算器、参数表格等界面。

```python
from PyQt6.QtWidgets import QGridLayout, QLabel, QLineEdit

layout = QGridLayout()
#                        控件           行  列
layout.addWidget(QLabel("姓名:"),       0,  0)
layout.addWidget(QLineEdit(),           0,  1)
layout.addWidget(QLabel("年龄:"),       1,  0)
layout.addWidget(QLineEdit(),           1,  1)
```

```
┌──────────────────────────┐
│  姓名: [__________]      │
│  年龄: [__________]      │
└──────────────────────────┘
```

### 跨行跨列

使用额外参数实现单元格合并：

```python
# addWidget(widget, row, col, rowSpan, colSpan)
layout.addWidget(title_label, 0, 0, 1, 2)  # 第0行，跨2列
layout.addWidget(big_button, 1, 0, 2, 1)   # 第1行，跨2行
```

```
┌─────────────────────────────┐
│      标题（跨2列）           │
├──────────┬──────────────────┤
│          │   控件A          │
│ 大按钮   ├──────────────────┤
│（跨2行） │   控件B          │
└──────────┴──────────────────┘
```

### 设置行列比例

```python
# 设置列的拉伸比例
layout.setColumnStretch(0, 1)  # 第0列，权重1
layout.setColumnStretch(1, 2)  # 第1列，权重2（宽度是第0列的2倍）

# 设置行的拉伸比例
layout.setRowStretch(0, 1)
layout.setRowStretch(1, 1)
```

### 物理计算器示例

```python
class PhysicsCalculator(QWidget):
    """简单的物理公式计算器布局"""
    
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        
        # 第0行：公式选择
        layout.addWidget(QLabel("公式:"), 0, 0)
        self.combo_formula = QComboBox()
        self.combo_formula.addItems(["动能 E=½mv²", "动量 p=mv", "波长 λ=h/p"])
        layout.addWidget(self.combo_formula, 0, 1, 1, 2)
        
        # 第1行：输入参数1
        layout.addWidget(QLabel("质量 m:"), 1, 0)
        self.spin_mass = QDoubleSpinBox()
        self.spin_mass.setSuffix(" kg")
        layout.addWidget(self.spin_mass, 1, 1)
        
        # 第2行：输入参数2
        layout.addWidget(QLabel("速度 v:"), 2, 0)
        self.spin_velocity = QDoubleSpinBox()
        self.spin_velocity.setSuffix(" m/s")
        layout.addWidget(self.spin_velocity, 2, 1)
        
        # 第3行：计算按钮（跨2列）
        self.btn_calc = QPushButton("计算")
        layout.addWidget(self.btn_calc, 3, 0, 1, 2)
        
        # 第4行：结果显示
        layout.addWidget(QLabel("结果:"), 4, 0)
        self.label_result = QLabel("--")
        layout.addWidget(self.label_result, 4, 1)
        
        self.setLayout(layout)
```

---

## 2.3 表单布局

**示例程序**：[form_layout_demo.py](form_layout_demo.py)

### QFormLayout - 表单布局

专为"标签-控件"配对设计，自动对齐标签和输入控件。

```python
from PyQt6.QtWidgets import QFormLayout, QLineEdit, QDoubleSpinBox

layout = QFormLayout()
layout.addRow("样品名称:", QLineEdit())
layout.addRow("温度 (K):", QDoubleSpinBox())
layout.addRow("磁场 (T):", QDoubleSpinBox())
```

```
┌─────────────────────────────┐
│    样品名称:  [__________]  │
│    温度 (K):  [__________]  │
│    磁场 (T):  [__________]  │
└─────────────────────────────┘
```

### 表单布局的优势

1. **自动对齐**：标签右对齐，控件左对齐
2. **代码简洁**：`addRow(label, widget)`一行搞定
3. **语义清晰**：明确的标签-控件配对关系

### 表单选项

```python
# 设置标签对齐方式
layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

# 设置行的包装策略
layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)

# 设置字段增长策略
layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
```

### 实验参数表单示例

```python
class ExperimentForm(QWidget):
    """实验参数输入表单"""
    
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layout.setSpacing(12)
        
        # 样品信息
        self.input_sample = QLineEdit()
        self.input_sample.setPlaceholderText("例如: YBa2Cu3O7")
        layout.addRow("样品名称:", self.input_sample)
        
        # 温度范围
        self.spin_temp_start = QDoubleSpinBox()
        self.spin_temp_start.setRange(1.5, 400)
        self.spin_temp_start.setValue(2.0)
        self.spin_temp_start.setSuffix(" K")
        layout.addRow("起始温度:", self.spin_temp_start)
        
        self.spin_temp_end = QDoubleSpinBox()
        self.spin_temp_end.setRange(1.5, 400)
        self.spin_temp_end.setValue(300.0)
        self.spin_temp_end.setSuffix(" K")
        layout.addRow("终止温度:", self.spin_temp_end)
        
        # 测量模式
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["ZFC", "FC", "ZFC-FC"])
        layout.addRow("测量模式:", self.combo_mode)
        
        self.setLayout(layout)
```

---

## 2.4 嵌套布局与复杂界面

**示例程序**：[nested_layout.py](nested_layout.py)

### 嵌套布局原理

复杂界面通常由多个简单布局**嵌套**组成。使用`addLayout()`将一个布局添加到另一个布局中。

```python
# 主垂直布局
main_layout = QVBoxLayout()

# 顶部水平布局
top_layout = QHBoxLayout()
top_layout.addWidget(QLabel("标题"))
top_layout.addStretch()
top_layout.addWidget(QPushButton("设置"))

# 将顶部布局添加到主布局
main_layout.addLayout(top_layout)

# 中间网格布局
grid_layout = QGridLayout()
# ... 添加控件 ...
main_layout.addLayout(grid_layout)

# 底部按钮布局
bottom_layout = QHBoxLayout()
bottom_layout.addStretch()
bottom_layout.addWidget(QPushButton("确定"))
bottom_layout.addWidget(QPushButton("取消"))
main_layout.addLayout(bottom_layout)
```

### 典型界面结构

```
┌─────────────────────────────────────────┐
│  ┌─────────────────────────────────┐    │  ← 顶部栏 (HBox)
│  │ 标题             [设置] [帮助]  │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │                                 │    │  ← 主内容区 (Grid/VBox)
│  │     主要内容区域                 │    │
│  │                                 │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │  ← 底部按钮栏 (HBox)
│  │               [确定] [取消]     │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### 数据采集界面示例

```python
class DataAcquisitionUI(QWidget):
    """数据采集界面 - 嵌套布局示例"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # ===== 主布局（垂直）=====
        main_layout = QVBoxLayout()
        
        # ===== 顶部：标题栏 =====
        title_layout = QHBoxLayout()
        title_label = QLabel("数据采集系统")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(QPushButton("⚙ 设置"))
        main_layout.addLayout(title_layout)
        
        # ===== 中部：参数+图表（水平分割）=====
        content_layout = QHBoxLayout()
        
        # 左侧：参数面板
        params_layout = QFormLayout()
        params_layout.addRow("采样率:", QDoubleSpinBox())
        params_layout.addRow("采样点数:", QSpinBox())
        params_layout.addRow("触发模式:", QComboBox())
        
        params_group = QGroupBox("采集参数")
        params_group.setLayout(params_layout)
        params_group.setFixedWidth(200)
        content_layout.addWidget(params_group)
        
        # 右侧：图表区域（占位）
        chart_placeholder = QLabel("📊 实时波形显示区域")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet(
            "background-color: #2c3e50; color: white; "
            "border-radius: 5px; font-size: 16px;"
        )
        chart_placeholder.setMinimumHeight(300)
        content_layout.addWidget(chart_placeholder, stretch=1)
        
        main_layout.addLayout(content_layout)
        
        # ===== 底部：控制按钮 =====
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton("▶ 开始"))
        button_layout.addWidget(QPushButton("⏸ 暂停"))
        button_layout.addWidget(QPushButton("⏹ 停止"))
        button_layout.addStretch()
        button_layout.addWidget(QPushButton("导出数据"))
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
```

---

## 2.5 分组框与标签页

**示例程序**：[groupbox_tabs.py](groupbox_tabs.py)

### QGroupBox - 分组框

将相关控件分组显示，带有标题和边框。

```python
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout

# 创建分组框
group = QGroupBox("温度设置")

# 分组框内部布局
group_layout = QVBoxLayout()
group_layout.addWidget(QLabel("当前温度: 300 K"))
group_layout.addWidget(QDoubleSpinBox())
group_layout.addWidget(QPushButton("设置"))

# 将布局应用到分组框
group.setLayout(group_layout)
```

```
┌─ 温度设置 ─────────────────┐
│  当前温度: 300 K           │
│  [        300.0 ▼    ] K   │
│  [      设置      ]        │
└────────────────────────────┘
```

### 可折叠分组框

```python
group = QGroupBox("高级选项")
group.setCheckable(True)   # 添加复选框
group.setChecked(False)    # 默认折叠（内部控件禁用）
```

### QTabWidget - 标签页

将多个页面组织在标签页中，节省空间。

```python
from PyQt6.QtWidgets import QTabWidget, QWidget

# 创建标签页控件
tabs = QTabWidget()

# 创建各个页面
page1 = QWidget()
page1_layout = QVBoxLayout(page1)
page1_layout.addWidget(QLabel("这是第一页"))

page2 = QWidget()
page2_layout = QVBoxLayout(page2)
page2_layout.addWidget(QLabel("这是第二页"))

# 添加页面到标签页
tabs.addTab(page1, "基本设置")
tabs.addTab(page2, "高级设置")
```

```
┌──────────────┬──────────────┬──────────┐
│  基本设置    │  高级设置    │          │
├──────────────┴──────────────┴──────────┤
│                                        │
│      当前页面内容                       │
│                                        │
└────────────────────────────────────────┘
```

### 带图标的标签页

```python
from PyQt6.QtGui import QIcon

tabs.addTab(page1, QIcon("icons/settings.png"), "设置")
tabs.addTab(page2, QIcon("icons/chart.png"), "图表")
```

### 标签页常用属性

```python
# 设置标签位置
tabs.setTabPosition(QTabWidget.TabPosition.North)  # 上方（默认）
tabs.setTabPosition(QTabWidget.TabPosition.South)  # 下方
tabs.setTabPosition(QTabWidget.TabPosition.West)   # 左侧
tabs.setTabPosition(QTabWidget.TabPosition.East)   # 右侧

# 设置标签可关闭
tabs.setTabsClosable(True)
tabs.tabCloseRequested.connect(self.close_tab)

# 设置当前页
tabs.setCurrentIndex(0)

# 获取当前页索引
current = tabs.currentIndex()
```

### QSplitter - 可拖动分割

允许用户拖动调整区域大小。

```python
from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import Qt

splitter = QSplitter(Qt.Orientation.Horizontal)
splitter.addWidget(left_panel)
splitter.addWidget(right_panel)

# 设置初始比例
splitter.setSizes([200, 400])

# 设置是否可折叠
splitter.setCollapsible(0, False)  # 左侧不可折叠
```

---

## 2.6 使用Qt Designer设计界面

**示例目录**：[designer_example/](designer_example/)

### Qt Designer 简介

Qt Designer是Qt提供的可视化界面设计工具，可以通过拖放方式创建UI。

### 安装Qt Designer

```bash
pip install pyqt6-tools
```

安装后，可以在以下位置找到Qt Designer：
- Windows: `Python安装目录\Lib\site-packages\qt6_applications\Qt\bin\designer.exe`
- Linux: 可以通过 `pyqt6-tools designer` 命令启动

### 设计流程

1. **打开Qt Designer**，创建新的Widget或MainWindow
2. **拖放控件**到设计区域
3. **设置布局**：选中容器 → 右键 → Layout
4. **设置属性**：在属性编辑器中修改控件属性
5. **保存为.ui文件**

### 加载.ui文件

#### 方法一：使用uic模块动态加载

```python
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 加载.ui文件
        uic.loadUi("my_design.ui", self)
        
        # 现在可以直接访问UI中的控件
        # 控件名称就是Designer中设置的objectName
        self.pushButton.clicked.connect(self.on_click)
    
    def on_click(self):
        text = self.lineEdit.text()
        self.label.setText(f"你输入了: {text}")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
```

#### 方法二：转换为Python代码

```bash
# 将.ui文件转换为.py文件
pyuic6 -x my_design.ui -o ui_my_design.py
```

生成的代码可以这样使用：

```python
from PyQt6.QtWidgets import QApplication, QWidget
from ui_my_design import Ui_Form  # 导入生成的类
import sys

class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化UI
        
        # 连接信号
        self.pushButton.clicked.connect(self.on_click)
    
    def on_click(self):
        print("按钮被点击")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
```

### 何时使用Qt Designer？

| 场景 | 建议 |
|------|------|
| 简单界面（< 10个控件） | 手写代码 |
| 复杂界面、多标签页 | Qt Designer |
| 需要频繁修改界面 | Qt Designer |
| 学习阶段 | 手写代码（加深理解） |
| 团队协作 | Qt Designer（设计与逻辑分离） |

---

## 本章小结

通过本章学习，你应该掌握了：

1. **QHBoxLayout / QVBoxLayout**：水平和垂直布局
2. **QGridLayout**：网格布局，适合表格式界面
3. **QFormLayout**：表单布局，适合参数输入
4. **嵌套布局**：组合简单布局构建复杂界面
5. **QGroupBox**：分组框，组织相关控件
6. **QTabWidget**：标签页，节省空间
7. **QSplitter**：可拖动分割区域
8. **Qt Designer**：可视化界面设计工具

### 布局选择指南

```
需要什么样的布局？
│
├── 控件需要水平/垂直排列？
│   └── QHBoxLayout / QVBoxLayout
│
├── 控件需要排列成表格？
│   └── QGridLayout
│
├── 控件是"标签-输入框"配对？
│   └── QFormLayout
│
├── 需要分组显示？
│   └── QGroupBox + 内部布局
│
├── 内容太多需要分页？
│   └── QTabWidget
│
└── 需要用户可调整区域大小？
    └── QSplitter
```

### 练习题

1. 创建一个"光谱仪参数设置"界面，包含：
   - 顶部：标题和状态指示灯
   - 中部：使用QGridLayout排列波长范围、积分时间、平均次数等参数
   - 底部：开始/停止按钮

2. 使用QTabWidget创建一个多页面设置界面：
   - 第一页：连接设置（IP地址、端口）
   - 第二页：采集参数
   - 第三页：显示选项

---

## 下一章预告

[第三章：信号与槽机制](../ch03_signals/) - 深入学习PyQt的事件驱动编程模型，掌握信号与槽的高级用法。

