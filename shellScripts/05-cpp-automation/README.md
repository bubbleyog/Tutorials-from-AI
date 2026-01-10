# 第5章：C++程序自动化

> 本章介绍如何用Shell脚本管理C++程序的编译与运行：编译器选择、编译选项、Makefile集成、以及批量编译/执行与结果汇总。

## 📋 本章概述

在Linux服务器或HPC环境中，C++任务通常有以下特点：

- 编译耗时较长，需要合理复用构建产物（增量编译、分离build目录）
- 不同编译选项会影响性能（如 `-O0/-O2/-O3`、`-march=native`）
- 常用Makefile/CMake进行构建管理
- 运行阶段需要记录日志、检查退出码，并对多组参数做批量扫描

本章以“能直接运行”的脚本为主，给出一套实用且易迁移的自动化模板。

## 🎯 学习目标

完成本章学习后，你将能够：

- 检测并选择可用的C++编译器（g++/clang++）
- 使用脚本自动编译、运行并处理退出码
- 在脚本中调用 `make` 并向Makefile传递变量与编译参数
- 批量编译/执行多种配置，并把结果保存为CSV

---

## 5.1 编译流程速查

### 常见编译器

- `g++`（GCC）
- `clang++`（Clang）

### 常见编译选项

| 选项 | 说明 |
|------|------|
| `-std=c++17` | 选择C++标准（示例使用C++17） |
| `-O0/-O2/-O3` | 优化等级 |
| `-g` | 调试信息（便于gdb） |
| `-Wall -Wextra` | 常用告警 |
| `-march=native` | 针对当前CPU优化（可移植性较差） |

### 基本命令

```bash
# 编译
g++ -std=c++17 -O2 -Wall -Wextra -o app sample.cpp

# 运行
./app --seed 1 --name Alice

# 查看退出码
echo $?
```

📄 **示例脚本**: [01-compile-run.sh](01-compile-run.sh)

---

## 5.2 Makefile集成

在项目稍微复杂后，推荐使用Makefile统一管理编译选项、依赖与目标文件。

关键套路：

- 用变量控制编译器与参数：`CXX`、`CXXFLAGS`、`LDFLAGS`
- 用 `make clean` 清理产物
- 在脚本中通过 `make CXX=clang++ CXXFLAGS='...'` 覆盖默认配置

📄 **示例脚本**: [02-makefile-integration.sh](02-makefile-integration.sh)

---

## 5.3 批量编译与执行

典型需求：

- 对不同优化等级编译（`-O0/-O2/-O3`）
- 对不同参数/种子运行
- 归档每次运行的stdout/stderr日志
- 汇总关键指标到CSV

📄 **示例脚本**: [03-batch-cpp.sh](03-batch-cpp.sh)

---

## 🧾 快速参考

| 目标 | 常用命令 |
|------|----------|
| 检测编译器 | `command -v g++` / `command -v clang++` |
| 查看版本 | `g++ --version` |
| 编译 | `g++ -std=c++17 -O2 -o app sample.cpp` |
| 运行 | `./app --seed 1` |
| 调用make | `make -j` / `make clean` |
| 获取退出码 | `$?` |

---

## 📦 本章文件

- [01-compile-run.sh](01-compile-run.sh) 编译与运行：编译器选择、日志与退出码
- [02-makefile-integration.sh](02-makefile-integration.sh) Makefile集成：变量覆盖、clean/run
- [03-batch-cpp.sh](03-batch-cpp.sh) 批量编译执行：多配置扫描、日志归档、CSV汇总
- [sample.cpp](sample.cpp) 示例C++程序（供上述脚本调用）
