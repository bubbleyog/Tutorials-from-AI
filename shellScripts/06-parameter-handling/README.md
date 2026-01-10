# 第6章：参数处理与程序对接

> 本章介绍脚本参数处理的核心套路：位置参数、getopts解析、配置文件读取、参数替换/模板渲染、以及用管道把多个程序串起来。

## 📋 本章概述

当脚本从“自己跑”变成“给别人用/给系统调度用”时，最关键的能力就是：

- **把输入讲清楚**：支持命令行参数、配置文件、环境变量
- **把输出做规范**：stdout/stderr分流，结构化输出便于下游处理
- **把程序串起来**：用管道与标准输入输出构建数据流

本章所有示例脚本都可以直接运行，并尽量使用服务器上常见的工具组合。

## 🎯 学习目标

完成本章学习后，你将能够：

- 正确使用 `$1`…`${10}`、`$@`、`$*`、`$#`，并理解引号的重要性
- 使用 `getopts` 解析短选项并实现 `usage`/错误处理
- 从 `.env`/`key=value` 等配置文件读取参数并覆盖默认值
- 熟练使用参数替换（`${var:-default}` 等）与模板渲染（`envsubst`/`sed`）
- 用管道、进程替换和Here Document对接外部程序

---

## 6.1 位置参数与 shift

📄 **示例脚本**: [01-args-basics.sh](01-args-basics.sh)

---

## 6.2 getopts：短选项解析

📄 **示例脚本**: [02-getopts.sh](02-getopts.sh)

> ⚠️ 注意：`getopts` 主要用于短选项（如 `-i file -n 3`）。长选项（`--input`）通常用 `getopt` 或自行解析。

---

## 6.3 配置文件读取（.env / ini风格）

📄 **示例脚本**: [03-config-files.sh](03-config-files.sh)

> 💡 提示：配置文件解析需要考虑注释、空行、空格、以及值中包含特殊字符的情况。本章示例给出“够用且安全”的写法。

---

## 6.4 参数替换与模板渲染

📄 **示例脚本**: [04-param-substitution.sh](04-param-substitution.sh)

---

## 6.5 程序管道对接（stdin/stdout）

📄 **示例脚本**: [05-pipeline.sh](05-pipeline.sh)

---

## 🧾 快速参考

| 目标 | 写法 |
|------|------|
| 参数个数 | `$#` |
| 全部参数（逐个） | `"$@"`（推荐） |
| 全部参数（拼成一个） | `"$*"` |
| 第10个参数 | `${10}` |
| 丢弃前N个参数 | `shift N` |
| 解析短选项 | `while getopts ":i:o:n:vh" opt; do ...; done` |
| 变量默认值 | `${var:-default}` |
| 必填参数检查 | `${var:?missing}` |
| 管道 | `producer | consumer` |
| HereDoc | `cmd << 'EOF' ... EOF` |
| 进程替换 | `diff <(cmd1) <(cmd2)` |

---

## 📦 本章文件

- [01-args-basics.sh](01-args-basics.sh) 位置参数、引号差异、shift
- [02-getopts.sh](02-getopts.sh) getopts短选项解析
- [03-config-files.sh](03-config-files.sh) 配置文件读取（.env/ini/可选JSON）
- [04-param-substitution.sh](04-param-substitution.sh) 参数替换与模板渲染
- [05-pipeline.sh](05-pipeline.sh) 管道对接、进程替换、HereDoc
