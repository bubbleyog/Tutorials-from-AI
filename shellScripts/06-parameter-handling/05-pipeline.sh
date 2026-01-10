#!/bin/bash
#
# 脚本名称: 05-pipeline.sh
# 描述: 程序管道对接示例：stdin/stdout管道、进程替换、Here Document
# 用法: ./05-pipeline.sh
#

set -euo pipefail

echo "=== 程序管道对接示例 ==="
echo ""

# ============================================================
# 1. 基本管道：producer | consumer
# ============================================================
echo "--- 1. 基本管道：producer | consumer ---"

# 生成一些数据（包含空格/重复项）
cat << 'EOF' | tr 'A-Z' 'a-z' | sort | uniq -c
Apple
banana
apple
Cherry
banana
EOF

echo ""

# ============================================================
# 2. Here Document：向程序提供多行输入
# ============================================================
echo "--- 2. Here Document：多行输入 ---"

# - 使用单引号EOF可禁止变量扩展，更安全
awk '{print NR ":" $0}' << 'EOF'
line one
line two
line three
EOF

echo ""

# ============================================================
# 3. 进程替换：把命令输出当成文件
# ============================================================
echo "--- 3. 进程替换：diff <(cmd1) <(cmd2) ---"

# 比较两种排序结果
if command -v diff >/dev/null 2>&1; then
    diff -u <(printf "%s\n" 3 2 1 | sort -n) <(printf "%s\n" 1 2 3 | sort -n) || true
else
    echo "未找到 diff，跳过进程替换diff演示"
fi

echo ""

# ============================================================
# 4. 对接外部程序（示例：对接第4章Python程序）
# ============================================================
echo "--- 4. 对接外部程序（示例：对接Python） ---"

PY_PROG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../04-python-automation"
PY_SCRIPT="$PY_PROG_DIR/sample.py"

if command -v python3 >/dev/null 2>&1 && [[ -f "$PY_SCRIPT" ]]; then
    # 用管道生成seed列表 -> 逐个运行Python -> 提取metric
    # 这里演示“脚本输出 -> awk提取 -> 汇总”
    echo "seed,metric" 
    printf "%s\n" 1 2 3 | while IFS= read -r seed; do
        out=$(APP_MODE="pipe" APP_RUN_ID="seed-$seed" python3 "$PY_SCRIPT" --name "Pipe" --seed "$seed")
        metric=$(echo "$out" | awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^metric=/){sub(/^metric=/,"",$i); print $i; exit}}}')
        echo "$seed,$metric"
    done
else
    echo "未找到 python3 或 $PY_SCRIPT，跳过对接Python演示"
fi

echo ""
echo "完成。"
