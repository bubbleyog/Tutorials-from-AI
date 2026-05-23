#!/bin/bash

# ==================== Slurm Directives ====================
#SBATCH --job-name=BasicJob      # 作业名称
#SBATCH --partition=debug        # 分区名称 (debug, compute, batch 等)
#SBATCH --nodes=1                # 申请 1 个节点
#SBATCH --ntasks=1               # 运行 1 个任务 (进程)
#SBATCH --cpus-per-task=1        # 每个任务 1 个 CPU 核
#SBATCH --time=00:10:00          # 限制运行 10 分钟
#SBATCH --output=job_%j.out      # 标准输出 (%j 会被替换为作业ID)
#SBATCH --error=job_%j.err       # 错误输出

# ==================== Shell Commands ====================

# 注意: Slurm 默认就在你提交作业的目录下启动，
# 所以不需要像 PBS 那样 "cd $PBS_O_WORKDIR"。
echo "Job ID: $SLURM_JOB_ID"
echo "Working Directory: $(pwd)"
echo "Running on node: $(hostname)"

# 加载软件环境
module load python/3.8

# 运行程序
echo "Start running..."
python -c "import socket; print(f'Hello from {socket.gethostname()}')"
echo "Done."
