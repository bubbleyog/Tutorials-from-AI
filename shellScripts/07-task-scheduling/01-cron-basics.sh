#!/bin/bash
#
# 脚本名称: 01-cron-basics.sh
# 描述: cron基础：生成示例任务脚本与crontab片段（默认dry-run，可选安装）
# 用法:
#   ./01-cron-basics.sh
#   APPLY=1 ./01-cron-basics.sh   # 尝试把示例任务加入当前用户crontab
#

set -euo pipefail

echo "=== cron 基础示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

APPLY=${APPLY:-0}

# ============================================================
# 1. 生成示例任务脚本
# ============================================================
echo "--- 1. 生成示例任务脚本 ---"

job_script="$TEMP_DIR/cron_job.sh"
job_log="$SCRIPT_DIR/cron_job.log"

cat >"$job_script" << EOF
#!/bin/bash
set -euo pipefail

# cron环境通常没有你交互式shell的PATH与工作目录
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

echo "[\$(date +\"%F %T\")] cron job running on \$(hostname)" >> "$job_log"
EOF

chmod +x "$job_script"

echo "已生成任务脚本: $job_script"
echo "日志文件将写入: $job_log"

# ============================================================
# 2. 生成crontab片段
# ============================================================
echo ""
echo "--- 2. 生成crontab片段 ---"

# 每分钟运行一次（演示用）
cron_line="* * * * * $job_script"

cat << EOF
建议的crontab内容（演示：每分钟运行一次）:
  $cron_line

常见建议：
  - 使用绝对路径
  - 显式设置 PATH/SHELL
  - 把stdout/stderr重定向到日志文件（或让任务脚本自己写日志）
EOF

# ============================================================
# 3. dry-run / 可选安装
# ============================================================
echo ""
echo "--- 3. 安装到当前用户crontab（可选） ---"

if [[ $APPLY -ne 1 ]]; then
    echo "默认不修改系统。若要尝试安装到当前用户crontab，请运行："
    echo "  APPLY=1 ./01-cron-basics.sh"
    echo ""
    echo "手动安装示例（推荐先检查crontab再安装）："
    echo "  crontab -l"
    echo "  (crontab -l 2>/dev/null; echo \"$cron_line\") | crontab -"
    echo "  crontab -l"
    exit 0
fi

if ! command -v crontab >/dev/null 2>&1; then
    echo "未找到 crontab 命令，可能未安装cron组件（cronie/cron）。" >&2
    echo "本脚本将不执行安装。" >&2
    exit 1
fi

# 避免重复添加
current=$(crontab -l 2>/dev/null || true)
if echo "$current" | grep -Fq "$cron_line"; then
    echo "crontab已包含该任务，跳过添加。"
else
    echo "将任务追加到当前用户crontab..."
    (crontab -l 2>/dev/null; echo "$cron_line") | crontab -
    echo "已添加。"
fi

echo ""
echo "查看当前用户crontab："
crontab -l

echo ""
echo "提示：删除该任务可手动编辑 crontab -e，或用grep过滤重写。"
