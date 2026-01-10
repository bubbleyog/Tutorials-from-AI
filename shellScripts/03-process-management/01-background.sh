#!/bin/bash
#
# 脚本名称: 01-background.sh
# 描述: 前后台作业管理示例
# 用法: ./01-background.sh
#

set -euo pipefail

echo "=== 前后台作业管理示例 ==="
echo ""

# ============================================================
# 1. 启动后台任务
# ============================================================
echo "--- 1. 启动后台任务 ---"

echo "启动3个后台任务..."

# 启动后台任务
sleep 30 &
pid1=$!
echo "任务1 已启动 (PID: $pid1)"

sleep 40 &
pid2=$!
echo "任务2 已启动 (PID: $pid2)"

sleep 50 &
pid3=$!
echo "任务3 已启动 (PID: $pid3)"

echo ""
echo "当前后台作业列表:"
jobs -l

# ============================================================
# 2. 检查后台任务状态
# ============================================================
echo ""
echo "--- 2. 检查后台任务状态 ---"

# 检查进程是否运行
check_process() {
    local pid=$1
    if kill -0 "$pid" 2>/dev/null; then
        echo "进程 $pid: 运行中"
    else
        echo "进程 $pid: 已结束"
    fi
}

check_process $pid1
check_process $pid2
check_process $pid3

# ============================================================
# 3. 等待特定任务完成
# ============================================================
echo ""
echo "--- 3. 等待任务完成 ---"

# 启动一个快速完成的任务
sleep 2 &
quick_pid=$!
echo "启动快速任务 (PID: $quick_pid)"

echo "等待快速任务完成..."
wait $quick_pid
echo "快速任务已完成，退出状态: $?"

# ============================================================
# 4. 终止后台任务
# ============================================================
echo ""
echo "--- 4. 终止后台任务 ---"

echo "终止之前启动的任务..."

# 安全终止（发送SIGTERM）
for pid in $pid1 $pid2 $pid3; do
    if kill -0 "$pid" 2>/dev/null; then
        kill "$pid"
        echo "已终止进程 $pid"
    fi
done

# 等待所有后台作业结束
wait 2>/dev/null || true

echo "所有后台任务已终止"

# ============================================================
# 5. 并行任务与等待
# ============================================================
echo ""
echo "--- 5. 并行任务与等待 ---"

# 模拟并行处理多个任务
process_item() {
    local item=$1
    local duration=$((RANDOM % 3 + 1))
    echo "  开始处理: $item (耗时 ${duration}秒)"
    sleep $duration
    echo "  完成处理: $item"
}

echo "并行处理4个任务..."
items=("数据A" "数据B" "数据C" "数据D")

for item in "${items[@]}"; do
    process_item "$item" &
done

echo "等待所有任务完成..."
wait
echo "所有任务已完成!"

# ============================================================
# 6. 收集后台任务的输出
# ============================================================
echo ""
echo "--- 6. 收集后台任务输出 ---"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# 启动多个任务，输出到临时文件
for i in {1..3}; do
    (
        sleep $((RANDOM % 2))
        echo "任务$i的结果: 成功"
    ) > "$TEMP_DIR/result_$i.txt" &
done

wait

echo "收集结果:"
for f in "$TEMP_DIR"/result_*.txt; do
    cat "$f"
done

# ============================================================
# 7. 限制并行任务数量
# ============================================================
echo ""
echo "--- 7. 限制并行任务数量 ---"

MAX_JOBS=2
current_jobs=0

limited_parallel() {
    local total=6
    
    for i in $(seq 1 $total); do
        # 等待直到有空位
        while (( $(jobs -r | wc -l) >= MAX_JOBS )); do
            sleep 0.1
        done
        
        # 启动新任务
        (
            echo "  任务 $i 开始"
            sleep 1
            echo "  任务 $i 完成"
        ) &
    done
    
    wait
}

echo "最多同时运行 $MAX_JOBS 个任务:"
limited_parallel

# ============================================================
# 8. 后台任务超时控制
# ============================================================
echo ""
echo "--- 8. 后台任务超时控制 ---"

run_with_timeout() {
    local timeout=$1
    local cmd=$2
    
    # 启动命令
    eval "$cmd" &
    local pid=$!
    
    # 启动超时监控
    (
        sleep "$timeout"
        if kill -0 $pid 2>/dev/null; then
            echo "  任务超时，正在终止..."
            kill $pid 2>/dev/null
        fi
    ) &
    local timeout_pid=$!
    
    # 等待命令完成
    if wait $pid 2>/dev/null; then
        # 命令正常完成，终止超时监控
        kill $timeout_pid 2>/dev/null || true
        wait $timeout_pid 2>/dev/null || true
        return 0
    else
        wait $timeout_pid 2>/dev/null || true
        return 1
    fi
}

echo "运行一个2秒超时的任务（任务需要1秒）:"
if run_with_timeout 2 "sleep 1 && echo '  任务完成'"; then
    echo "  结果: 成功"
else
    echo "  结果: 超时或失败"
fi

echo ""
echo "运行一个1秒超时的任务（任务需要3秒）:"
if run_with_timeout 1 "sleep 3 && echo '  任务完成'"; then
    echo "  结果: 成功"
else
    echo "  结果: 超时或失败"
fi

# ============================================================
# 9. 作业状态查询函数
# ============================================================
echo ""
echo "--- 9. 作业状态查询 ---"

# 启动几个测试任务
sleep 10 &
test_pid1=$!
sleep 15 &
test_pid2=$!

show_job_status() {
    echo "当前后台作业:"
    echo "-------------------"
    
    local job_count=$(jobs | wc -l)
    if [[ $job_count -eq 0 ]]; then
        echo "  (无后台作业)"
    else
        jobs -l | while read line; do
            echo "  $line"
        done
    fi
    
    echo "-------------------"
    echo "运行中: $(jobs -r | wc -l) 个"
    echo "已停止: $(jobs -s | wc -l) 个"
}

show_job_status

# 清理
kill $test_pid1 $test_pid2 2>/dev/null || true
wait 2>/dev/null || true

# ============================================================
# 10. 实用示例：批量处理文件
# ============================================================
echo ""
echo "--- 10. 实用示例：批量处理文件 ---"

# 创建测试文件
for i in {1..5}; do
    echo "文件$i的内容" > "$TEMP_DIR/file_$i.txt"
done

process_file() {
    local file=$1
    local basename=$(basename "$file")
    echo "  处理: $basename"
    sleep 0.5
    # 模拟处理（转换为大写）
    tr 'a-z' 'A-Z' < "$file" > "${file}.processed"
}

echo "并行处理文件..."
for file in "$TEMP_DIR"/file_*.txt; do
    process_file "$file" &
done
wait

echo "处理完成，结果:"
for file in "$TEMP_DIR"/*.processed; do
    echo "  $(basename "$file"): $(cat "$file")"
done

# ============================================================
# 11. 使用命名管道进行进程间通信
# ============================================================
echo ""
echo "--- 11. 进程间通信示例 ---"

# 创建命名管道
fifo="$TEMP_DIR/myfifo"
mkfifo "$fifo"

# 生产者进程
(
    for i in {1..3}; do
        echo "消息 $i" > "$fifo"
        sleep 0.5
    done
) &
producer_pid=$!

# 消费者进程
(
    while read -r line; do
        echo "  收到: $line"
    done < "$fifo"
) &
consumer_pid=$!

# 等待生产者完成
wait $producer_pid

# 关闭管道
exec 3>"$fifo"  # 打开写端
exec 3>&-       # 关闭写端，这会让消费者的read结束

wait $consumer_pid 2>/dev/null || true

echo "进程间通信完成"

echo ""
echo "=== 前后台作业管理示例完成 ==="

