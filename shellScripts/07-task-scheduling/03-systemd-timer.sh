#!/bin/bash
#
# 脚本名称: 03-systemd-timer.sh
# 描述: systemd timer示例（用户级）：生成.service/.timer，默认dry-run，可选安装到~/.config/systemd/user
# 用法:
#   ./03-systemd-timer.sh
#   APPLY=1 ./03-systemd-timer.sh   # 尝试安装并执行 systemctl --user 操作
#

set -euo pipefail

echo "=== systemd timer（用户级）示例 ==="
echo ""

APPLY=${APPLY:-0}
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

unit_name="demo-task"
service_file="$TEMP_DIR/${unit_name}.service"
timer_file="$TEMP_DIR/${unit_name}.timer"
job_log="$SCRIPT_DIR/systemd_timer.log"

# ============================================================
# 1. 生成 unit 文件
# ============================================================
echo "--- 1. 生成 unit 文件 ---"

cat >"$service_file" << EOF
[Unit]
Description=Demo task (service) - append timestamp to log

[Service]
Type=oneshot
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/bin/bash -lc 'echo "[\$(date +\"%F %T\")] systemd timer ran on \$(hostname)" >> "${job_log}"'
EOF

cat >"$timer_file" << 'EOF'
[Unit]
Description=Demo task (timer) - run every minute

[Timer]
OnCalendar=*:0/1
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "service: $service_file"
echo "timer  : $timer_file"
echo "日志文件: $job_log"

# ============================================================
# 2. 安装与管理命令
# ============================================================
echo ""
echo "--- 2. 常用命令（user级） ---"

USER_UNIT_DIR="$HOME/.config/systemd/user"

cat << EOF
安装位置（用户级）：
  $USER_UNIT_DIR/

安装步骤：
  mkdir -p "$USER_UNIT_DIR"
  cp "$service_file" "$USER_UNIT_DIR/${unit_name}.service"
  cp "$timer_file"   "$USER_UNIT_DIR/${unit_name}.timer"

启用并立刻启动：
  systemctl --user daemon-reload
  systemctl --user enable --now ${unit_name}.timer

查看定时器：
  systemctl --user list-timers --all | grep ${unit_name}

查看服务日志（若journal可用）：
  journalctl --user -u ${unit_name}.service -n 50 --no-pager

停用与删除：
  systemctl --user disable --now ${unit_name}.timer
  rm -f "$USER_UNIT_DIR/${unit_name}.service" "$USER_UNIT_DIR/${unit_name}.timer"
  systemctl --user daemon-reload
EOF

# ============================================================
# 3. dry-run / 可选安装
# ============================================================
echo ""
echo "--- 3. 安装并尝试启用（可选） ---"

if [[ $APPLY -ne 1 ]]; then
    echo "默认不安装。若要尝试安装并执行 systemctl --user，请运行："
    echo "  APPLY=1 ./03-systemd-timer.sh"
    echo ""
    echo "提示：某些容器/无systemd user session环境下，systemctl --user 可能不可用。"
    exit 0
fi

if ! command -v systemctl >/dev/null 2>&1; then
    echo "未找到 systemctl，当前环境可能不使用systemd。" >&2
    exit 1
fi

mkdir -p "$USER_UNIT_DIR"
cp "$service_file" "$USER_UNIT_DIR/${unit_name}.service"
cp "$timer_file" "$USER_UNIT_DIR/${unit_name}.timer"

echo "已复制unit文件到: $USER_UNIT_DIR"

echo "尝试执行: systemctl --user daemon-reload"
set +e
systemctl --user daemon-reload
rc=$?
set -e

if [[ $rc -ne 0 ]]; then
    echo "systemctl --user 不可用（退出码=$rc）。unit文件已生成并复制，但未启用。" >&2
    echo "可在支持user session的环境中手动运行上述命令。" >&2
    exit 0
fi

systemctl --user enable --now "${unit_name}.timer"

echo "已启用并启动: ${unit_name}.timer"

echo ""
echo "当前定时器（过滤）："
systemctl --user list-timers --all | grep "${unit_name}" || true
