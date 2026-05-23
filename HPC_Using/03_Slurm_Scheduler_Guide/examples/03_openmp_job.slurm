#!/bin/bash

# ==================== Slurm Directives ====================
#SBATCH --job-name=OpenMP_Job
#SBATCH --partition=compute
#SBATCH --nodes=1                # 只申请 1 个节点
#SBATCH --ntasks=1               # 只运行 1 个主进程
#SBATCH --cpus-per-task=20       # 这个进程需要 20 个 CPU 核心 (多线程)
#SBATCH --time=00:30:00
#SBATCH --output=omp_%j.log

# ==================== Shell Commands ====================
echo "Job ID: $SLURM_JOB_ID"

module load gcc/9.3.0

# 设置 OMP_NUM_THREADS
# Slurm 提供了 $SLURM_CPUS_PER_TASK 变量
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS"

# 对于 OpenMP 程序，直接运行即可，或者是用 srun 运行
# srun ./my_openmp_program
./my_openmp_program
