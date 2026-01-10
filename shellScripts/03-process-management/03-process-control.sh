#!/bin/bash
#
# 脚本名称: 03-process-control.sh
# 描述: 进程控制与信号处理示例
# 用法: ./03-process-control.sh
#

set -euo pipefail

echo "=== 进程控制与信号处理示例 ==="
echo ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# ============================================================
# 1. 进程信息查看
# ============================================================
echo "--- 1. 进程信息查看 ---"

echo ""
echo "当前脚本信息:"
echo "  PID: $$"
echo "  PPID: $PPID"
echo "  用户: $USER"
echo "  命令: $0"

echo ""
echo "使用 ps 查看进程:"
echo "  当前Shell的进程:"
ps -p $$ -o pid,ppid,user,cmd

# ============================================================
# 2. ps 命令详解
# ============================================================
echo ""
echo "--- 2. ps 命令详解 ---"

echo ""
echo "ps aux 输出说明:"
echo "  USER: 进程所有者"
echo "  PID:  进程ID"
echo "  %CPU: CPU使用率"
echo "  %MEM: 内存使用率"
echo "  VSZ:  虚拟内存大小"
echo "  RSS:  常驻内存大小"
echo "  TTY:  终端"
echo "  STAT: 进程状态"
echo "  START: 启动时间"
echo "  TIME: 累计CPU时间"
echo "  COMMAND: 命令"

echo ""
echo "进程状态代码:"
echo "  R: 运行"
echo "  S: 睡眠（可中断）"
echo "  D: 睡眠（不可中断）"
echo "  Z: 僵尸"
echo "  T: 停止"

echo ""
echo "按CPU排序的前5个进程:"
ps aux --sort=-%cpu | head -6

echo ""
echo "按内存排序的前5个进程:"
ps aux --sort=-%mem | head -6

# ============================================================
# 3. 进程查找
# ============================================================
echo ""
echo "--- 3. 进程查找 ---"

echo ""
echo "使用 pgrep 查找进程:"
echo "  bash 进程:"
pgrep -l bash | head -3

echo ""
echo "使用 pidof 获取PID:"
if command -v sshd &>/dev/null || pgrep sshd &>/dev/null; then
    echo "  sshd PID: $(pidof sshd 2>/dev/null || pgrep sshd | head -1 || echo '未运行')"
fi

echo ""
echo "当前用户的进程数: $(ps -u "$USER" --no-headers | wc -l)"

# ============================================================
# 4. 信号类型
# ============================================================
echo ""
echo "--- 4. 信号类型 ---"

echo ""
echo "常用信号列表:"
cat << 'EOF'
  编号  名称      说明
  ----  --------  --------------------------------
  1     SIGHUP    挂起（终端断开）
  2     SIGINT    中断（Ctrl+C）
  3     SIGQUIT   退出（Ctrl+\）
  9     SIGKILL   强制终止（不可捕获）
  15    SIGTERM   请求终止（默认）
  18    SIGCONT   继续执行
  19    SIGSTOP   暂停（不可捕获）
  20    SIGTSTP   终端停止（Ctrl+Z）
  10    SIGUSR1   用户自定义1
  12    SIGUSR2   用户自定义2
EOF

echo ""
echo "查看所有信号:"
echo "  (使用 'kill -l' 命令)"
kill -l | head -3
echo "  ..."

# ============================================================
# 5. kill 命令使用
# ============================================================
echo ""
echo "--- 5. kill 命令使用 ---"

# 启动测试进程
sleep 100 &
test_pid=$!

echo "启动测试进程 (PID: $test_pid)"
echo ""

echo "kill 命令格式:"
echo "  kill PID           发送SIGTERM（15）"
echo "  kill -9 PID        发送SIGKILL（强制）"
echo "  kill -TERM PID     使用信号名"
echo "  kill -0 PID        检查进程是否存在"

echo ""
echo "检查进程是否存在:"
if kill -0 $test_pid 2>/dev/null; then
    echo "  进程 $test_pid 正在运行"
else
    echo "  进程 $test_pid 不存在"
fi

echo ""
echo "终止测试进程:"
kill $test_pid
sleep 0.5
if ! kill -0 $test_pid 2>/dev/null; then
    echo "  进程 $test_pid 已终止"
fi

# ============================================================
# 6. killall 和 pkill
# ============================================================
echo ""
echo "--- 6. killall 和 pkill ---"

echo ""
echo "killall 命令:"
echo "  killall name       终止所有同名进程"
echo "  killall -9 name    强制终止"
echo "  killall -u user    终止用户的所有进程"

echo ""
echo "pkill 命令:"
echo "  pkill pattern      按模式终止"
echo "  pkill -f pattern   匹配完整命令行"
echo "  pkill -u user      按用户终止"
echo "  pkill -t tty       按终端终止"

# ============================================================
# 7. trap 信号捕获
# ============================================================
echo ""
echo "--- 7. trap 信号捕获 ---"

# 创建演示脚本
cat > "$TEMP_DIR/trap_demo.sh" << 'SCRIPT'
#!/bin/bash

# 清理函数
cleanup() {
    echo "执行清理..."
    rm -f /tmp/trap_demo.lock
    echo "清理完成"
}

# 信号处理函数
handle_sigint() {
    echo ""
    echo "收到 SIGINT (Ctrl+C)"
    cleanup
    exit 130
}

handle_sigterm() {
    echo ""
    echo "收到 SIGTERM"
    cleanup
    exit 143
}

# 设置trap
trap handle_sigint SIGINT
trap handle_sigterm SIGTERM
trap cleanup EXIT

# 创建锁文件
touch /tmp/trap_demo.lock
echo "锁文件已创建: /tmp/trap_demo.lock"

echo "程序运行中 (PID: $$)"
echo "按 Ctrl+C 或发送 kill 信号测试..."

# 主循环
count=0
while true; do
    ((count++))
    echo "运行中... ($count)"
    sleep 1
done
SCRIPT

chmod +x "$TEMP_DIR/trap_demo.sh"

echo "trap演示脚本已创建"
echo ""
echo "脚本内容:"
echo "----------------------------------------"
cat "$TEMP_DIR/trap_demo.sh"
echo "----------------------------------------"
echo ""
echo "测试方法:"
echo "  1. 运行: $TEMP_DIR/trap_demo.sh"
echo "  2. 按 Ctrl+C 或在另一终端执行 kill PID"

# ============================================================
# 8. 实用的trap模式
# ============================================================
echo ""
echo "--- 8. 实用的trap模式 ---"

echo ""
echo "模式1: 临时文件清理"
cat << 'EOF'
  TEMP_FILE=$(mktemp)
  trap 'rm -f "$TEMP_FILE"' EXIT
EOF

echo ""
echo "模式2: 错误处理"
cat << 'EOF'
  trap 'echo "Error at line $LINENO"; exit 1' ERR
EOF

echo ""
echo "模式3: 忽略信号"
cat << 'EOF'
  trap '' SIGINT  # 忽略Ctrl+C
EOF

echo ""
echo "模式4: 恢复默认处理"
cat << 'EOF'
  trap - SIGINT   # 恢复SIGINT默认行为
EOF

echo ""
echo "模式5: 多信号处理"
cat << 'EOF'
  cleanup() { echo "Cleaning up..."; }
  trap cleanup SIGINT SIGTERM SIGHUP EXIT
EOF

# ============================================================
# 9. 进程优先级
# ============================================================
echo ""
echo "--- 9. 进程优先级 ---"

echo ""
echo "nice 值范围: -20（最高优先级）到 19（最低优先级）"
echo "默认 nice 值: 0"

echo ""
echo "启动低优先级任务:"
echo "  nice -n 10 ./task.sh"

echo ""
echo "启动高优先级任务（需要root）:"
echo "  sudo nice -n -10 ./task.sh"

echo ""
echo "修改运行中进程的优先级:"
echo "  renice -n 5 -p PID"

echo ""
echo "当前Shell的nice值: $(nice)"

# ============================================================
# 10. 进程资源限制
# ============================================================
echo ""
echo "--- 10. 进程资源限制 ---"

echo ""
echo "ulimit 当前限制:"
echo "  最大打开文件数: $(ulimit -n)"
echo "  最大进程数: $(ulimit -u)"
echo "  栈大小: $(ulimit -s)"
echo "  最大虚拟内存: $(ulimit -v)"

echo ""
echo "常用 ulimit 设置:"
echo "  ulimit -n 65535    # 增加文件描述符限制"
echo "  ulimit -v 1000000  # 限制虚拟内存(KB)"
echo "  ulimit -t 60       # 限制CPU时间(秒)"

# ============================================================
# 11. timeout 命令
# ============================================================
echo ""
echo "--- 11. timeout 命令 ---"

echo ""
echo "使用 timeout 限制命令执行时间:"

echo ""
echo "示例1: 2秒超时（任务1秒完成）"
if timeout 2 sleep 1; then
    echo "  任务在超时前完成"
fi

echo ""
echo "示例2: 1秒超时（任务需要3秒）"
if timeout 1 sleep 3; then
    echo "  任务完成"
else
    echo "  任务超时 (退出码: $?)"
fi

echo ""
echo "timeout 选项:"
echo "  timeout -s KILL 5 cmd  # 使用SIGKILL"
echo "  timeout -k 10 5 cmd    # 5秒后SIGTERM，再10秒后SIGKILL"

# ============================================================
# 12. 进程监控脚本
# ============================================================
echo ""
echo "--- 12. 进程监控脚本 ---"

# 创建监控脚本
cat > "$TEMP_DIR/process_monitor.sh" << 'SCRIPT'
#!/bin/bash
#
# 进程监控脚本
#

monitor_process() {
    local name="$1"
    local check_interval="${2:-5}"
    
    echo "监控进程: $name"
    echo "检查间隔: ${check_interval}秒"
    echo "按 Ctrl+C 停止监控"
    echo ""
    
    while true; do
        local count=$(pgrep -c "$name" 2>/dev/null || echo 0)
        local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        
        if [[ $count -gt 0 ]]; then
            echo "[$timestamp] $name: 运行中 ($count 个实例)"
            pgrep -a "$name" | head -3 | while read pid cmd; do
                local cpu=$(ps -p $pid -o %cpu= 2>/dev/null || echo "N/A")
                local mem=$(ps -p $pid -o %mem= 2>/dev/null || echo "N/A")
                echo "  PID $pid: CPU=${cpu}% MEM=${mem}%"
            done
        else
            echo "[$timestamp] $name: 未运行"
        fi
        
        sleep "$check_interval"
    done
}

# 用法检查
if [[ $# -lt 1 ]]; then
    echo "用法: $0 <进程名> [检查间隔秒数]"
    echo "示例: $0 nginx 10"
    exit 1
fi

monitor_process "$@"
SCRIPT

chmod +x "$TEMP_DIR/process_monitor.sh"

echo "进程监控脚本已创建: $TEMP_DIR/process_monitor.sh"
echo ""
echo "用法: $TEMP_DIR/process_monitor.sh <进程名> [间隔秒数]"
echo "示例: $TEMP_DIR/process_monitor.sh bash 5"

# ============================================================
# 13. 自动重启脚本
# ============================================================
echo ""
echo "--- 13. 自动重启脚本 ---"

cat > "$TEMP_DIR/auto_restart.sh" << 'SCRIPT'
#!/bin/bash
#
# 自动重启脚本
#

COMMAND="$1"
MAX_RESTARTS="${2:-5}"
RESTART_DELAY="${3:-3}"

restart_count=0

# 信号处理
cleanup() {
    echo ""
    echo "收到终止信号，停止监控..."
    if [[ -n "${child_pid:-}" ]] && kill -0 "$child_pid" 2>/dev/null; then
        kill "$child_pid"
    fi
    exit 0
}
trap cleanup SIGINT SIGTERM

echo "自动重启守护进程"
echo "命令: $COMMAND"
echo "最大重启次数: $MAX_RESTARTS"
echo "重启延迟: ${RESTART_DELAY}秒"
echo ""

while true; do
    echo "[$(date '+%H:%M:%S')] 启动进程..."
    
    # 运行命令
    eval "$COMMAND" &
    child_pid=$!
    
    # 等待进程结束
    wait $child_pid
    exit_code=$?
    
    echo "[$(date '+%H:%M:%S')] 进程退出 (退出码: $exit_code)"
    
    ((restart_count++))
    
    if [[ $restart_count -ge $MAX_RESTARTS ]]; then
        echo "已达到最大重启次数 ($MAX_RESTARTS)，停止监控"
        exit 1
    fi
    
    echo "等待 ${RESTART_DELAY} 秒后重启... (第 $restart_count/$MAX_RESTARTS 次)"
    sleep "$RESTART_DELAY"
done
SCRIPT

chmod +x "$TEMP_DIR/auto_restart.sh"

echo "自动重启脚本已创建: $TEMP_DIR/auto_restart.sh"
echo ""
echo "用法: $TEMP_DIR/auto_restart.sh <命令> [最大重启次数] [重启延迟秒数]"
echo "示例: $TEMP_DIR/auto_restart.sh './myserver.sh' 5 10"

# ============================================================
# 14. 健康检查脚本
# ============================================================
echo ""
echo "--- 14. 健康检查脚本 ---"

cat > "$TEMP_DIR/health_check.sh" << 'SCRIPT'
#!/bin/bash
#
# 进程健康检查脚本
#

check_process() {
    local name="$1"
    if pgrep -x "$name" > /dev/null; then
        return 0
    fi
    return 1
}

check_port() {
    local port="$1"
    if command -v ss &>/dev/null; then
        ss -tuln | grep -q ":$port "
    elif command -v netstat &>/dev/null; then
        netstat -tuln | grep -q ":$port "
    else
        return 1
    fi
}

check_url() {
    local url="$1"
    local timeout="${2:-5}"
    if command -v curl &>/dev/null; then
        curl -sf --max-time "$timeout" "$url" > /dev/null
    elif command -v wget &>/dev/null; then
        wget -q --timeout="$timeout" -O /dev/null "$url"
    else
        return 1
    fi
}

# 运行检查
echo "系统健康检查"
echo "============="
echo ""

# 检查关键进程
echo "进程检查:"
for proc in sshd cron systemd; do
    if check_process "$proc"; then
        echo "  ✓ $proc 运行中"
    else
        echo "  ✗ $proc 未运行"
    fi
done

echo ""
echo "端口检查:"
for port in 22 80 443; do
    if check_port "$port"; then
        echo "  ✓ 端口 $port 开放"
    else
        echo "  - 端口 $port 未开放"
    fi
done

echo ""
echo "资源检查:"
# 磁盘使用
disk_usage=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [[ $disk_usage -lt 80 ]]; then
    echo "  ✓ 磁盘使用: ${disk_usage}%"
else
    echo "  ⚠ 磁盘使用: ${disk_usage}% (警告: 超过80%)"
fi

# 内存使用
if command -v free &>/dev/null; then
    mem_usage=$(free | awk '/Mem:/ {printf "%.0f", $3/$2*100}')
    if [[ $mem_usage -lt 80 ]]; then
        echo "  ✓ 内存使用: ${mem_usage}%"
    else
        echo "  ⚠ 内存使用: ${mem_usage}% (警告: 超过80%)"
    fi
fi

# 负载
load=$(cat /proc/loadavg | awk '{print $1}')
cores=$(nproc)
echo "  ✓ 系统负载: $load (CPU核心: $cores)"
SCRIPT

chmod +x "$TEMP_DIR/health_check.sh"

echo "健康检查脚本已创建并运行:"
echo ""
"$TEMP_DIR/health_check.sh"

# ============================================================
# 15. 总结
# ============================================================
echo ""
echo "--- 15. 命令速查表 ---"

cat << 'EOF'
进程控制命令速查:
=================

查看进程:
  ps aux              所有进程
  ps -ef              所有进程（另一格式）
  ps aux --sort=-%cpu 按CPU排序
  top / htop          实时监控
  pgrep name          按名称查找

终止进程:
  kill PID            发送SIGTERM
  kill -9 PID         强制终止
  killall name        终止同名进程
  pkill pattern       按模式终止

信号处理:
  trap 'cmd' SIGNAL   捕获信号
  trap '' SIGNAL      忽略信号
  trap - SIGNAL       恢复默认

资源控制:
  nice -n N cmd       设置优先级
  renice -n N -p PID  修改优先级
  timeout N cmd       超时控制
  ulimit -n N         设置限制

EOF

echo ""
echo "=== 进程控制与信号处理示例完成 ==="

