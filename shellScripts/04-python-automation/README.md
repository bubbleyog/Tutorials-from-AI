# 第4章：Python程序自动化

> 本章介绍如何用Shell脚本管理和自动化Python程序运行：解释器选择、虚拟环境、参数传递、批量执行与结果收集、以及错误处理与日志。

## 📋 本章概述

在Linux服务器上运行Python任务时，常见需求包括：

- 选择合适的Python解释器（系统Python、模块环境、虚拟环境）
- 传递命令行参数与环境变量
- 记录日志（stdout/stderr分流、追加、带时间戳）
- 批量运行一组参数并汇总结果
- 可靠地处理失败（退出码、重试、清理临时文件）

本章通过可直接运行的示例脚本，演示一套“够用且健壮”的实践套路。

## 🎯 学习目标

完成本章学习后，你将能够：

- 使用Shell脚本稳定地运行Python程序并获取退出码
- 用环境变量与命令行参数控制Python程序行为
- 创建与使用 `venv` 虚拟环境（无需手动激活也可运行）
- 批量执行多组参数并把结果保存为结构化文件（CSV）

---

## 4.1 基础运行：解释器与脚本执行

### 解释器选择

常见做法：

- 优先使用 `python3`（服务器环境更常见）
- 用 `command -v python3` 检测是否存在
- 在脚本中允许通过环境变量覆盖解释器（如 `PYTHON_BIN=/path/to/python`）

### 获取退出码

Shell中可用 `$?` 获取上一条命令的退出状态：

```bash
python3 script.py
rc=$?
echo "exit code: $rc"
```

> 💡 约定俗成：退出码 `0` 表示成功，非 `0` 表示失败。

📄 **示例脚本**: [01-run-python.sh](01-run-python.sh)

---

## 4.2 虚拟环境：venv/conda 的基本套路

### venv（Python自带）

```bash
python3 -m venv .venv
source .venv/bin/activate
python -V
```

在脚本里更推荐“**不依赖交互式activate**”的方式：

```bash
.venv/bin/python your_script.py
```

这样更适合cron、systemd、以及HPC作业脚本。

📄 **示例脚本**: [02-venv-manage.sh](02-venv-manage.sh)

> ⚠️ 注意：如果你的系统Python缺少 `venv` 模块（常见于最小化安装），需要安装发行版对应包，例如Debian/Ubuntu上的 `python3-venv`。

---

## 4.3 参数传递：命令行参数与环境变量

两种方式各有用武之地：

- 命令行参数：适合任务参数（如 `--epochs 10 --lr 1e-3`）
- 环境变量：适合环境配置（如 `DATA_DIR=/data`、`CUDA_VISIBLE_DEVICES=0`）

📄 **示例程序**: [sample.py](sample.py)

---

## 4.4 批量执行：参数扫描与结果收集

典型场景：

- 对不同 `seed`、不同输入文件、不同超参数组合做扫描
- 每次运行保存日志
- 汇总每次运行的关键指标到一个CSV，便于后续分析

📄 **示例脚本**: [03-batch-python.sh](03-batch-python.sh)

---

## 🧾 快速参考

| 目标 | 常用命令 |
|------|----------|
| 检查Python是否存在 | `command -v python3` |
| 运行脚本 | `python3 script.py args...` |
| 创建venv | `python3 -m venv .venv` |
| 不激活运行venv | `.venv/bin/python script.py` |
| 记录日志 | `cmd > out.log 2> err.log` / `cmd >> run.log 2>&1` |
| 获取退出码 | `$?` |

---

## 📦 本章文件

- [01-run-python.sh](01-run-python.sh) 运行Python：解释器、参数、退出码、日志
- [02-venv-manage.sh](02-venv-manage.sh) venv管理：创建、复用、清理、无激活运行
- [03-batch-python.sh](03-batch-python.sh) 批量执行：参数扫描、日志归档、CSV汇总
- [sample.py](sample.py) 示例Python程序（供上述脚本调用）
