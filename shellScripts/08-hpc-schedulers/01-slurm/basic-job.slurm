#!/bin/bash
#SBATCH --job-name=basic-demo
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# 说明：
# - %x: job name
# - %j: job id
# - 建议在提交目录下创建logs/，或把输出写到共享文件系统目录

set -euo pipefail

echo "=== Basic Slurm Job ==="
echo "Job ID: ${SLURM_JOB_ID:-unknown}"
echo "Job Name: ${SLURM_JOB_NAME:-unknown}"
echo "Submit Dir: ${SLURM_SUBMIT_DIR:-unknown}"
echo "Node List: ${SLURM_NODELIST:-unknown}"
echo "Start Time: $(date +"%F %T")"
echo ""

# Slurm通常在提交目录执行，但建议显式cd
if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  cd "$SLURM_SUBMIT_DIR"
fi

# 这里用 sleep 模拟计算任务
echo "Running workload..."
sleep 3

# 也可以在这里运行你的程序，例如：
# python3 train.py --epochs 10
# ./your_app --arg value

echo ""
echo "Done. End Time: $(date +"%F %T")"