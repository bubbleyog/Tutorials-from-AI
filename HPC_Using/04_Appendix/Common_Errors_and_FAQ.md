# 常见错误与解答 (FAQ)

在使用 HPC 过程中，遇到错误是常态。这里收集了一些最常见的问题及其排查思路。

## 1. 作业状态类

### Q: 这里的作业一直是 `PD` (Pending) 或 `Q` (Queued) 状态，不运行？
**A: 原因可能有很多，请使用 `scontrol show job <jobid>` (Slurm) 或 `qstat -f <jobid>` (PBS) 查看原因。**
*   **Reason: Resources**: 集群正忙，没有足够的空闲节点。请耐心等待。
*   **Reason: Priority**: 你的优先级较低（可能最近跑了太多任务），被排在别人后面。
*   **Reason: AssocGrpBillingMinutes**: 你的账号机时耗尽了。
*   **Reason: Dependency**: 设置了依赖关系，前置作业还没跑完。
*   **Reason: QOSMaxJobsPerUserLimit**: 你同时运行的作业数达到了管理员设置的上限。

### Q: 作业一运行就变成 `C` 或 `CD`，但是没有结果？
**A: 这种通常是“秒退”，说明并在还没开始算就挂了。**
*   检查 `.e` (Error) 日志文件。
*   **常见原因 1**: 路径错误。脚本里没有写 `cd $PBS_O_WORKDIR`，导致程序在 Home 目录下找不到输入文件。
*   **常见原因 2**: 模块没加载。脚本里直接运行 `python` 但没写 `module load python`。
*   **常见原因 3**: 脚本权限。偶尔会因为脚本本身没有执行权限（`chmod +x`），或者格式是 DOS 格式（见下文）。

## 2. 资源报错类

### Error: `OOM` / `Out Of Memory` / `Kill signal 9`
**A: 你的程序申请的内存超过了你在脚本里申请的限制。**
*   **解决**: 增加 `--mem` (Slurm) 或 `mem=` (PBS) 的数值。
*   **注意**: 也不要无脑申请几百 G，申请越大，排队时间通常越长。

### Error: `Time Limit Exceeded` / `DUE TO TIME LIMIT`
**A: 程序运行时间超过了申请的 `walltime`。**
*   Scheduler 极其严格，说 1 小时停就 1 小时停，多一秒都不行。
*   **解决**: 预估时间时留出 20% 的余量。如果程序支持 Checkpoint (断点续传)，请务必开启。

## 3. SSH 与登录类

### Error: `Permission denied (publickey,password).`
**A: 密码错误或 SSH Key 没配置好。**
*   注意：Linux 输入密码不回显。
*   检查是否因为连续输错密码导致 IP 被暂时封禁（Fail2ban）。

### Error: `module: command not found`
**A: 这是因为你在脚本开头使用了 `/bin/sh` 而不是 `/bin/bash`，或者环境变量没初始化。**
*   确保脚本第一行是 `#!/bin/bash`。
*   如果在脚本中 source `.bashrc` 可能会解决，但不推荐（可能污染环境）。

## 4. 杂项

### Error: `^M: bad interpreter: No such file or directory`
**A: 这是经典的文件格式问题。**
*   **原因**: 脚本是在 Windows 下编辑的，换行符是 `CRLF` (Windows 标准)，而 Linux 只认 `LF`。
*   **解决**:
    *   在 Linux 下运行 `dos2unix script.sh`。
    *   或者在 Vim 中输入 `:set ff=unix` 然后保存。

### Error: Python `ModuleNotFoundError`
**A: 即使 `module load python` 了，还是找不到包。**
*   **原因**: 集群自带的 Python 基本只有标准库。你需要用 `pip install --user` 安装包到个人目录，或者使用 Conda 虚拟环境（推荐）。
