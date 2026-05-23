#!/bin/bash

# ==================== Slurm Directives ====================
#SBATCH --job-name=ArrayTest
#SBATCH --partition=compute
#SBATCH --array=1-5              # 创建一个作业数组，包含 ID 从 1 到 5 的 5 个子作业
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:05:00
#SBATCH --output=array_%A_%a.out # %A 是主作业ID(Array Job ID), %a 是数组索引(Array Task ID)

# ==================== Shell Commands ====================
echo "This is array task number: $SLURM_ARRAY_TASK_ID"

# 典型用法：根据 ID 处理不同的输入文件
# 假设我们有 input_1.dat, input_2.dat, ...
INPUT_FILE="input_${SLURM_ARRAY_TASK_ID}.dat"

echo "Processing $INPUT_FILE..."

# ./my_program $INPUT_FILE
sleep 2 # 模拟处理时间
echo "Task $SLURM_ARRAY_TASK_ID finished."
