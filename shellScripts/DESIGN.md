# Shell脚本编程简明教程 - 设计文档

> 面向Linux服务器任务运行管理的实用教程

## 📋 教程概述

本教程旨在提供一份**简明实用**的Shell脚本编程指南，专注于Linux服务器环境下的任务运行管理。教程将涵盖从基础语法到高性能计算集群调度的完整知识链条，帮助读者快速掌握自动化运维和科学计算任务管理的核心技能。

### 目标读者

- Linux服务器管理员
- 需要在服务器上运行Python/C++程序的研究人员
- 高性能计算集群用户
- DevOps工程师

### 教程特色

- **实战导向**：每个章节配有可运行的示例脚本
- **循序渐进**：从基础到高级，逻辑清晰
- **聚焦服务器**：专注于服务器任务管理场景

---

## 📁 目录结构

```
shellScripts/
├── DESIGN.md                    # 本设计文档
├── README.md                    # 教程入口与导航
│
├── 01-basics/                   # 第1章：Shell基础
│   ├── README.md                # 章节说明
│   ├── 01-hello.sh              # Hello World示例
│   ├── 02-variables.sh          # 变量使用
│   ├── 03-conditions.sh         # 条件判断
│   └── 04-loops.sh              # 循环结构
│
├── 02-file-operations/          # 第2章：文件与目录操作
│   ├── README.md
│   ├── 01-file-test.sh          # 文件测试
│   ├── 02-file-process.sh       # 文件处理
│   └── 03-directory-ops.sh      # 目录操作
│
├── 03-process-management/       # 第3章：进程与后台任务
│   ├── README.md
│   ├── 01-background.sh         # 后台运行
│   ├── 02-nohup-screen.sh       # nohup与screen
│   └── 03-process-control.sh    # 进程控制
│
├── 04-python-automation/        # 第4章：Python程序自动化
│   ├── README.md
│   ├── 01-run-python.sh         # 运行Python脚本
│   ├── 02-venv-manage.sh        # 虚拟环境管理
│   ├── 03-batch-python.sh       # 批量执行
│   └── sample.py                # 示例Python程序
│
├── 05-cpp-automation/           # 第5章：C++程序自动化
│   ├── README.md
│   ├── 01-compile-run.sh        # 编译与运行
│   ├── 02-makefile-integration.sh # Makefile集成
│   ├── 03-batch-cpp.sh          # 批量编译执行
│   └── sample.cpp               # 示例C++程序
│
├── 06-parameter-handling/       # 第6章：参数处理与程序对接
│   ├── README.md
│   ├── 01-args-basics.sh        # 参数基础
│   ├── 02-getopts.sh            # getopts解析
│   ├── 03-config-files.sh       # 配置文件读取
│   ├── 04-param-substitution.sh # 参数替换与模板
│   └── 05-pipeline.sh           # 程序管道对接
│
├── 07-task-scheduling/          # 第7章：本地任务调度
│   ├── README.md
│   ├── 01-cron-basics.sh        # cron基础
│   ├── 02-at-command.sh         # at一次性任务
│   └── 03-systemd-timer.sh      # systemd定时器
│
└── 08-hpc-schedulers/           # 第8章：高性能计算调度系统
    ├── README.md                # 章节主文档（重点章节）
    ├── 01-slurm/                # Slurm调度系统
    │   ├── README.md
    │   ├── basic-job.slurm      # 基础作业脚本
    │   ├── array-job.slurm      # 数组作业
    │   ├── gpu-job.slurm        # GPU作业
    │   └── multi-node.slurm     # 多节点作业
    ├── 02-pbs/                  # PBS/Torque调度系统
    │   ├── README.md
    │   └── basic-job.pbs
    ├── 03-sge/                  # SGE调度系统
    │   ├── README.md
    │   └── basic-job.sge
    └── 04-best-practices.md     # 最佳实践与技巧
```

---

## 📚 章节内容设计

### 第1章：Shell基础 (`01-basics/`)

**目标**：建立Shell脚本编程的基础知识

| 内容 | 说明 |
|------|------|
| Shebang与执行权限 | `#!/bin/bash`、`chmod +x` |
| 变量与环境变量 | 定义、引用、导出、特殊变量 |
| 字符串操作 | 拼接、截取、替换 |
| 条件判断 | `if-elif-else`、`test`、`[[ ]]` |
| 循环结构 | `for`、`while`、`until` |
| 函数定义 | 函数、局部变量、返回值 |

---

### 第2章：文件与目录操作 (`02-file-operations/`)

**目标**：掌握文件系统操作的脚本化

| 内容 | 说明 |
|------|------|
| 文件测试 | `-f`、`-d`、`-e`、`-r`、`-w`、`-x` |
| 文件读写 | `read`、重定向、`cat`、`tee` |
| 文本处理 | `grep`、`sed`、`awk`基础 |
| 目录遍历 | `find`、通配符、递归处理 |

---

### 第3章：进程与后台任务 (`03-process-management/`)

**目标**：理解Linux进程管理，掌握长时间任务运行技巧

| 内容 | 说明 |
|------|------|
| 前台与后台 | `&`、`jobs`、`fg`、`bg` |
| 进程状态 | `ps`、`top`、`htop` |
| 保持运行 | `nohup`、`disown` |
| 终端复用 | `screen`、`tmux` |
| 信号处理 | `trap`、`kill`、常用信号 |

---

### 第4章：Python程序自动化 (`04-python-automation/`)

**目标**：使用Shell脚本管理和自动化Python程序运行

| 内容 | 说明 |
|------|------|
| 基础运行 | 解释器选择、脚本执行 |
| 虚拟环境 | venv/conda激活与管理 |
| 参数传递 | 命令行参数、环境变量 |
| 批量执行 | 参数扫描、结果收集 |
| 错误处理 | 返回值检查、日志记录 |

---

### 第5章：C++程序自动化 (`05-cpp-automation/`)

**目标**：使用Shell脚本管理C++程序的编译和运行

| 内容 | 说明 |
|------|------|
| 编译流程 | g++/clang++、编译选项 |
| Makefile集成 | make调用、条件编译 |
| CMake集成 | cmake构建自动化 |
| 运行与调试 | 参数传递、gdb集成 |
| 批量任务 | 多配置编译、性能测试 |

---

### 第6章：参数处理与程序对接 (`06-parameter-handling/`)

**目标**：掌握脚本参数处理和与其他程序的对接技术

| 内容 | 说明 |
|------|------|
| 位置参数 | `$1`-`$9`、`$@`、`$#`、`shift` |
| getopts | 短选项解析 |
| 长选项 | getopt外部命令 |
| 配置文件 | INI/YAML/JSON读取 |
| 模板替换 | `envsubst`、`sed`替换 |
| 管道对接 | 标准输入输出、进程替换 |
| Here Document | 多行输入、程序交互 |

---

### 第7章：本地任务调度 (`07-task-scheduling/`)

**目标**：掌握Linux系统的定时任务管理

| 内容 | 说明 |
|------|------|
| cron | crontab语法、用户级/系统级 |
| at | 一次性定时任务 |
| systemd timer | 现代定时任务管理 |
| 任务监控 | 日志、邮件通知 |

---

### 第8章：高性能计算调度系统 (`08-hpc-schedulers/`) ⭐重点

**目标**：全面了解HPC集群作业调度，能够编写和提交各类作业

#### 8.1 调度系统概述
- 什么是作业调度系统
- 主流调度系统对比（Slurm、PBS、SGE、LSF）
- 资源管理基本概念（节点、分区、队列、QoS）

#### 8.2 Slurm（重点讲解）
| 内容 | 说明 |
|------|------|
| 基础命令 | `sbatch`、`squeue`、`scancel`、`sinfo` |
| 作业脚本 | `#SBATCH`指令详解 |
| 资源请求 | CPU、内存、时间、GPU |
| 数组作业 | 参数扫描、批量任务 |
| 多节点并行 | MPI作业、分布式计算 |
| 依赖关系 | 作业链、工作流 |
| 交互作业 | `srun`、`salloc` |

#### 8.3 PBS/Torque
- 基础用法与Slurm对比
- 常用PBS指令

#### 8.4 SGE (Sun Grid Engine)
- 基础用法
- qsub命令

#### 8.5 最佳实践
- 资源估算技巧
- 作业脚本模板
- 调试与故障排查
- 效率优化建议

---

## 🎯 设计原则

### 1. 渐进式学习
```
基础语法 → 文件操作 → 进程管理 → 语言集成 → 参数处理 → 调度系统
```

### 2. 示例驱动
- 每个概念配有**可运行**的示例脚本
- 示例包含详细注释
- 提供练习建议

### 3. 实用优先
- 聚焦服务器运维场景
- 避免过度深入语法细节
- 提供"速查"式的命令表

### 4. 模块独立
- 每章可独立阅读
- 交叉引用其他章节时标注

---

## 🛠️ 开发计划

| 阶段 | 内容 | 预计文件数 |
|------|------|-----------|
| Phase 1 | 第1-3章：基础与进程管理 | ~12个 |
| Phase 2 | 第4-5章：Python/C++自动化 | ~10个 |
| Phase 3 | 第6-7章：参数与调度 | ~8个 |
| Phase 4 | 第8章：HPC调度系统 | ~10个 |
| Phase 5 | README与完善 | ~3个 |

**总计**：约43个文件（含markdown文档和示例脚本）

---

## 📝 编写规范

### Markdown文档
- 使用清晰的标题层级
- 代码块标注语言类型
- 重要信息使用提示框（`> ⚠️ 注意`）
- 提供"快速参考"表格

### Shell脚本
```bash
#!/bin/bash
#
# 脚本名称: example.sh
# 描述: 脚本功能简述
# 用法: ./example.sh [参数]
#

# 启用严格模式
set -euo pipefail

# 脚本内容...
```

### 命名规范
- 目录：`数字-英文名称`（如`01-basics`）
- 脚本：`数字-功能名.sh`（如`01-hello.sh`）
- 说明：统一使用`README.md`

---

## ✅ 确认事项

请确认以下设计是否符合您的需求：

1. **章节设置**：8个章节的安排是否合理？
2. **深度广度**：各章节的内容深度是否适当？
3. **重点章节**：第8章HPC调度作为重点是否正确？
4. **示例程序**：是否需要更多/更复杂的Python/C++示例？
5. **其他需求**：是否有其他需要包含的主题？

---

*设计文档版本: v1.0*  
*创建日期: 2025-12-25*

