#!/bin/bash
#
# 脚本名称: 03-batch-cpp.sh
# 描述: 批量编译与执行：扫描编译选项（-O0/-O2/-O3）、归档日志、CSV汇总
# 用法: ./03-batch-cpp.sh
#

set -euo pipefail

echo "=== 批量编译与执行C++示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CPP_SRC="$SCRIPT_DIR/sample.cpp"

# ============================================================
# 1. 选择编译器
# ============================================================
echo "--- 1. 选择编译器 ---"

CXX=${CXX:-""}
if [[ -z "$CXX" ]]; then
    if command -v g++ >/dev/null 2>&1; then
        CXX="g++"
    elif command -v clang++ >/dev/null 2>&1; then
        CXX="clang++"
    else
        echo "未找到C++编译器（g++/clang++）" >&2
        exit 1
    fi
fi

echo "使用编译器: $CXX"

# ============================================================
# 2. 准备输出目录
# ============================================================
echo ""
echo "--- 2. 准备输出目录 ---"

run_ts=$(date +"%Y%m%d-%H%M%S")
OUT_DIR="$SCRIPT_DIR/results/$run_ts"
LOG_DIR="$OUT_DIR/logs"
BIN_DIR="$OUT_DIR/bin"
mkdir -p "$LOG_DIR" "$BIN_DIR"

RESULT_CSV="$OUT_DIR/results.csv"
echo "opt,seed,exit_code,metric,bin,stdout_log,stderr_log" >"$RESULT_CSV"

echo "输出目录: $OUT_DIR"
echo "结果文件: $RESULT_CSV"

# ============================================================
# 3. 扫描编译配置与运行参数
# ============================================================
echo ""
echo "--- 3. 扫描编译配置与运行参数 ---"

opts=(O0 O2 O3)
seeds=(1 2 3)

success_count=0
fail_count=0

for opt in "${opts[@]}"; do
    cxxflags="-std=c++17 -${opt} -Wall -Wextra"
    bin="$BIN_DIR/app_${opt}"

    echo "编译配置: -${opt}"
    echo "  命令: $CXX $cxxflags -o $bin $CPP_SRC"
    "$CXX" $cxxflags -o "$bin" "$CPP_SRC"

    for seed in "${seeds[@]}"; do
        run_id="${opt}_seed-${seed}"
        stdout_log="$LOG_DIR/${run_id}.out.log"
        stderr_log="$LOG_DIR/${run_id}.err.log"

        echo "  运行: $run_id"

        set +e
        "$bin" --name "Batch" --seed "$seed" >"$stdout_log" 2>"$stderr_log"
        rc=$?
        set -e

        metric=$(awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^metric=/){sub(/^metric=/,"",$i); print $i; exit}}}' "$stdout_log" 2>/dev/null || true)
        metric=${metric:-""}

        echo "$opt,$seed,$rc,$metric,$bin,$stdout_log,$stderr_log" >>"$RESULT_CSV"

        if [[ $rc -eq 0 ]]; then
            success_count=$((success_count + 1))
        else
            fail_count=$((fail_count + 1))
        fi
    done

done

# ============================================================
# 4. 汇总
# ============================================================
echo ""
echo "--- 4. 汇总 ---"

echo "成功次数: $success_count"
echo "失败次数: $fail_count"
echo "CSV结果: $RESULT_CSV"

echo ""
echo "查看结果示例:"
echo "  column -s, -t < $RESULT_CSV | head"
