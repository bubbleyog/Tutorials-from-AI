# 第3章：进程与后台任务

> 本章介绍Linux进程管理和后台任务运行，这是服务器任务管理的核心技能。

## 📋 本章概述

在服务器上运行长时间任务时，理解进程管理是必不可少的。本章将介绍如何在后台运行任务、管理进程生命周期、以及在断开SSH连接后保持任务继续运行。

## 🎯 学习目标

完成本章学习后，你将能够：

- 在前台和后台之间切换任务
- 使用nohup和disown保持任务运行
- 使用screen/tmux管理多个会话
- 监控和控制进程
- 使用trap处理信号

---

## 3.1 前台与后台

### 基本概念

- **前台进程**：占用终端，用户可以与之交互
- **后台进程**：不占用终端，在后台静默运行
- **作业（Job）**：Shell管理的进程组

### 后台运行

```bash
# 启动时放入后台（添加 &）
./long_running_task.sh &

# 查看后台作业
jobs
jobs -l    # 显示PID

# 输出示例：
# [1]+  Running                 ./long_running_task.sh &
# [2]-  Stopped                 vim file.txt
```

### 前后台切换

```bash
# 将前台任务暂停并放入后台
# 按 Ctrl+Z

# 查看暂停的作业
jobs

# 将作业恢复到前台运行
fg           # 恢复最近的作业
fg %1        # 恢复作业1
fg %+        # 恢复当前作业
fg %-        # 恢复上一个作业

# 将作业恢复到后台运行
bg           # 恢复最近的作业到后台
bg %1        # 恢复作业1到后台
```

### 作业标识符

| 标识符 | 说明 |
|--------|------|
| `%n` | 作业号为n的作业 |
| `%+` 或 `%%` | 当前作业 |
| `%-` | 上一个作业 |
| `%string` | 命令以string开头的作业 |
| `%?string` | 命令包含string的作业 |

### 示例

```bash
# 启动多个后台任务
sleep 100 &
sleep 200 &
sleep 300 &

# 查看作业
jobs -l
# [1]   12345 Running                 sleep 100 &
# [2]-  12346 Running                 sleep 200 &
# [3]+  12347 Running                 sleep 300 &

# 终止特定作业
kill %2

# 等待所有后台作业完成
wait

# 等待特定作业完成
wait %1
wait 12345   # 使用PID
```

📄 **示例脚本**: [01-background.sh](01-background.sh)

---

## 3.2 保持任务运行

### 问题：SSH断开后任务终止

当你断开SSH连接时，Shell会向其子进程发送SIGHUP信号，导致进程终止。以下方法可以避免这个问题。

### 方法1：nohup

```bash
# 基本用法
nohup command &

# 输出会保存到 nohup.out
nohup ./script.sh &

# 指定输出文件
nohup ./script.sh > output.log 2>&1 &

# 丢弃输出
nohup ./script.sh > /dev/null 2>&1 &

# 查看输出
tail -f nohup.out
```

### 方法2：disown

```bash
# 启动后台任务
./script.sh &

# 从作业表中移除（断开与Shell的关联）
disown

# 移除特定作业
disown %1

# 移除所有作业
disown -a

# 标记作业，使其不接收SIGHUP
disown -h %1
```

### 方法3：setsid

```bash
# 在新会话中运行（完全脱离终端）
setsid ./script.sh

# 结合重定向
setsid ./script.sh > output.log 2>&1
```

### 方法4：使用括号创建子Shell

```bash
# 在子Shell中运行
(./script.sh &)

# 结合nohup
(nohup ./script.sh > output.log 2>&1 &)
```

### 比较

| 方法 | 特点 | 适用场景 |
|------|------|----------|
| `nohup` | 简单，自动处理SIGHUP | 简单的长时间任务 |
| `disown` | 可以对已运行的任务使用 | 忘记用nohup时补救 |
| `setsid` | 完全脱离终端 | 需要独立会话的任务 |
| `screen/tmux` | 可以重新连接 | 需要交互的长时间任务 |

📄 **示例脚本**: [02-nohup-screen.sh](02-nohup-screen.sh)

---

## 3.3 终端复用器

### Screen

Screen是一个终端复用器，允许你创建多个虚拟终端，并在断开连接后重新连接。

#### 基本操作

```bash
# 安装（如果未安装）
sudo apt install screen    # Debian/Ubuntu
sudo yum install screen    # CentOS/RHEL

# 创建新会话
screen                     # 匿名会话
screen -S mysession        # 命名会话

# 分离会话（保持运行）
# 按 Ctrl+A 然后按 D

# 查看所有会话
screen -ls

# 重新连接会话
screen -r                  # 连接唯一会话
screen -r mysession        # 连接指定会话
screen -r 12345            # 使用会话ID连接

# 强制分离并重连
screen -d -r mysession

# 终止会话
screen -X -S mysession quit
# 或在会话中输入 exit
```

#### 常用快捷键

所有快捷键都以 `Ctrl+A` 开头：

| 快捷键 | 说明 |
|--------|------|
| `Ctrl+A d` | 分离当前会话 |
| `Ctrl+A c` | 创建新窗口 |
| `Ctrl+A n` | 下一个窗口 |
| `Ctrl+A p` | 上一个窗口 |
| `Ctrl+A "` | 窗口列表 |
| `Ctrl+A A` | 重命名窗口 |
| `Ctrl+A k` | 关闭当前窗口 |
| `Ctrl+A [` | 进入复制模式 |
| `Ctrl+A ]` | 粘贴 |
| `Ctrl+A ?` | 帮助 |

#### 配置文件 ~/.screenrc

```bash
# 关闭启动消息
startup_message off

# 设置滚动缓冲区大小
defscrollback 10000

# 状态栏
hardstatus alwayslastline
hardstatus string '%{= kG}[ %{G}%H %{g}][%= %{= kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B} %m-%d %{W}%c %{g}]'

# 默认Shell
shell -$SHELL
```

### Tmux

Tmux是更现代的终端复用器，功能更强大。

#### 基本操作

```bash
# 安装
sudo apt install tmux      # Debian/Ubuntu
sudo yum install tmux      # CentOS/RHEL

# 创建新会话
tmux                       # 匿名会话
tmux new -s mysession      # 命名会话

# 分离会话
# 按 Ctrl+B 然后按 D

# 查看所有会话
tmux ls

# 重新连接
tmux attach                # 连接最近的会话
tmux attach -t mysession   # 连接指定会话
tmux a -t mysession        # 简写

# 终止会话
tmux kill-session -t mysession
```

#### 常用快捷键

所有快捷键都以 `Ctrl+B` 开头：

| 快捷键 | 说明 |
|--------|------|
| `Ctrl+B d` | 分离会话 |
| `Ctrl+B c` | 创建新窗口 |
| `Ctrl+B n` | 下一个窗口 |
| `Ctrl+B p` | 上一个窗口 |
| `Ctrl+B w` | 窗口列表 |
| `Ctrl+B ,` | 重命名窗口 |
| `Ctrl+B &` | 关闭窗口 |
| `Ctrl+B %` | 垂直分屏 |
| `Ctrl+B "` | 水平分屏 |
| `Ctrl+B 方向键` | 切换面板 |
| `Ctrl+B x` | 关闭面板 |
| `Ctrl+B [` | 进入复制模式 |
| `Ctrl+B ?` | 帮助 |

#### 配置文件 ~/.tmux.conf

```bash
# 设置前缀键为 Ctrl+A（类似screen）
# unbind C-b
# set -g prefix C-a
# bind C-a send-prefix

# 启用鼠标支持
set -g mouse on

# 设置历史记录大小
set -g history-limit 10000

# 窗口编号从1开始
set -g base-index 1
setw -g pane-base-index 1

# 状态栏
set -g status-bg black
set -g status-fg white
set -g status-left '#[fg=green]#H '
set -g status-right '#[fg=yellow]%Y-%m-%d %H:%M'

# 快速重载配置
bind r source-file ~/.tmux.conf \; display "Config reloaded!"
```

### Screen vs Tmux

| 特性 | Screen | Tmux |
|------|--------|------|
| 分屏 | 基础支持 | 强大灵活 |
| 配置 | 简单 | 更可定制 |
| 脚本化 | 基础 | 强大 |
| 复制模式 | 基础 | Vi/Emacs风格 |
| 社区 | 成熟稳定 | 活跃开发 |
| 学习曲线 | 较低 | 稍高 |

📄 **示例脚本**: [02-nohup-screen.sh](02-nohup-screen.sh)

---

## 3.4 进程监控

### ps - 进程快照

```bash
# 查看当前用户的进程
ps

# 查看所有进程（BSD风格）
ps aux

# 查看所有进程（Unix风格）
ps -ef

# 查看进程树
ps auxf
ps -ejH

# 查看特定用户的进程
ps -u username

# 查看特定进程
ps -p 1234

# 自定义输出格式
ps -eo pid,ppid,user,%cpu,%mem,cmd

# 查找特定进程
ps aux | grep python
ps -C python           # 按命令名查找

# 按CPU或内存排序
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

### top - 实时监控

```bash
# 启动top
top

# 常用交互命令：
# q - 退出
# h - 帮助
# k - 终止进程
# r - 修改优先级
# M - 按内存排序
# P - 按CPU排序
# c - 显示完整命令
# 1 - 显示每个CPU核心
# u - 过滤用户

# 命令行选项
top -u username        # 只显示特定用户
top -p 1234,5678       # 只显示特定PID
top -n 5               # 更新5次后退出
top -b -n 1            # 批处理模式（适合脚本）
```

### htop - 增强版top

```bash
# 安装
sudo apt install htop

# 启动
htop

# 特点：
# - 彩色显示
# - 鼠标支持
# - 垂直和水平滚动
# - 更直观的进程管理
```

### 其他监控工具

```bash
# pgrep - 按名称查找进程
pgrep python
pgrep -u root sshd
pgrep -l python        # 显示进程名
pgrep -a python        # 显示完整命令

# pidof - 获取进程ID
pidof nginx

# pstree - 进程树
pstree
pstree -p              # 显示PID
pstree -u              # 显示用户

# lsof - 查看进程打开的文件
lsof -p 1234           # 特定进程
lsof -u username       # 特定用户
lsof -i :8080          # 使用特定端口

# fuser - 查看文件/端口被谁使用
fuser /path/to/file
fuser -n tcp 8080
```

📄 **示例脚本**: [03-process-control.sh](03-process-control.sh)

---

## 3.5 信号处理

### 常用信号

| 信号 | 编号 | 说明 | 默认行为 |
|------|------|------|----------|
| SIGHUP | 1 | 挂起（终端断开） | 终止 |
| SIGINT | 2 | 中断（Ctrl+C） | 终止 |
| SIGQUIT | 3 | 退出（Ctrl+\） | 终止+core |
| SIGKILL | 9 | 强制终止 | 不可捕获 |
| SIGTERM | 15 | 请求终止 | 终止 |
| SIGSTOP | 19 | 暂停 | 不可捕获 |
| SIGCONT | 18 | 继续 | 继续执行 |
| SIGUSR1 | 10 | 用户定义1 | 终止 |
| SIGUSR2 | 12 | 用户定义2 | 终止 |

### kill - 发送信号

```bash
# 发送默认信号（SIGTERM）
kill 1234

# 发送特定信号
kill -9 1234           # SIGKILL
kill -SIGTERM 1234     # 使用名称
kill -15 1234          # 使用编号

# 终止进程组
kill -TERM -1234       # 负号表示进程组

# 终止所有同名进程
killall python
killall -9 python

# 按模式终止
pkill python
pkill -u root python
pkill -f "python script.py"   # 匹配完整命令
```

### trap - 信号捕获

```bash
#!/bin/bash

# 定义清理函数
cleanup() {
    echo "正在清理..."
    rm -f /tmp/myapp.pid
    exit 0
}

# 捕获信号
trap cleanup SIGINT SIGTERM

# 捕获退出（无论什么原因）
trap cleanup EXIT

# 忽略信号
trap '' SIGINT

# 恢复默认处理
trap - SIGINT

# 显示当前trap设置
trap -p
```

### 实用示例

```bash
#!/bin/bash

# 创建PID文件
echo $$ > /tmp/myapp.pid

# 清理函数
cleanup() {
    echo "收到终止信号，正在清理..."
    rm -f /tmp/myapp.pid
    rm -f /tmp/myapp.lock
    # 终止子进程
    jobs -p | xargs -r kill
    exit 0
}

# 错误处理
on_error() {
    echo "发生错误，行号: $1"
    cleanup
}

# 设置trap
trap cleanup SIGINT SIGTERM SIGHUP
trap 'on_error $LINENO' ERR

# 主程序
echo "程序运行中... (PID: $$)"
while true; do
    sleep 1
done
```

📄 **示例脚本**: [03-process-control.sh](03-process-control.sh)

---

## 3.6 实用技巧

### 并行执行

```bash
# 使用 & 并行运行多个任务
task1 &
task2 &
task3 &
wait   # 等待所有任务完成

# 使用 xargs 并行
find . -name "*.txt" | xargs -P 4 -I {} process {}

# 使用 GNU parallel（如果安装了）
parallel -j 4 process ::: file1 file2 file3 file4
```

### 限制资源

```bash
# 限制CPU时间
timeout 60 ./long_task.sh

# 限制内存（使用ulimit）
ulimit -v 1000000    # 限制虚拟内存
./memory_intensive_task.sh

# 降低优先级
nice -n 19 ./low_priority_task.sh

# 修改运行中进程的优先级
renice -n 10 -p 1234
```

### 后台任务日志

```bash
# 带时间戳的日志
./script.sh 2>&1 | while IFS= read -r line; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') $line"
done >> output.log &

# 使用 ts 命令（moreutils包）
./script.sh 2>&1 | ts '%Y-%m-%d %H:%M:%S' >> output.log &
```

### 检查进程是否运行

```bash
# 使用 pgrep
if pgrep -x "nginx" > /dev/null; then
    echo "Nginx is running"
fi

# 使用 PID 文件
if [[ -f /var/run/myapp.pid ]]; then
    pid=$(cat /var/run/myapp.pid)
    if kill -0 "$pid" 2>/dev/null; then
        echo "Process is running (PID: $pid)"
    else
        echo "PID file exists but process is not running"
    fi
fi
```

---

## 📝 快速参考

### 常用命令速查

| 任务 | 命令 |
|------|------|
| 后台运行 | `command &` |
| 查看作业 | `jobs -l` |
| 切到前台 | `fg %1` |
| 切到后台 | `bg %1` |
| 暂停进程 | `Ctrl+Z` |
| 断开仍运行 | `nohup command &` |
| 分离已运行 | `disown %1` |
| 终止进程 | `kill PID` |
| 强制终止 | `kill -9 PID` |
| 查看进程 | `ps aux` |
| 实时监控 | `top` 或 `htop` |

### Screen/Tmux速查

| 操作 | Screen | Tmux |
|------|--------|------|
| 新建会话 | `screen -S name` | `tmux new -s name` |
| 分离 | `Ctrl+A d` | `Ctrl+B d` |
| 列出会话 | `screen -ls` | `tmux ls` |
| 重连 | `screen -r name` | `tmux a -t name` |
| 新窗口 | `Ctrl+A c` | `Ctrl+B c` |
| 切换窗口 | `Ctrl+A n/p` | `Ctrl+B n/p` |

---

## 📂 本章示例文件

| 文件 | 说明 |
|------|------|
| [01-background.sh](01-background.sh) | 前后台作业管理示例 |
| [02-nohup-screen.sh](02-nohup-screen.sh) | nohup和screen/tmux使用 |
| [03-process-control.sh](03-process-control.sh) | 进程控制与信号处理 |

---

## 🎯 练习建议

1. **后台任务**：创建一个每秒输出时间的脚本，练习前后台切换
2. **nohup实践**：使用nohup运行任务，断开SSH后重连检查
3. **Screen/Tmux**：创建多窗口会话，练习分离和重连
4. **信号处理**：编写带清理函数的脚本，测试各种终止方式
5. **进程监控**：使用ps和top找出系统中最耗资源的进程

---

[← 上一章：文件与目录操作](../02-file-operations/README.md) | [下一章：Python程序自动化 →](../04-python-automation/README.md)

