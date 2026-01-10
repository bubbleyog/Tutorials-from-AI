#!/bin/bash
#SBATCH --job-name=gpu-demo
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# GPU作业说明：
# - --partition 通常需要选择GPU分区（示例为 gpu）
# - --gres=gpu:1 申请1张GPU（不同集群可能写法不同，如 gpu:a100:1）

set -euo pipefail

echo "=== Slurm GPU Job ==="
echo "Job ID: ${SLURM_JOB_ID:-unknown}"
echo "Node List: ${SLURM_NODELIST:-unknown}"
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-<not set>}"

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  cd "$SLURM_SUBMIT_DIR"
fi

# 常见做法：加载模块（根据集群实际情况）
# module purge
# module load cuda/12.1
# module load anaconda

# 运行GPU程序示例：
# python3 train.py --device cuda
# ./cuda_app --batch 256

sleep 2

echo "Done. End Time: $(date +"%F %T")"