# Slurm 调度系统（重点）

> 本节给出Slurm的常用命令与作业脚本模板：基础作业、数组作业、GPU作业、多节点（MPI）作业。

## 📋 概述

Slurm的核心思路：

- 你写一个作业脚本（通常以 `.slurm` 结尾）
- 用 `sbatch` 提交
- 用 `squeue/scontrol` 查看状态
- 失败了看 `--output/--error` 指定的日志

## 🎯 学习目标

- 会写 `#SBATCH` 指令请求资源
- 会设置日志输出位置（含 `%j` 作业ID）
- 会写数组作业并用 `SLURM_ARRAY_TASK_ID` 映射参数
- 会写GPU资源请求（`--gres=gpu:1`）
- 知道多节点并行通常通过 `srun` 启动（MPI/多进程）

---

## 常用命令速查

```bash
# 提交
sbatch job.slurm

# 查看队列
squeue -u $USER

# 查看作业详情
scontrol show job <job_id>

# 取消作业
scancel <job_id>

# 查看分区信息
sinfo

# 交互资源申请（集群允许时）
salloc -p <partition> -N 1 -c 4 --mem=8G -t 00:30:00

# 交互运行
srun -p <partition> -N 1 -c 4 --mem=8G -t 00:10:00 bash
```

---

## 作业脚本要点

### 常见 #SBATCH 指令

| 指令 | 说明 |
|------|------|
| `--job-name` | 作业名 |
| `--partition` | 分区（队列） |
| `--nodes` | 节点数 |
| `--ntasks` | 任务数（MPI rank数/进程数） |
| `--cpus-per-task` | 每任务CPU核数 |
| `--mem` / `--mem-per-cpu` | 内存 |
| `--time` | 最大运行时长 |
| `--output` / `--error` | stdout/stderr日志路径 |
| `--array` | 数组作业 |
| `--gres=gpu:N` | GPU资源 |

### 常用环境变量

- `SLURM_JOB_ID`：作业ID
- `SLURM_JOB_NAME`：作业名
- `SLURM_SUBMIT_DIR`：提交目录
- `SLURM_NODELIST`：分配到的节点列表
- `SLURM_ARRAY_TASK_ID`：数组任务编号

---

## 示例脚本

- 基础作业： [basic-job.slurm](basic-job.slurm)
- 数组作业： [array-job.slurm](array-job.slurm)
- GPU作业： [gpu-job.slurm](gpu-job.slurm)
- 多节点作业： [multi-node.slurm](multi-node.slurm)

> ⚠️ 注意：示例中的 `--partition`、`--time`、`--mem`、`--gres` 需要按你集群实际情况调整。
