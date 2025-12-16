# PyQt科研应用编程教程

> 面向理论物理与实验物理研究者的PyQt6 GUI编程实战教程

## 📖 教程简介

本教程专为物理研究者设计，从PyQt基础到仪器控制界面开发，帮助您快速构建实用的科研工具软件。

### 适用人群

- 理论物理研究者：需要可视化模拟结果、交互式参数调节
- 实验物理研究者：需要仪器控制界面、数据采集系统
- 具有Python基础的科研工作者

### 你将学到

✅ PyQt6 GUI编程核心概念  
✅ 在界面中嵌入Matplotlib科研绘图  
✅ 交互式修改绑图参数  
✅ 串口/网络仪器通信  
✅ 构建完整的数据采集系统  

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 推荐使用虚拟环境

### 安装依赖

```bash
# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 验证安装

```bash
python ch01_basics/install_check.py
```

---

## 📚 章节目录

| 章节 | 主题 | 描述 |
|------|------|------|
| [第一章](ch01_basics/) | **PyQt基础入门** | 窗口创建、常用控件、基本概念 |
| [第二章](ch02_layout/) | **布局管理与界面设计** | 布局器、分组、Qt Designer |
| [第三章](ch03_signals/) | **信号与槽机制** | 事件驱动、自定义信号、参数传递 |
| [第四章](ch04_plotting/) | **Matplotlib科研绘图** | 图表嵌入、交互参数、实时更新 |
| [第五章](ch05_data_analysis/) | **数据处理与分析界面** | 文件操作、曲线拟合、多线程 |
| [第六章](ch06_communication/) | **仪器通信基础** | 串口、TCP/IP、SCPI协议 |
| [第七章](ch07_instrument/) | **仪器控制界面实战** | 完整的仪器控制面板开发 |
| [第八章](ch08_projects/) | **综合项目实战** | 三个完整科研工具项目 |

---

## 🔬 物理应用示例

本教程包含多个贴近物理研究的实例：

### 理论物理

- 量子力学波函数可视化
- 相空间轨迹绑制
- 物理常数计算器

### 实验物理

- 光谱曲线拟合工具
- 温度控制器界面
- 多仪器协同数据采集

---

## 📁 项目结构

```
PyQt/
├── README.md           # 本文件
├── DESIGN.md           # 设计文档
├── requirements.txt    # 依赖包
├── ch01_basics/        # 第一章：基础入门
├── ch02_layout/        # 第二章：布局设计
├── ch03_signals/       # 第三章：信号与槽
├── ch04_plotting/      # 第四章：科研绘图
├── ch05_data_analysis/ # 第五章：数据分析
├── ch06_communication/ # 第六章：仪器通信
├── ch07_instrument/    # 第七章：仪器控制
└── ch08_projects/      # 第八章：综合项目
```

---

## 🛠️ 开发建议

### 推荐IDE

- **VS Code** + Python扩展
- **PyCharm** Community/Professional

### 调试技巧

1. 使用`print()`或`logging`输出调试信息
2. PyQt的错误信息可能较为晦涩，注意检查信号槽连接
3. 界面冻结通常是主线程阻塞，考虑使用多线程

---

## 📖 参考资源

- [PyQt6官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt官方文档](https://doc.qt.io/)
- [Matplotlib官方文档](https://matplotlib.org/stable/)
- [PySerial文档](https://pyserial.readthedocs.io/)

---

## 📄 许可证

本教程代码采用 MIT 许可证，可自由用于学习和科研目的。

---

**开始学习** → [第一章：PyQt基础入门](ch01_basics/)

