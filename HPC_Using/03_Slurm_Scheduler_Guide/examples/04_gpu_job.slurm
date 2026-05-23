#!/bin/bash

# ==================== Slurm Directives ====================
#SBATCH --job-name=GPU_Job
#SBATCH --partition=gpu          # 提交到 GPU 分区
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4        # 哪怕是 GPU 任务，也需要一些 CPU 核心来做数据加载
#SBATCH --gres=gpu:1             # 申请 1 个通用资源(GRES): GPU
#SBATCH --time=02:00:00
#SBATCH --output=gpu_%j.log

# ==================== Shell Commands ====================
echo "Job ID: $SLURM_JOB_ID"

module load cuda/11.0 conda

# 检查 GPU 是否分配成功
echo "Checking GPU status:"
nvidia-smi

# 运行 Python 训练脚本
python train_deep_learning_model.py
