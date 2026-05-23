# 第一部分：Linux 基础与 HPC 环境入门

本章将介绍使用 HPC（高性能计算）集群所需的基础知识。哪怕你之前没有太多 Linux 经验，通过本章的学习，你也能够掌握登录集群、管理文件、配置环境以及监控任务的基本技能。

## 1.1 登录与连接

HPC 集群通常运行在 Linux 操作系统上，用户通过 SSH (Secure Shell) 协议进行远程连接。

### 客户端选择
*   **Windows**: 推荐使用 [MobaXterm](https://mobaxterm.mobatek.net/) (功能全，自带文件传输) 或 [Windows Terminal](https://github.com/microsoft/terminal) (自带 OpenSSH)。
*   **Mac/Linux**: 直接使用终端 (Terminal)。

### 基本登录命令
在终端中输入以下命令，替换 `username` 为你的账号，`hpc.example.com` 为集群地址：

```bash
ssh username@hpc.example.com
```

输入密码时屏幕不会显示任何字符，输完直接回车即可。

### 进阶：配置 SSH Config (简化登录)
每次输入长长的地址很麻烦，可以配置 `~/.ssh/config` 文件。

1.  在本地电脑上编辑配置文件：`nano ~/.ssh/config`
2.  添加如下内容：

```text
Host myhpc
    HostName hpc.example.com
    User username
    Port 22
```

之后只需输入 `ssh myhpc` 即可登录。

## 1.2 文件管理与传输

### 常用文件操作命令
HPC 没有图形界面，你需要习惯命令行操作。

| 命令 | 作用 | 示例 |
| :--- | :--- | :--- |
| `ls` | 列出文件 | `ls -lh` (显示详细信息和易读大小) |
| `cd` | 切换目录 | `cd /path/to/dir`, `cd ..` (上一级), `cd ~` (回主目录) |
| `pwd` | 显示当前路径 | `pwd` |
| `mkdir` | 创建文件夹 | `mkdir my_project` |
| `cp` | 复制 | `cp file1 file2`, `cp -r dir1 dir2` (复制文件夹) |
| `mv` | 移动/重命名 | `mv oldname newname` |
| `rm` | 删除 (慎用！) | `rm file`, `rm -rf dir` (强制删除文件夹，不可恢复) |

### 权限管理
Linux 文件权限分为：读 (r), 写 (w), 执行 (x)。
*   `chmod +x script.sh`: 给脚本添加执行权限。
*   `ls -l`: 查看权限 (如 `-rw-r--r--` 表示所有者可读写，其他人只读)。

### 文件传输
将文件从本地上传到集群，或从集群下载。

*   **SCP (命令行)**:
    *   上传: `scp local_file username@hpc.example.com:~/remote_dir`
    *   下载: `scp username@hpc.example.com:~/remote_file local_dir`
*   **SFTP 客户端**: MobaXterm, FileZilla 等软件支持拖拽上传下载，更适合新手。

## 1.3 文本编辑与查看

在集群上修改代码或配置文件是常态。

*   **nano**: 简单易用的编辑器。
    *   `nano filename` 打开文件。
    *   `Ctrl+O` 保存，`Ctrl+X` 退出。
*   **vim**: 强大的编辑器 (陡峭的学习曲线)。
    *   `i` 进入插入模式。
    *   `Esc` 退出模式，输入 `:wq` 保存退出，`:q!` 强制不保存退出。
*   **查看文件**:
    *   `cat file`: 显示全部内容。
    *   `less file`: 分页查看 (按 `q` 退出)。
    *   `head -n 10 file`: 看前10行。
    *   `tail -n 10 file`: 看后10行 (常用于查看日志)。

## 1.4 HPC 环境配置 (Environment Modules)

HPC 集群上安装了成百上千个软件，版本各异。为了避免冲突，HPC 使用 **Environment Modules** 系统来管理软件环境。

### 核心概念
默认情况下，除了基础系统工具，你是无法直接使用某些专业软件（如 Python 3.9, GCC 11, CUDA 12）的。你需要“加载”对应的模块。

### 常用命令
| 命令 | 作用 |
| :--- | :--- |
| `module avail` | 列出系统中所有可用的软件模块 |
| `module avail python` | 搜索包含 "python" 的模块 |
| `module load <name>` | 加载指定模块 (如 `module load python/3.8`) |
| `module list` | 查看当前已加载的模块 |
| `module unload <name>` | 卸载指定模块 |
| `module purge` | 清除所有已加载的模块 (重置环境) |

### 环境变量
加载模块本质上是在修改环境变量。
*   `PATH`: 决定了系统去哪里寻找可执行程序。
*   `LD_LIBRARY_PATH`: 决定了程序去哪里寻找动态链接库 (.so 文件)。

## 1.5 进程与资源监控

查看你的程序是否在运行，以及占用了多少资源。

*   **htop / top**: 实时显示系统进程。可以看到 CPU 和 内存使用率。
    *   注意：**不要在登录节点运行高负荷计算任务！** 登录节点是大家共享用来提交作业的。
*   **ps**: 查看当前用户的进程。
    *   `ps -ef | grep username`
*   **kill**: 结束进程。
    *   `kill <PID>` (PID 是进程 ID，可从 ps 或 top 中看到)
    *   `kill -9 <PID>` (强制结束)

## 下一步
熟悉了这些基础操作后，你就可以开始编写脚本并在集群上提交作业了。请查看 `examples/` 目录下的示例脚本，并阅读 `Example_Code_Explanations.md` 了解详情。
