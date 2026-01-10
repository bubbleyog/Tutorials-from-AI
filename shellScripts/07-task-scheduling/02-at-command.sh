#!/bin/bash
#
# 脚本名称: 02-at-command.sh
# 描述: at一次性任务示例：生成任务内容并展示提交/查看/取消方法（默认dry-run）
# 用法:
#   ./02-at-command.sh
#   RUN=1 ./02-at-command.sh      # 尝试实际提交一次性任务（可能需要atd运行/权限）
#

set -euo pipefail

echo "=== at 一次性任务示例 ==="
echo ""

RUN=${RUN:-0}
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

job_script="$TEMP_DIR/at_job.sh"
job_log="$SCRIPT_DIR/at_job.log"

# ============================================================
# 1. 生成一次性任务脚本
# ============================================================
echo "--- 1. 生成一次性任务脚本 ---"

cat >"$job_script" << EOF
#!/bin/bash
set -euo pipefail

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

echo "[\$(date +\"%F %T\")] at job ran on \$(hostname)" >> "$job_log"
EOF

chmod +x "$job_script"

echo "任务脚本: $job_script"
echo "日志文件: $job_log"

# ============================================================
# 2. 提交/查看/取消命令
# ============================================================
echo ""
echo "--- 2. 常用命令 ---"

cat << EOF
提交任务示例（1分钟后执行）：
  echo "$job_script" | at now + 1 minute

查看队列：
  atq

取消任务：
  atrm <job_id>

查看任务内容：
  at -c <job_id>
EOF

# ============================================================
# 3. dry-run / 可选执行
# ============================================================
echo ""
echo "--- 3. 提交任务（可选） ---"

if [[ $RUN -ne 1 ]]; then
    echo "默认不提交任务。若要尝试实际提交，请运行："
    echo "  RUN=1 ./02-at-command.sh"
    exit 0
fi

if ! command -v at >/dev/null 2>&1; then
    echo "未找到 at 命令，可能未安装 at（以及atd服务）。" >&2
    echo "本脚本将不提交任务。" >&2
    exit 1
fi

# 提交任务
# 说明：某些系统需要atd运行；某些环境（容器）可能禁止
set +e
job_output=$(echo "$job_script" | at now + 1 minute 2>&1)
rc=$?
set -e

if [[ $rc -ne 0 ]]; then
    echo "提交失败（退出码=$rc）：" >&2
    echo "$job_output" >&2
    echo "提示：确认已安装at并且atd在运行。" >&2
    exit $rc
fi

echo "提交成功："
echo "$job_output"

echo ""
echo "当前队列："
(atq || true)
