#!/bin/bash

# Module 系统演示脚本
# 注意：此脚本需要在支持 Environment Modules 的 HPC 环境中运行
# 如果在普通 Linux 机器上运行可能会报错 "module: command not found"

# 为了在 Shell 脚本中使用 module 命令，通常需要先初始化 shell 环境
# source /etc/profile.d/modules.sh  # 具体路径因系统而异

echo "=== 1. Checking loaded modules ==="
module list

echo -e "\n=== 2. Checking available Python modules ==="
module avail python 2>&1 | head -n 10
# 注意：module 命令通常输出到 stderr，所以用 2>&1 重定向以便查看

echo -e "\n=== 3. Loading Anaconda3 ==="
# 尝试加载一个常见的模块名，不同集群名字可能不同
# 常见名字: python/3.8, anaconda3, miniconda
# 这里仅演示命令格式
echo "Executing: module load anaconda3"
# module load anaconda3

echo -e "\n=== 4. Checking Python version ==="
python --version

echo -e "\n=== 5. Swapping environment ==="
# 切换编译器版本，例如从 GCC 4.8 切换到 GCC 9.3
echo "Executing: module swap gcc/4.8.5 gcc/9.3.0"
# module swap gcc/4.8.5 gcc/9.3.0

echo -e "\n=== 6. Purging setup ==="
echo "Executing: module purge"
# module purge
# module list
