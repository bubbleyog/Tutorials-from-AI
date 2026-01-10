# PBS/Torque 调度系统

> 本节提供PBS/Torque的基础概念与作业脚本模板，便于从Slurm迁移时快速上手。

## 常用命令速查

```bash
# 提交
qsub job.pbs

# 查看队列
qstat -u $USER

# 查看作业详情（不同PBS实现选项略有差异）
qstat -f <job_id>

# 取消
qdel <job_id>
```

---

## PBS脚本指令要点

PBS作业脚本通常以 `#PBS` 开头指定资源与行为，例如：

- `#PBS -N name`：作业名
- `#PBS -q queue`：队列
- `#PBS -l select=...`：资源选择（节点/核/内存等，写法因版本而异）
- `#PBS -l walltime=HH:MM:SS`：最长运行时间
- `#PBS -o /path/out.log`：stdout
- `#PBS -e /path/err.log`：stderr

> ⚠️ 注意：PBS生态存在多种实现（PBS Pro / OpenPBS / Torque），资源请求语法可能不同。本章示例采用较常见的写法，实际请以你集群文档为准。

---

## 示例脚本

- 基础作业： [basic-job.pbs](basic-job.pbs)
