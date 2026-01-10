#!/bin/bash
#SBATCH --job-name=multi-node-demo
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err

# 多节点作业说明：
# - 多节点并行通常通过 srun 启动（MPI/多进程）
# - 具体参数取决于你的程序是MPI还是多进程/多线程

set -euo pipefail

echo "=== Slurm Multi-node Job ==="
echo "Job ID: ${SLURM_JOB_ID:-unknown}"
echo "Nodes: ${SLURM_JOB_NUM_NODES:-unknown}"
echo "Node List: ${SLURM_NODELIST:-unknown}"

echo "Start Time: $(date +"%F %T")"

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then
  cd "$SLURM_SUBMIT_DIR"
fi

# 常见：加载MPI模块（根据集群实际情况）
# module purge
# module load openmpi

# 示例1：用srun启动多个进程（不一定是MPI程序，但常用于并行启动）
# srun --ntasks=$SLURM_NTASKS ./your_app --arg value

# 示例2：MPI程序（很多集群也推荐用srun而不是mpirun）
# srun ./mpi_app

echo "SLURM_NTASKS=${SLURM_NTASKS:-unknown}"

# 用hostname演示多节点多任务分布
srun --ntasks=${SLURM_NTASKS:-1} bash -lc 'echo "rank? host=$(hostname) pid=$$"'

echo "Done. End Time: $(date +"%F %T")"