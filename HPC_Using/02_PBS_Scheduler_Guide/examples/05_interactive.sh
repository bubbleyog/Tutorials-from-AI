#!/bin/bash

# 也可以将交互式作业的申请命令写成一个 Alias 或小脚本放在 ~/bin 下
# 方便随时调用

# 1. 普通调试 (CPU)
# 申请 1 核，30分钟
qsub -I -N Interactive_Debug -l nodes=1:ppn=1 -l walltime=00:30:00 -q debug

# 2. 交互式使用 GPU
# 有些集群支持交互式使用 GPU 进行 Notebook 调试
# qsub -I -N GPU_Debug -l nodes=1:ppn=1:gpus=1 -q gpu

# 提示:
# 当你运行上述命令后，终端会“卡住”一会，等待调度器分配资源。
# 一旦分配成功，你会发现命令行提示符的主机名变了 (例如从 login01 变成了 node05)。
# 这时你就可以像在本地一样运行程序了。
# 输入 `exit` 即可结束作业并返回登录节点。
