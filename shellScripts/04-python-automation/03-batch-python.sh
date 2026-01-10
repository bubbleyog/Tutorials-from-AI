#!/bin/bash
#
# 脚本名称: 03-batch-python.sh
# 描述: 批量执行Python程序：参数扫描、日志归档、CSV结果汇总
# 用法: ./03-batch-python.sh
#

set -euo pipefail

echo "=== 批量执行Python示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PY_SCRIPT="$SCRIPT_DIR/sample.py"

if ! command -v python3 >/dev/null 2>&1; then
    echo "未找到 python3，请先安装Python3" >&2
    exit 1
fi

# ============================================================
# 1. 准备输出目录
# ============================================================
echo "--- 1. 准备输出目录 ---"

run_ts=$(date +"%Y%m%d-%H%M%S")
OUT_DIR="$SCRIPT_DIR/results/$run_ts"
LOG_DIR="$OUT_DIR/logs"
mkdir -p "$LOG_DIR"

RESULT_CSV="$OUT_DIR/results.csv"

# 写CSV表头
echo "run_id,seed,exit_code,metric,stdout_log,stderr_log" >"$RESULT_CSV"

echo "输出目录: $OUT_DIR"
echo "结果文件: $RESULT_CSV"

# ============================================================
# 2. 批量参数扫描
# ============================================================
echo ""
echo "--- 2. 批量参数扫描 ---"

seeds=(1 2 3 4 5)

success_count=0
fail_count=0

for seed in "${seeds[@]}"; do
    run_id="seed-${seed}"
    stdout_log="$LOG_DIR/${run_id}.out.log"
    stderr_log="$LOG_DIR/${run_id}.err.log"

    echo "运行: $run_id"

    # 给每次运行写入不同的环境变量
    set +e
    APP_MODE="batch" APP_RUN_ID="$run_id" python3 "$PY_SCRIPT" --name "Batch" --seed "$seed" >"$stdout_log" 2>"$stderr_log"
    rc=$?
    set -e

    # 从stdout中提取 metric（输出形如 metric=0.123456）
    metric=$(awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^metric=/){sub(/^metric=/,"",$i); print $i; exit}}}' "$stdout_log" 2>/dev/null || true)
    metric=${metric:-""}

    echo "$run_id,$seed,$rc,$metric,$stdout_log,$stderr_log" >>"$RESULT_CSV"

    if [[ $rc -eq 0 ]]; then
        success_count=$((success_count + 1))
    else
        fail_count=$((fail_count + 1))
    fi

done

# ============================================================
# 3. 汇总
# ============================================================
echo ""
echo "--- 3. 汇总 ---"

echo "成功次数: $success_count"
echo "失败次数: $fail_count"
echo "CSV结果: $RESULT_CSV"

echo ""
echo "查看结果示例:"
echo "  column -s, -t < $RESULT_CSV | head"
