#!/bin/bash

# Slurm 作业脚本模板
# 提交作业命令: sbatch job_script.slurm

# --- 资源申请部分 ---
#SBATCH --job-name=my_hpc_job        # 作业名称
#SBATCH --output=result_%j.out       # 标准输出文件 (%j 代表作业 ID)
#SBATCH --error=result_%j.err        # 标准错误文件
#SBATCH --nodes=2                    # 申请节点数 (例如 2 台机器)
#SBATCH --ntasks-per-node=4          # 每个节点的 MPI 进程数 (例如每台机器启动 4 个进程)
#SBATCH --cpus-per-task=1            # 每个进程使用的 CPU 核数 (如果混合 OpenMP，这里设为线程数)
#SBATCH --time=00:10:00              # 预计运行时间 (10分钟)，超时会被杀掉
#SBATCH --partition=debug            # 提交到的队列/分区名称 (需根据集群实际情况修改)

# --- 环境配置部分 ---
echo "Starting job on $(hostname)"
echo "Nodes allocated: $SLURM_JOB_NODELIST"

# 加载必要的模块 (Module)
# 这一步非常重要，因为计算节点的环境通常是空的
# module purge                 # 清除所有已加载模块
# module load gcc/9.3.0        # 加载编译器
# module load openmpi/4.0.3    # 加载 MPI 库
# module load cmake/3.18       # 加载 CMake (如果需要编译)

# --- 运行部分 ---

# 1. 编译 (通常建议在登录节点编译好，这里仅演示)
# mkdir -p build && cd build
# cmake .. && make

# 2. 运行 MPI 程序
# srun 是 Slurm 提供的运行命令，会自动读取 #SBATCH 的配置启动 MPI 进程
# 注意：在 Slurm 中通常推荐使用 srun 而不是 mpirun
srun ./build/app

echo "Job finished at $(date)"
