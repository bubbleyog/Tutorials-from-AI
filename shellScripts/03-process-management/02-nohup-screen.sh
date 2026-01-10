#!/bin/bash
#
# 脚本名称: 02-nohup-screen.sh
# 描述: nohup、disown和终端复用器使用示例
# 用法: ./02-nohup-screen.sh
#

set -euo pipefail

echo "=== nohup与终端复用器示例 ==="
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# ============================================================
# 1. nohup 基本用法
# ============================================================
echo "--- 1. nohup 基本用法 ---"

echo "nohup 命令格式:"
echo "  nohup command &"
echo "  nohup command > output.log 2>&1 &"
echo ""

# 创建测试脚本
cat > "$TEMP_DIR/long_task.sh" << 'EOF'
#!/bin/bash
for i in {1..5}; do
    echo "$(date '+%H:%M:%S') - 运行中... ($i/5)"
    sleep 1
done
echo "任务完成!"
EOF
chmod +x "$TEMP_DIR/long_task.sh"

echo "使用 nohup 运行任务..."
cd "$TEMP_DIR"
nohup ./long_task.sh > output.log 2>&1 &
nohup_pid=$!
echo "任务已启动 (PID: $nohup_pid)"
echo "输出文件: $TEMP_DIR/output.log"

# 等待任务完成
echo ""
echo "等待任务完成..."
wait $nohup_pid 2>/dev/null || true

echo ""
echo "任务输出:"
cat "$TEMP_DIR/output.log"

# ============================================================
# 2. disown 用法
# ============================================================
echo ""
echo "--- 2. disown 用法 ---"

echo "disown 命令说明:"
echo "  disown        - 移除最近的作业"
echo "  disown %n     - 移除作业n"
echo "  disown -a     - 移除所有作业"
echo "  disown -h %n  - 标记作业n不接收SIGHUP"
echo ""

# 演示 disown
echo "启动后台任务并使用 disown..."
sleep 5 &
bg_pid=$!
echo "任务已启动 (PID: $bg_pid)"

# disown 需要在交互式Shell中才有意义
# 这里只是演示命令格式
echo "在交互式Shell中，可以执行:"
echo "  disown $bg_pid"
echo "  或"
echo "  disown %1"

# 清理
kill $bg_pid 2>/dev/null || true

# ============================================================
# 3. setsid 用法
# ============================================================
echo ""
echo "--- 3. setsid 用法 ---"

echo "setsid 命令说明:"
echo "  setsid command  - 在新会话中运行命令"
echo ""

# 创建测试脚本
cat > "$TEMP_DIR/setsid_test.sh" << 'EOF'
#!/bin/bash
echo "PID: $$, SID: $(ps -o sid= -p $$)" > /tmp/setsid_output.txt
sleep 2
echo "完成" >> /tmp/setsid_output.txt
EOF
chmod +x "$TEMP_DIR/setsid_test.sh"

echo "使用 setsid 运行任务..."
setsid "$TEMP_DIR/setsid_test.sh" &
sleep 3

if [[ -f /tmp/setsid_output.txt ]]; then
    echo "setsid 输出:"
    cat /tmp/setsid_output.txt
    rm -f /tmp/setsid_output.txt
fi

# ============================================================
# 4. Screen 命令参考
# ============================================================
echo ""
echo "--- 4. Screen 命令参考 ---"

cat << 'EOF'
Screen 基本命令:
================

创建和管理会话:
  screen -S name        创建命名会话
  screen -ls            列出所有会话
  screen -r name        重新连接到会话
  screen -d -r name     分离并重连
  screen -X -S name quit 终止会话

会话内快捷键 (Ctrl+A 后跟):
  d     分离会话
  c     创建新窗口
  n     下一个窗口
  p     上一个窗口
  "     窗口列表
  A     重命名窗口
  k     关闭当前窗口
  [     进入复制模式
  ]     粘贴
  ?     帮助

EOF

# 检查screen是否安装
if command -v screen &>/dev/null; then
    echo "Screen 版本: $(screen --version 2>&1 | head -1)"
else
    echo "Screen 未安装。安装命令:"
    echo "  Ubuntu/Debian: sudo apt install screen"
    echo "  CentOS/RHEL:   sudo yum install screen"
fi

# ============================================================
# 5. Tmux 命令参考
# ============================================================
echo ""
echo "--- 5. Tmux 命令参考 ---"

cat << 'EOF'
Tmux 基本命令:
==============

创建和管理会话:
  tmux new -s name      创建命名会话
  tmux ls               列出所有会话
  tmux attach -t name   连接到会话
  tmux kill-session -t name 终止会话

会话内快捷键 (Ctrl+B 后跟):
  d     分离会话
  c     创建新窗口
  n     下一个窗口
  p     上一个窗口
  w     窗口列表
  ,     重命名窗口
  &     关闭窗口
  %     垂直分屏
  "     水平分屏
  方向键 切换面板
  x     关闭面板
  [     进入复制模式
  ?     帮助

EOF

# 检查tmux是否安装
if command -v tmux &>/dev/null; then
    echo "Tmux 版本: $(tmux -V)"
else
    echo "Tmux 未安装。安装命令:"
    echo "  Ubuntu/Debian: sudo apt install tmux"
    echo "  CentOS/RHEL:   sudo yum install tmux"
fi

# ============================================================
# 6. 生成 Screen 配置文件示例
# ============================================================
echo ""
echo "--- 6. Screen 配置文件示例 ---"

cat << 'EOF'
推荐的 ~/.screenrc 配置:
========================

# 关闭启动消息
startup_message off

# 设置滚动缓冲区
defscrollback 10000

# 启用256色
term screen-256color

# 状态栏
hardstatus alwayslastline
hardstatus string '%{= kG}[%{G}%H%{g}][%= %{= kw}%?%-Lw%?%{r}(%{W}%n*%f%t%?(%u)%?%{r})%{w}%?%+Lw%?%?%= %{g}][%{B}%Y-%m-%d %{W}%c%{g}]'

# UTF-8支持
defutf8 on

# 自动分离
autodetach on

EOF

# ============================================================
# 7. 生成 Tmux 配置文件示例
# ============================================================
echo ""
echo "--- 7. Tmux 配置文件示例 ---"

cat << 'EOF'
推荐的 ~/.tmux.conf 配置:
=========================

# 启用鼠标支持
set -g mouse on

# 设置历史记录大小
set -g history-limit 50000

# 窗口编号从1开始
set -g base-index 1
setw -g pane-base-index 1

# 自动重新编号窗口
set -g renumber-windows on

# 256色支持
set -g default-terminal "screen-256color"

# 减少命令延迟
set -s escape-time 0

# 状态栏
set -g status-bg colour235
set -g status-fg white
set -g status-left '#[fg=green]#H '
set -g status-right '#[fg=yellow]%Y-%m-%d #[fg=white]%H:%M'

# 分屏快捷键（更直观）
bind | split-window -h
bind - split-window -v

# 快速重载配置
bind r source-file ~/.tmux.conf \; display "Config reloaded!"

# 使用vim风格的面板切换
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R

EOF

# ============================================================
# 8. 实用脚本：后台任务管理器
# ============================================================
echo ""
echo "--- 8. 后台任务管理器示例 ---"

# 创建任务管理脚本
cat > "$TEMP_DIR/task_manager.sh" << 'SCRIPT'
#!/bin/bash
#
# 简易后台任务管理器
#

TASK_DIR="${HOME}/.task_manager"
mkdir -p "$TASK_DIR"

start_task() {
    local name="$1"
    shift
    local command="$*"
    
    local pid_file="$TASK_DIR/${name}.pid"
    local log_file="$TASK_DIR/${name}.log"
    
    if [[ -f "$pid_file" ]]; then
        local old_pid=$(cat "$pid_file")
        if kill -0 "$old_pid" 2>/dev/null; then
            echo "任务 '$name' 已在运行 (PID: $old_pid)"
            return 1
        fi
    fi
    
    nohup bash -c "$command" > "$log_file" 2>&1 &
    local pid=$!
    echo "$pid" > "$pid_file"
    echo "任务 '$name' 已启动 (PID: $pid)"
    echo "日志文件: $log_file"
}

stop_task() {
    local name="$1"
    local pid_file="$TASK_DIR/${name}.pid"
    
    if [[ ! -f "$pid_file" ]]; then
        echo "任务 '$name' 不存在"
        return 1
    fi
    
    local pid=$(cat "$pid_file")
    if kill "$pid" 2>/dev/null; then
        echo "任务 '$name' 已停止 (PID: $pid)"
        rm -f "$pid_file"
    else
        echo "任务 '$name' 未在运行"
        rm -f "$pid_file"
    fi
}

status_task() {
    local name="$1"
    local pid_file="$TASK_DIR/${name}.pid"
    
    if [[ ! -f "$pid_file" ]]; then
        echo "任务 '$name': 不存在"
        return 1
    fi
    
    local pid=$(cat "$pid_file")
    if kill -0 "$pid" 2>/dev/null; then
        echo "任务 '$name': 运行中 (PID: $pid)"
    else
        echo "任务 '$name': 已停止"
    fi
}

list_tasks() {
    echo "后台任务列表:"
    echo "-------------"
    for pid_file in "$TASK_DIR"/*.pid 2>/dev/null; do
        [[ -f "$pid_file" ]] || continue
        local name=$(basename "$pid_file" .pid)
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            echo "  $name: 运行中 (PID: $pid)"
        else
            echo "  $name: 已停止"
        fi
    done
}

case "${1:-}" in
    start)
        start_task "$2" "${@:3}"
        ;;
    stop)
        stop_task "$2"
        ;;
    status)
        status_task "$2"
        ;;
    list)
        list_tasks
        ;;
    *)
        echo "用法: $0 {start|stop|status|list} [name] [command]"
        echo ""
        echo "示例:"
        echo "  $0 start mytask 'while true; do echo running; sleep 10; done'"
        echo "  $0 status mytask"
        echo "  $0 stop mytask"
        echo "  $0 list"
        ;;
esac
SCRIPT

chmod +x "$TEMP_DIR/task_manager.sh"

echo "任务管理器脚本已创建: $TEMP_DIR/task_manager.sh"
echo ""
echo "使用示例:"
echo "  $TEMP_DIR/task_manager.sh list"
"$TEMP_DIR/task_manager.sh" list

# ============================================================
# 9. 创建 Screen 会话脚本
# ============================================================
echo ""
echo "--- 9. Screen 会话脚本示例 ---"

cat > "$TEMP_DIR/start_screen_session.sh" << 'SCRIPT'
#!/bin/bash
#
# 创建预配置的Screen会话
#

SESSION_NAME="${1:-dev}"

# 检查会话是否存在
if screen -ls | grep -q "$SESSION_NAME"; then
    echo "会话 '$SESSION_NAME' 已存在，正在连接..."
    screen -r "$SESSION_NAME"
    exit 0
fi

# 创建新会话
screen -dmS "$SESSION_NAME"

# 配置窗口
screen -S "$SESSION_NAME" -X screen -t "editor" 0
screen -S "$SESSION_NAME" -X screen -t "shell" 1
screen -S "$SESSION_NAME" -X screen -t "logs" 2

# 在各窗口运行命令
screen -S "$SESSION_NAME" -p 0 -X stuff "echo '编辑器窗口'\n"
screen -S "$SESSION_NAME" -p 1 -X stuff "echo '命令行窗口'\n"
screen -S "$SESSION_NAME" -p 2 -X stuff "echo '日志窗口'\n"

# 选择第一个窗口
screen -S "$SESSION_NAME" -X select 0

echo "会话 '$SESSION_NAME' 已创建，包含3个窗口"
echo "使用 'screen -r $SESSION_NAME' 连接"
SCRIPT

chmod +x "$TEMP_DIR/start_screen_session.sh"

echo "Screen会话脚本已创建"
echo "脚本内容预览:"
head -20 "$TEMP_DIR/start_screen_session.sh"

# ============================================================
# 10. 创建 Tmux 会话脚本
# ============================================================
echo ""
echo "--- 10. Tmux 会话脚本示例 ---"

cat > "$TEMP_DIR/start_tmux_session.sh" << 'SCRIPT'
#!/bin/bash
#
# 创建预配置的Tmux会话
#

SESSION_NAME="${1:-dev}"

# 检查会话是否存在
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "会话 '$SESSION_NAME' 已存在，正在连接..."
    tmux attach -t "$SESSION_NAME"
    exit 0
fi

# 创建新会话
tmux new-session -d -s "$SESSION_NAME" -n "editor"

# 创建额外窗口
tmux new-window -t "$SESSION_NAME" -n "shell"
tmux new-window -t "$SESSION_NAME" -n "logs"

# 在第一个窗口创建分屏
tmux select-window -t "$SESSION_NAME:editor"
tmux split-window -h -t "$SESSION_NAME:editor"
tmux split-window -v -t "$SESSION_NAME:editor.1"

# 发送命令到各面板
tmux send-keys -t "$SESSION_NAME:editor.0" "echo '主编辑区'" Enter
tmux send-keys -t "$SESSION_NAME:editor.1" "echo '文件浏览'" Enter
tmux send-keys -t "$SESSION_NAME:editor.2" "echo '终端'" Enter

# 选择主面板
tmux select-pane -t "$SESSION_NAME:editor.0"

# 选择第一个窗口
tmux select-window -t "$SESSION_NAME:editor"

echo "会话 '$SESSION_NAME' 已创建，布局:"
echo "  窗口1 (editor): 三分屏"
echo "  窗口2 (shell): 命令行"
echo "  窗口3 (logs): 日志查看"
echo ""
echo "使用 'tmux attach -t $SESSION_NAME' 连接"
SCRIPT

chmod +x "$TEMP_DIR/start_tmux_session.sh"

echo "Tmux会话脚本已创建"
echo "脚本内容预览:"
head -25 "$TEMP_DIR/start_tmux_session.sh"

# ============================================================
# 11. 持久化任务运行检查
# ============================================================
echo ""
echo "--- 11. 持久化任务运行检查 ---"

check_persistence_methods() {
    echo "检查可用的持久化方法:"
    echo ""
    
    # nohup
    if command -v nohup &>/dev/null; then
        echo "  ✓ nohup - 可用"
    else
        echo "  ✗ nohup - 不可用"
    fi
    
    # screen
    if command -v screen &>/dev/null; then
        echo "  ✓ screen - 可用 ($(screen --version 2>&1 | head -1))"
    else
        echo "  ✗ screen - 不可用"
    fi
    
    # tmux
    if command -v tmux &>/dev/null; then
        echo "  ✓ tmux - 可用 ($(tmux -V))"
    else
        echo "  ✗ tmux - 不可用"
    fi
    
    # systemd
    if command -v systemctl &>/dev/null; then
        echo "  ✓ systemd - 可用 (用于用户服务)"
    else
        echo "  ✗ systemd - 不可用"
    fi
}

check_persistence_methods

# ============================================================
# 12. 最佳实践建议
# ============================================================
echo ""
echo "--- 12. 最佳实践建议 ---"

cat << 'EOF'
后台任务最佳实践:
=================

1. 简单任务使用 nohup:
   nohup ./script.sh > output.log 2>&1 &

2. 需要交互的任务使用 screen/tmux:
   screen -S mytask
   ./interactive_script.sh
   # Ctrl+A d 分离

3. 始终记录PID:
   ./script.sh &
   echo $! > /var/run/myscript.pid

4. 使用日志轮转:
   nohup ./script.sh 2>&1 | rotatelogs output.%Y%m%d.log 86400 &

5. 设置资源限制:
   ulimit -v 1000000  # 限制内存
   nice -n 10 ./script.sh  # 降低优先级

6. 监控任务状态:
   while true; do
       if ! kill -0 $PID 2>/dev/null; then
           echo "进程已退出，重启中..."
           ./script.sh &
           PID=$!
       fi
       sleep 60
   done

7. 使用正确的信号处理:
   trap 'cleanup; exit' SIGTERM SIGINT

EOF

echo ""
echo "=== nohup与终端复用器示例完成 ==="

