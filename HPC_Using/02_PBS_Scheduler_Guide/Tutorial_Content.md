# 第二部分：PBS 调度系统实战

**PBS (Portable Batch System)** 是最经典的高性能计算作业调度系统之一。本章将教你如何通过 PBS "提交" 作业，而不是像在个人电脑上那样直接运行程序。

## 2.1 为什么要使用调度系统？

在 HPC 集群上，成百上千个用户共享资源。如果大家都直接登录到节点上运行程序，系统会立刻崩溃。
调度系统（Scheduler）就像一个**交通指挥官**：
1.  你提交一个“任务申请单”（作业脚本）。
2.  指挥官根据你需要的资源（如 CPUs 数量、内存大小），把你安排到空闲的计算节点上。
3.  任务运行结束后，自动释放资源给下一个人。

## 2.2 基本作业提交 (`qsub`)

提交作业最核心的命令是 `qsub` (Queue SUBmit)。你需要编写一个 `.pbs` 后缀的脚本文件。

### PBS 脚本结构
一个标准的 PBS 脚本分为两部分：
1.  **Directive Header (指令头)**: 以 `#PBS` 开头的行，告诉调度器你需要什么资源。
2.  **Execution Block (执行块)**: 普通的 Shell 命令，实际运行的内容。

### 核心参数详解
| 参数 | 含义 | 示例 |
| :--- | :--- | :--- |
| `-N name` | 作业名称 | `#PBS -N MySimulation` |
| `-l nodes=X:ppn=Y` | 资源申请 | `#PBS -l nodes=1:ppn=20` (1个节点，每个节点20核) |
| `-l walltime=HH:MM:SS` | 预计运行时间 | `#PBS -l walltime=24:00:00` (如果超时会被强制杀掉) |
| `-q queue_name` | 指定队列 | `#PBS -q batch` |
| `-j oe` | 合并输出 | 将标准输出(stdout)和错误输出(stderr)合并到一个文件 |
| `-o filename` | 指定输出文件 | `#PBS -o my_job.log` |

### 提交命令
```bash
qsub examples/01_basic_job.pbs
```
提交成功后，屏幕会显示一个作业 ID（如 `12345.hpc-cluster`）。

## 2.3 作业管理与监控

作业提交后，你需要查看它的状态。

### 查看状态 (`qstat`)
*   `qstat`: 查看自己的所有作业。
*   `qstat -a`: 显示更详细的信息。
*   `qstat -n`: 显示作业被分配到了哪些节点上。

**状态代码含义**:
*   **Q (Queued)**: 排队中，等待资源。
*   **R (Running)**: 正在运行。
*   **C (Completed)**: 已完成（或即使出错只要结束了也是 C）。
*   **H (Held)**: 被挂起（通常是因为依赖或管理员操作）。

### 删除作业 (`qdel`)
如果发现脚本写错了，或者不想跑了，可以使用 `qdel` 强制取消。
```bash
qdel 12345   # 这里的 12345 是你的作业 ID
```

### 查看作业详情 (`qstat -f`)
如果作业排队很久没运行，或者出错退出，可以用全量信息查看原因：
```bash
qstat -f 12345
```

## 2.4 高级用法 (MPI, OpenMP, GPU)

大部分 HPC 任务是并行的。

*   **MPI (跨节点并行)**: 适用于大型仿真。需要使用 `mpirun` 或 `mpiexec` 配合 PBS 的 nodefile 使用。参见 `examples/02_mpi_job.pbs`。
*   **OpenMP (单节点多线程)**: 适用于利用单台机器的多个核心。通过环境变量 `OMP_NUM_THREADS` 控制。参见 `examples/03_openmp_job.pbs`。
*   **GPU 作业**: 深度学习通常需要 GPU。申请语法通常是 `nodes=1:ppn=1:gpus=1`。参见 `examples/04_gpu_job.pbs`。
*   **作业数组 (Job Arrays)**: 当你需要处理 100 个数据文件时，不要写 100 个脚本。使用 `-t` 参数。

## 2.5 交互式作业 (`qsub -I`)
有时你需要像在本地电脑一样，进入一个计算节点进行调试、编译代码或数据探索。**不要在登录节点做这些事！** 请申请一个交互式作业。

```bash
qsub -I -l nodes=1:ppn=4 -l walltime=01:00:00 -q debug
```
*   `-I`: Interactive (交互式)。
*   命令执行后，你的终端提示符会从登录节点变为计算节点（如 `node01`）。
*    Logout 退出后，作业自动结束。

## 下一步
请仔细阅读 `examples/` 目录下的脚本模板。大部分情况下，你只需要复制这些模板，修改核心命令即可。
