# PyQt科研应用编程教程 - 设计文档

## 教程概述

**目标受众**：理论物理与实验物理研究者  
**技术栈**：Python 3.10+, PyQt6, Matplotlib, NumPy, PySerial  
**难度级别**：初级到中级

### 核心目标

1. 帮助物理研究者快速掌握PyQt GUI编程
2. 实现科研绑图的交互式参数调节
3. 构建具有数据通信功能的仪器控制界面

---

## 章节规划

### 第一章：PyQt基础入门 (`ch01_basics/`)

**目标**：建立PyQt核心概念理解，编写第一个GUI程序

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 1.1 | 环境安装与配置 | `install_check.py` |
| 1.2 | PyQt架构与核心概念 | - |
| 1.3 | 第一个PyQt窗口 | `first_window.py` |
| 1.4 | 常用控件详解（按钮、输入框、标签等） | `basic_widgets.py` |
| 1.5 | 控件属性与方法 | `widget_properties.py` |

**知识点**：
- QApplication, QWidget, QMainWindow
- QPushButton, QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox
- 控件的创建、属性设置、显示

---

### 第二章：布局管理与界面设计 (`ch02_layout/`)

**目标**：掌握界面布局技巧，设计美观实用的科研界面

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 2.1 | 水平与垂直布局 | `hbox_vbox_demo.py` |
| 2.2 | 网格布局 | `grid_layout_demo.py` |
| 2.3 | 表单布局 | `form_layout_demo.py` |
| 2.4 | 嵌套布局与复杂界面 | `nested_layout.py` |
| 2.5 | 分组框与标签页 | `groupbox_tabs.py` |
| 2.6 | 使用Qt Designer设计界面 | `designer_example/` |

**知识点**：
- QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout
- QGroupBox, QTabWidget, QSplitter
- Qt Designer的.ui文件加载

---

### 第三章：信号与槽机制 (`ch03_signals/`)

**目标**：理解PyQt的事件驱动编程模型

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 3.1 | 信号与槽基础 | `signal_slot_basic.py` |
| 3.2 | 连接内置信号 | `builtin_signals.py` |
| 3.3 | 自定义信号 | `custom_signal.py` |
| 3.4 | 信号传递参数 | `signal_with_params.py` |
| 3.5 | Lambda表达式与信号 | `lambda_signals.py` |

**知识点**：
- connect()方法
- pyqtSignal定义与emit
- 装饰器@pyqtSlot

---

### 第四章：Matplotlib科研绑图集成 (`ch04_plotting/`)

**目标**：在PyQt中嵌入Matplotlib，实现交互式科研绘图

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 4.1 | Matplotlib嵌入PyQt基础 | `mpl_embed_basic.py` |
| 4.2 | 带工具栏的绑图窗口 | `mpl_with_toolbar.py` |
| 4.3 | 实时数据更新曲线 | `realtime_plot.py` |
| 4.4 | 交互式参数调节器 | `interactive_params.py` |
| 4.5 | 多子图与联动控制 | `multi_subplot.py` |
| 4.6 | 科研图表样式定制 | `scientific_style.py` |
| 4.7 | 图表导出与保存 | `plot_export.py` |

**知识点**：
- FigureCanvasQTAgg
- NavigationToolbar2QT
- QSlider, QDoubleSpinBox与绑图参数联动
- 定时器QTimer实现动态更新

**物理应用示例**：
- 波函数可视化（量子力学）
- 相空间轨迹（经典力学）
- 光谱曲线拟合

---

### 第五章：数据处理与分析界面 (`ch05_data_analysis/`)

**目标**：构建用于物理数据处理的GUI工具

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 5.1 | 文件对话框与数据导入 | `file_dialog.py` |
| 5.2 | 表格控件显示数据 | `table_view.py` |
| 5.3 | 曲线拟合界面 | `curve_fitting.py` |
| 5.4 | 数据滤波与处理 | `data_filter.py` |
| 5.5 | 多线程防止界面冻结 | `threading_demo.py` |
| 5.6 | 进度条与状态反馈 | `progress_bar.py` |

**知识点**：
- QFileDialog
- QTableWidget, QTableView
- QThread, QRunnable, QThreadPool
- QProgressBar

**物理应用示例**：
- 实验数据的Gauss/Lorentz拟合
- 信号FFT分析界面

---

### 第六章：仪器通信基础 (`ch06_communication/`)

**目标**：掌握串口与网络通信，为仪器控制做准备

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 6.1 | 串口通信原理与PySerial | `serial_basic.py` |
| 6.2 | 串口调试助手 | `serial_terminal.py` |
| 6.3 | TCP/IP Socket通信 | `tcp_client.py` |
| 6.4 | SCPI命令与仪器协议 | `scpi_intro.py` |
| 6.5 | 异步通信与线程安全 | `async_comm.py` |
| 6.6 | 通信日志与错误处理 | `comm_logging.py` |

**知识点**：
- pyserial库
- socket编程
- 标准命令可编程仪器(SCPI)协议
- 线程安全的数据队列

---

### 第七章：仪器控制界面实战 (`ch07_instrument/`)

**目标**：构建完整的仪器控制与数据采集系统

| 节号 | 内容 | 示例程序 |
|------|------|----------|
| 7.1 | 仪器控制面板设计模式 | `control_panel_basic.py` |
| 7.2 | 模拟仪器服务器（用于测试） | `mock_instrument.py` |
| 7.3 | 万用表数据读取界面 | `dmm_reader.py` |
| 7.4 | 信号发生器控制界面 | `signal_generator.py` |
| 7.5 | 温度控制器界面 | `temperature_controller.py` |
| 7.6 | 实时数据采集与记录 | `data_logger.py` |
| 7.7 | 多仪器协同控制 | `multi_instrument.py` |

**知识点**：
- 仪器抽象类设计
- 命令队列与响应处理
- 实时数据显示与存储
- 仪器状态监控

**物理应用示例**：
- 低温实验温度监控
- 光谱仪数据采集
- 电源与万用表联合测试

---

### 第八章：综合项目实战 (`ch08_projects/`)

**目标**：整合所有知识，完成实用的科研工具

| 项目 | 描述 | 目录 |
|------|------|------|
| 项目一 | 物理常数计算器 | `project_calculator/` |
| 项目二 | 波函数可视化工具 | `project_wavefunction/` |
| 项目三 | 完整数据采集系统 | `project_daq_system/` |

---

## 目录结构

```
PyQt/
├── DESIGN.md                    # 本设计文档
├── README.md                    # 教程总览与使用说明
├── requirements.txt             # 依赖包列表
│
├── ch01_basics/                 # 第一章
│   ├── README.md
│   ├── install_check.py
│   ├── first_window.py
│   ├── basic_widgets.py
│   └── widget_properties.py
│
├── ch02_layout/                 # 第二章
│   ├── README.md
│   ├── hbox_vbox_demo.py
│   ├── grid_layout_demo.py
│   ├── form_layout_demo.py
│   ├── nested_layout.py
│   ├── groupbox_tabs.py
│   └── designer_example/
│
├── ch03_signals/                # 第三章
│   ├── README.md
│   ├── signal_slot_basic.py
│   ├── builtin_signals.py
│   ├── custom_signal.py
│   ├── signal_with_params.py
│   └── lambda_signals.py
│
├── ch04_plotting/               # 第四章
│   ├── README.md
│   ├── mpl_embed_basic.py
│   ├── mpl_with_toolbar.py
│   ├── realtime_plot.py
│   ├── interactive_params.py
│   ├── multi_subplot.py
│   ├── scientific_style.py
│   └── plot_export.py
│
├── ch05_data_analysis/          # 第五章
│   ├── README.md
│   ├── file_dialog.py
│   ├── table_view.py
│   ├── curve_fitting.py
│   ├── data_filter.py
│   ├── threading_demo.py
│   └── progress_bar.py
│
├── ch06_communication/          # 第六章
│   ├── README.md
│   ├── serial_basic.py
│   ├── serial_terminal.py
│   ├── tcp_client.py
│   ├── scpi_intro.py
│   ├── async_comm.py
│   └── comm_logging.py
│
├── ch07_instrument/             # 第七章
│   ├── README.md
│   ├── control_panel_basic.py
│   ├── mock_instrument.py
│   ├── dmm_reader.py
│   ├── signal_generator.py
│   ├── temperature_controller.py
│   ├── data_logger.py
│   └── multi_instrument.py
│
└── ch08_projects/               # 第八章
    ├── README.md
    ├── project_calculator/
    ├── project_wavefunction/
    └── project_daq_system/
```

---

## 技术要求

### 依赖包

```
PyQt6>=6.5.0
matplotlib>=3.7.0
numpy>=1.24.0
scipy>=1.10.0
pyserial>=3.5
```

### 开发环境

- Python 3.10 或更高版本
- 推荐使用虚拟环境(venv/conda)
- IDE推荐：VS Code + Python扩展 或 PyCharm

---

## 教程编写规范

### Markdown文档规范

1. 每章有独立的`README.md`作为章节教程
2. 使用中文编写，技术术语保留英文
3. 包含代码块和运行效果说明
4. 关键概念用**加粗**标注

### 代码规范

1. 遵循PEP8代码风格
2. 使用类型注解(Type Hints)
3. 添加必要的中文注释
4. 每个示例程序可独立运行
5. 文件开头包含简要说明

### 示例代码模板

```python
"""
示例程序：XXX功能演示
所属章节：第X章 - XXX

功能说明：
    演示PyQt中XXX的使用方法

运行方式：
    python xxx_demo.py
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget

class DemoWindow(QWidget):
    """示例窗口类"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("示例程序")
        self.setGeometry(100, 100, 400, 300)

def main():
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

---

## 预计工作量

| 章节 | 预计文档字数 | 示例程序数 |
|------|-------------|-----------|
| 第一章 | 3000字 | 4 |
| 第二章 | 4000字 | 6 |
| 第三章 | 3000字 | 5 |
| 第四章 | 5000字 | 7 |
| 第五章 | 4000字 | 6 |
| 第六章 | 4000字 | 6 |
| 第七章 | 5000字 | 7 |
| 第八章 | 3000字 | 3个项目 |

**总计**：约31000字文档 + 44个示例程序 + 3个综合项目

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.1 | 2024-12-13 | 初始设计文档 |

---

## 后续扩展方向

1. PyQtGraph高性能绑图（适用于大数据量实时显示）
2. 3D可视化（VTK/PyVista集成）
3. 仪器VISA通信（pyvisa库）
4. 数据库集成（SQLite/PostgreSQL）
5. 网络化仪器控制（Web界面）

