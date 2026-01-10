#!/bin/bash
#SBATCH --job-name=array-demo
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
#SBATCH --array=0-4
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

# 数组作业说明：
# - %A: array master job id
# - %a: array task id
# - SLURM_ARRAY_TASK_ID: 当前任务编号

set -euo pipefail

echo "=== Slurm Array Job ==="
echo "Master Job ID: ${SLURM_ARRAY_JOB_ID:-unknown}"
echo "Task ID: ${SLURM_ARRAY_TASK_ID:-unknown}"
echo "Start Time: $(date +"%F %T")"

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  cd "$SLURM_SUBMIT_DIR"
fi

# 把任务编号映射为参数（常见套路）
# 示例：不同seed/不同输入文件
seed=$((100 + ${SLURM_ARRAY_TASK_ID}))

echo "Using seed: $seed"

# 运行程序示例：
# python3 sample.py --seed "$seed"
# ./sample_app --seed "$seed"

sleep 2

echo "Done. End Time: $(date +"%F %T")"