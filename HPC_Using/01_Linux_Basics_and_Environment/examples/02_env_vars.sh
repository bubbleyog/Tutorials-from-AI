#!/bin/bash

# 环境变量演示脚本

echo "----------------------------------------"
echo "1. 查看常用环境变量"
echo "----------------------------------------"

# $HOME: 用户的主目录
echo "My Home Directory: $HOME"

# $USER: 当前用户名
echo "Current User: $USER"

# $PATH: 系统查找命令的路径列表 (用冒号分隔)
echo "Current PATH:"
echo $PATH | tr ':' '\n' | head -n 3 # 只显示前3行以免太长
echo "..."

echo "----------------------------------------"
echo "2. 临时修改环境变量"
echo "----------------------------------------"

# 假设我们安装了一个软件在 ~/my_apps/bin
export PATH=$HOME/my_apps/bin:$PATH

echo "New PATH (prefix added):"
echo $PATH | tr ':' '\n' | head -n 1

echo "----------------------------------------"
echo "3. 自定义应用变量"
echo "----------------------------------------"
# 许多科学计算软件通过环境变量控制行为
export OMP_NUM_THREADS=4
echo "Set OMP_NUM_THREADS to $OMP_NUM_THREADS (Controls OpenMP parallelism)"
