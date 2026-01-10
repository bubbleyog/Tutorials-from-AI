# SGE（Sun Grid Engine）调度系统

> 本节提供SGE（含其常见衍生：Univa Grid Engine等）的基础脚本模板与常用命令。

## 常用命令速查

```bash
# 提交
qsub job.sge

# 查看队列
qstat
qstat -u $USER

# 删除作业
qdel <job_id>

# 查看作业详细信息（不同实现可能略有差异）
qstat -j <job_id>
```

---

## SGE脚本指令要点

SGE作业脚本通常以 `#$` 开头指定参数，例如：

- `#$ -N name`：作业名
- `#$ -q queue`：队列
- `#$ -cwd`：以提交目录为工作目录
- `#$ -pe smp 4`：并行环境与核数（示例：smp 4）
- `#$ -l h_rt=HH:MM:SS`：运行时长限制
- `#$ -o /path/out.log` / `#$ -e /path/err.log`：日志路径

> ⚠️ 注意：SGE的并行环境（PE）名称（如 `smp`、`mpi`）由集群管理员配置，需按实际情况修改。

---

## 示例脚本

- 基础作业： [basic-job.sge](basic-job.sge)
