# 第三部分：Slurm 调度系统实战

**Slurm (Simple Linux Utility for Resource Management)** 是目前世界上超级计算机（包括 Top500 中大部分机器）使用最主要的主流调度系统。相比 PBS，它更加现代、灵活，且功能强大。

## 3.1 Slurm 架构简介

Slurm 使用 **Partition (分区)** 的概念，类似于 PBS 中的 Queue (队列)。你需要根据任务类型（调试、长期运行、GPU）选择不同的分区。

## 3.2 基本作业提交 (`sbatch`)

在 Slurm 中，使用 `sbatch` 提交批处理作业脚本。脚本通常以 `.slurm` 或 `.sh` 结尾。

### Slurm 脚本结构
类似于 PBS，Slurm 脚本也由 Header 和 Body 组成。指令头以 `#SBATCH` 开头。

### 核心参数详解
| 参数 | 含义 | 示例 |
| :--- | :--- | :--- |
| `--job-name=name` | 作业名称 | `#SBATCH -J MyJob` (简写 -J) |
| `--partition=name` | 指定分区 | `#SBATCH -p compute` (简写 -p) |
| `--nodes=N` | 节点数 | `#SBATCH -N 2` (申请2个节点) |
| `--ntasks=N` | 总任务数(进程数) | `#SBATCH -n 40` (总共运行40个进程，常用于MPI) |
| `--cpus-per-task=N` | 每任务CPU数 | `#SBATCH -c 4` (每进程用4核，常用于OpenMP) |
| `--time=HH:MM:SS` | 时间限制 | `#SBATCH -t 01:30:00` |
| `--mem=size` | 内存限制 | `#SBATCH --mem=4G` (每节点4G) |
| `--output=file` | 标准输出文件 | `#SBATCH -o out_%j.log` (%j 代表作业ID) |
| `--error=file` | 错误输出文件 | `#SBATCH -e err_%j.log` |

### 提交命令
```bash
sbatch examples/01_basic_job.slurm
```
系统会返回：`Submitted batch job 12345`。

## 3.3 作业管理与监控

### 查看队列 (`squeue`)
*   `squeue`: 查看系统中所有作业。
*   `squeue -u username`: 只看我自己的。
*   `squeue -j jobid`: 查看特定作业。

**状态代码含义**:
*   **PD (Pending)**: 排队中。
*   **R (Running)**: 运行中。
*   **CG (Completing)**: 即将结束。
*   **CD (Completed)**: 已完成。
*   **F (Failed)**: 失败。

### 取消作业 (`scancel`)
```bash
scancel 12345       # 取消特定 ID 的作业
scancel -u username # 取消该用户的所有作业 (慎用！)
```

### 查看历史与详情
*   `scontrol show job 12345`: 查看运行中作业的极其详细的技术信息（如具体分配了哪些核）。
*   `sacct -j 12345`: 查看**历史**作业的信息（如实际运行时间、内存峰值）。这是 PBS 比较欠缺的功能。

## 3.4 核心命令 `srun`
Slurm 的一个独特之处在于 `srun` 命令。
*   **在脚本内**: 它作为“启动器”，类似于 `mpirun`。`srun ./my_program` 会自动根据 `#SBATCH` 的设置，把程序分发到各个节点运行。
*   **在命令行**: 它可以启动一个交互式作业。

### 交互式作业
```bash
# 申请 1 节点 1 核心，进入 bash 环境
srun -N 1 -c 1 -t 30:00 --pty /bin/bash
```

## 3.5 高级用法

*   **作业数组 (Arrays)**: 处理批处理任务的神器。
    *   `#SBATCH --array=1-100`
    *   脚本中通过 `$SLURM_ARRAY_TASK_ID` 区分当前是第几个任务。
*   **GPU 作业**:
    *   `--gres=gpu:1`: Generic Resource 语法，申请 1 个 GPU。
*   **依赖作业 (Dependency)**:
    *   `sbatch --dependency=afterok:12345 next_job.slurm`: 只有当 12345 成功跑完，next_job 才会开始排队。

## 下一步
请参考 `examples/` 文件夹中的 Slurm 脚本模板。
