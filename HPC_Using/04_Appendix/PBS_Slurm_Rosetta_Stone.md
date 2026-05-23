# PBS vs Slurm 命令对照表 (Rosetta Stone)

这是一份快速查阅指南，帮助熟悉 PBS 的用户快速上手 Slurm，反之亦然。

## 1. 命令行指令对照

| 动作 | PBS (Torque/Moab) | Slurm |
| :--- | :--- | :--- |
| **提交作业** | `qsub script.pbs` | `sbatch script.slurm` |
| **交互式作业** | `qsub -I ...` | `srun --pty ...` / `salloc ...` |
| **查看所有作业** | `qstat` | `squeue` |
| **查看特定用户作业** | `qstat -u user` | `squeue -u user` |
| **取消作业** | `qdel <jobid>` | `scancel <jobid>` |
| **取消用户所有作业** | `qdel all` (部分版本支持) | `scancel -u user` |
| **查看节点状态** | `pbsnodes -a` | `sinfo` / `scontrol show node` |
| **查看作业详细信息** | `qstat -f <jobid>` | `scontrol show job <jobid>` |
| **挂起作业 (Hold)** | `qhold <jobid>` | `scontrol hold <jobid>` |
| **释放作业 (Release)** | `qrls <jobid>` | `scontrol release <jobid>` |

## 2. 脚本指令头 (Directives) 对照

| 资源申请 | PBS (`#PBS`) | Slurm (`#SBATCH`) | 注意事项 |
| :--- | :--- | :--- | :--- |
| **脚本解释器** | `#!/bin/bash` | `#!/bin/bash` | 通用 |
| **作业名称** | `-N JobName` | `-J JobName` / `--job-name=JobName` | |
| **指定队列/分区** | `-q queue_name` | `-p partition_name` | |
| **运行时间限制** | `-l walltime=24:00:00` | `-t 24:00:00` | |
| **节点数** | `-l nodes=2` | `-N 2` / `--nodes=2` | |
| **每节点核心数** | `:ppn=20` | (无直接对应，组合使用) | Slurm 改用 ntasks 逻辑 |
| **总进程数 (MPI Rank)** | (通常结合 nodes:ppn) | `-n 40` / `--ntasks=40` | |
| **每进程 CPU 数 (OpenMP)**| (无指令, 设环境变量) | `-c 4` / `--cpus-per-task=4` | Slurm 显式支持 |
| **标准输出文件** | `-o stdout.log` | `-o stdout.log` | Slurm 支持 `%j` 宏 |
| **错误输出文件** | `-e stderr.log` | `-e stderr.log` | |
| **合并输出** | `-j oe` | (不指定 `-e` 默认合并到 `-o`) | |
| **作业数组** | `-t 1-100` | `-a 1-100` / `--array=1-100` | |
| **作业依赖** | `-W depend=afterok:123`| `-d afterok:123` | |
| **环境变量传递** | `-V` (默认不传部分环境) | `--export=ALL` (默认传) | |

## 3. 环境变量对照

在作业脚本内部自动生成的变量。

| 变量含义 | PBS 变量 | Slurm 变量 |
| :--- | :--- | :--- |
| **作业 ID** | `$PBS_JOBID` | `$SLURM_JOB_ID` |
| **作业提交目录** | `$PBS_O_WORKDIR` | `$SLURM_SUBMIT_DIR` |
| **分配的节点列表文件** | `$PBS_NODEFILE` | (自动处理, 部分支持 `$SLURM_JOB_NODELIST`) |
| **分配的节点名称** | (读 NODEFILE) | `$SLURM_JOB_NODELIST` |
| **作业数组索引** | `$PBS_ARRAYID` | `$SLURM_ARRAY_TASK_ID` |
