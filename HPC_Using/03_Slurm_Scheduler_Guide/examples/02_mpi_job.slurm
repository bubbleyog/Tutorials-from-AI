#!/bin/bash

# ==================== Slurm Directives ====================
#SBATCH --job-name=MPI_Job
#SBATCH --partition=compute
#SBATCH --nodes=2                # 申请 2 个节点
#SBATCH --ntasks=40              # 总共 40 个 MPI 进程 (假设每节点 20 核)
#SBATCH --cpus-per-task=1        # 每个 MPI 进程独占 1 个 CPU
#SBATCH --time=01:00:00
#SBATCH --output=mpi_%j.log

# ==================== Shell Commands ====================
echo "Job ID: $SLURM_JOB_ID"
echo "Nodes allocated: $SLURM_JOB_NODELIST"

module load openmpi/4.0.3

# 关键区别:
# 在 PBS 中我们需要 cat $PBS_NODEFILE 来看节点。
# 在 Slurm 中，srun 会自动读取环境变量配置。

echo "Running MPI program with srun..."
# srun 是 Slurm 原生的并行启动器，它知道 --ntasks=40，会自动分发
srun ./my_mpi_program

# 如果你的程序或者习惯强制要求用 mpirun，也可以:
# mpirun ./my_mpi_program
