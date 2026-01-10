# 第8章：高性能计算调度系统（HPC Schedulers）

> 本章介绍HPC集群作业调度系统的核心概念与实战脚本模板（重点：Slurm），帮助你把“在服务器上跑程序”升级为“在集群上稳定提交与管理作业”。

## 📋 本章概述

在HPC集群上，用户通常不能直接在登录节点长时间跑计算任务，而是需要：

- 编写作业脚本（job script）描述资源需求与执行命令
- 提交作业到调度系统（scheduler），由系统安排到计算节点执行
- 通过命令查看队列、取消作业、排查失败原因

本章内容以**可直接复用的脚本模板**为主，并强调日志、可复现与排障。

## 🎯 学习目标

完成本章学习后，你将能够：

- 理解调度系统的基本概念：节点/分区(队列)/资源/时间限制
- 使用Slurm提交与管理作业（`sbatch/squeue/scancel/sinfo`）
- 编写Slurm作业脚本：资源请求、输出日志、数组作业、GPU、多节点
- 了解PBS/Torque与SGE的基本作业脚本写法与常用命令

---

## 8.1 核心概念速读

- **登录节点（login node）**：用于编辑代码/提交作业/查看状态，不用于重计算。
- **计算节点（compute node）**：真正执行作业的机器。
- **分区/队列（partition/queue）**：资源池的逻辑划分（不同限制/不同硬件）。
- **作业（job）**：一次提交的任务。
- **资源请求**：CPU核数、内存、运行时长、GPU数量、节点数等。
- **日志（stdout/stderr）**：作业输出与错误输出，排障的第一入口。

> ⚠️ 注意：不同集群配置差异很大（分区名、GPU型号、MPI实现、时间限制等）。请把本章脚本中的占位符改成你集群的实际配置。

---

## 8.2 Slurm（重点）

📁 子章节： [01-slurm/README.md](01-slurm/README.md)

### 常用命令速查

```bash
# 提交作业
sbatch job.slurm

# 查看队列
squeue -u $USER

# 查看作业详情
scontrol show job <job_id>

# 取消作业
scancel <job_id>

# 查看分区与节点状态
sinfo
```

---

## 8.3 PBS/Torque

📁 子章节： [02-pbs/README.md](02-pbs/README.md)

---

## 8.4 SGE（Sun Grid Engine）

📁 子章节： [03-sge/README.md](03-sge/README.md)

---

## 8.5 最佳实践

📄 文档： [04-best-practices.md](04-best-practices.md)

---

## 📦 本章文件

- Slurm:
  - [01-slurm/basic-job.slurm](01-slurm/basic-job.slurm)
  - [01-slurm/array-job.slurm](01-slurm/array-job.slurm)
  - [01-slurm/gpu-job.slurm](01-slurm/gpu-job.slurm)
  - [01-slurm/multi-node.slurm](01-slurm/multi-node.slurm)
- PBS/Torque:
  - [02-pbs/basic-job.pbs](02-pbs/basic-job.pbs)
- SGE:
  - [03-sge/basic-job.sge](03-sge/basic-job.sge)
- Best practices:
  - [04-best-practices.md](04-best-practices.md)
