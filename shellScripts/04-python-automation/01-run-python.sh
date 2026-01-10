#!/bin/bash
#
# 脚本名称: 01-run-python.sh
# 描述: 运行Python脚本的常见方式：解释器选择、参数/环境变量传递、退出码与日志
# 用法: ./01-run-python.sh
#

set -euo pipefail

echo "=== 运行Python脚本示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PY_SCRIPT="$SCRIPT_DIR/sample.py"

# ============================================================
# 1. 检查Python解释器
# ============================================================
echo "--- 1. 检查Python解释器 ---"

# 允许用户通过环境变量覆盖解释器
PYTHON_BIN=${PYTHON_BIN:-""}

if [[ -z "$PYTHON_BIN" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_BIN="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_BIN="python"
    else
        echo "未找到Python解释器（python3/python）" >&2
        echo "请安装Python，或设置环境变量 PYTHON_BIN 指向解释器路径" >&2
        exit 1
    fi
fi

echo "使用解释器: $PYTHON_BIN"
"$PYTHON_BIN" -V

echo ""
echo "示例程序: $PY_SCRIPT"

# ============================================================
# 2. 传递命令行参数
# ============================================================
echo ""
echo "--- 2. 传递命令行参数 ---"

"$PYTHON_BIN" "$PY_SCRIPT" --name "Alice" --seed 1
"$PYTHON_BIN" "$PY_SCRIPT" --name "Bob" --seed 2 --sleep 0.1

# ============================================================
# 3. 传递环境变量
# ============================================================
echo ""
echo "--- 3. 传递环境变量 ---"

APP_MODE="prod" APP_RUN_ID="run-001" "$PYTHON_BIN" "$PY_SCRIPT" --name "Charlie" --seed 3

# ============================================================
# 4. 获取退出码（成功/失败）
# ============================================================
echo ""
echo "--- 4. 获取退出码（成功/失败） ---"

set +e
"$PYTHON_BIN" "$PY_SCRIPT" --fail
rc=$?
set -e

echo "失败示例退出码: $rc"

# ============================================================
# 5. 日志重定向（stdout/stderr）
# ============================================================
echo ""
echo "--- 5. 日志重定向（stdout/stderr） ---"

LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

stdout_log="$LOG_DIR/sample_stdout.log"
stderr_log="$LOG_DIR/sample_stderr.log"
combined_log="$LOG_DIR/sample_combined.log"

# 分开保存 stdout/stderr
"$PYTHON_BIN" "$PY_SCRIPT" --name "LogDemo" --seed 10 >"$stdout_log" 2>"$stderr_log"

# 合并保存（追加模式）
"$PYTHON_BIN" "$PY_SCRIPT" --name "Combined" --seed 11 >>"$combined_log" 2>&1

# 失败输出也会写入 combined
set +e
"$PYTHON_BIN" "$PY_SCRIPT" --fail >>"$combined_log" 2>&1
set -e

echo "stdout日志: $stdout_log"
echo "stderr日志: $stderr_log"
echo "合并日志:  $combined_log"

echo ""
echo "完成。"
