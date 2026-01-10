#!/bin/bash
#
# 脚本名称: 04-loops.sh
# 描述: Shell循环结构示例
# 用法: ./04-loops.sh
#

set -euo pipefail

echo "=== Shell循环结构示例 ==="
echo ""

# ============================================================
# 1. for循环 - 遍历列表
# ============================================================
echo "--- 1. for循环 - 遍历列表 ---"

echo "遍历水果列表:"
for fruit in apple banana cherry; do
    echo "  水果: $fruit"
done

# ============================================================
# 2. for循环 - 遍历数组
# ============================================================
echo ""
echo "--- 2. for循环 - 遍历数组 ---"

colors=("红色" "绿色" "蓝色" "黄色")

echo "遍历颜色数组:"
for color in "${colors[@]}"; do
    echo "  颜色: $color"
done

# 带索引遍历
echo ""
echo "带索引遍历:"
for i in "${!colors[@]}"; do
    echo "  [$i] ${colors[$i]}"
done

# ============================================================
# 3. for循环 - 数字范围
# ============================================================
echo ""
echo "--- 3. for循环 - 数字范围 ---"

echo "使用 {1..5} 语法:"
for i in {1..5}; do
    echo -n "  $i"
done
echo ""

echo "使用 {0..10..2} 步长语法:"
for i in {0..10..2}; do
    echo -n "  $i"
done
echo ""

echo "使用 seq 命令:"
for i in $(seq 1 3); do
    echo -n "  $i"
done
echo ""

# ============================================================
# 4. for循环 - C风格
# ============================================================
echo ""
echo "--- 4. for循环 - C风格 ---"

echo "C风格for循环 (0到4):"
for ((i = 0; i < 5; i++)); do
    echo -n "  $i"
done
echo ""

echo "倒序循环 (5到1):"
for ((i = 5; i >= 1; i--)); do
    echo -n "  $i"
done
echo ""

# ============================================================
# 5. for循环 - 遍历文件
# ============================================================
echo ""
echo "--- 5. for循环 - 遍历文件 ---"

# 创建临时测试文件
temp_dir=$(mktemp -d)
touch "$temp_dir/file1.txt" "$temp_dir/file2.txt" "$temp_dir/file3.log"

echo "遍历 $temp_dir 中的文件:"
for file in "$temp_dir"/*; do
    if [ -f "$file" ]; then
        echo "  文件: $(basename "$file")"
    fi
done

# 只遍历.txt文件
echo ""
echo "只遍历.txt文件:"
for file in "$temp_dir"/*.txt; do
    echo "  TXT文件: $(basename "$file")"
done

# 清理临时文件
rm -rf "$temp_dir"

# ============================================================
# 6. while循环
# ============================================================
echo ""
echo "--- 6. while循环 ---"

echo "基本while循环 (计数到5):"
count=1
while [ $count -le 5 ]; do
    echo -n "  $count"
    ((count++))
done
echo ""

# ============================================================
# 7. while循环 - 读取文件
# ============================================================
echo ""
echo "--- 7. while循环 - 读取文件 ---"

# 创建临时文件
temp_file=$(mktemp)
cat > "$temp_file" << EOF
第一行内容
第二行内容
第三行内容
EOF

echo "读取文件内容:"
while IFS= read -r line; do
    echo "  > $line"
done < "$temp_file"

# 清理临时文件
rm "$temp_file"

# ============================================================
# 8. while循环 - 处理命令输出
# ============================================================
echo ""
echo "--- 8. while循环 - 处理命令输出 ---"

echo "读取/etc/passwd前3行:"
head -3 /etc/passwd | while IFS=: read -r user _ uid gid _ home shell; do
    echo "  用户: $user, UID: $uid, Home: $home"
done

# ============================================================
# 9. until循环
# ============================================================
echo ""
echo "--- 9. until循环 ---"

echo "until循环 (直到count >= 5):"
count=1
until [ $count -ge 5 ]; do
    echo -n "  $count"
    ((count++))
done
echo ""

# ============================================================
# 10. 循环控制 - break
# ============================================================
echo ""
echo "--- 10. 循环控制 - break ---"

echo "在i=5时使用break跳出循环:"
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        echo "  遇到5，跳出循环"
        break
    fi
    echo -n "  $i"
done
echo ""

# ============================================================
# 11. 循环控制 - continue
# ============================================================
echo ""
echo "--- 11. 循环控制 - continue ---"

echo "跳过偶数:"
for i in {1..10}; do
    if (( i % 2 == 0 )); then
        continue
    fi
    echo -n "  $i"
done
echo ""

# ============================================================
# 12. 嵌套循环
# ============================================================
echo ""
echo "--- 12. 嵌套循环 ---"

echo "九九乘法表 (部分):"
for ((i = 1; i <= 5; i++)); do
    for ((j = 1; j <= i; j++)); do
        printf "%d×%d=%-2d " "$j" "$i" "$((i * j))"
    done
    echo ""
done

# ============================================================
# 13. break n - 跳出多层循环
# ============================================================
echo ""
echo "--- 13. break n - 跳出多层循环 ---"

echo "使用 break 2 跳出两层循环:"
for i in {1..3}; do
    for j in {1..3}; do
        echo "  i=$i, j=$j"
        if [ $j -eq 2 ]; then
            echo "  -> 遇到j=2，跳出所有循环"
            break 2
        fi
    done
done

# ============================================================
# 14. 实际应用：重试逻辑
# ============================================================
echo ""
echo "--- 14. 实际应用：重试逻辑 ---"

max_retries=3
retry_count=0
success=false

echo "模拟重试机制 (最多$max_retries次):"
while [ $retry_count -lt $max_retries ]; do
    ((retry_count++))
    echo "  尝试 #$retry_count..."
    
    # 模拟随机成功/失败
    if [ $retry_count -eq 2 ]; then
        echo "  ✓ 操作成功!"
        success=true
        break
    else
        echo "  ✗ 操作失败，稍后重试..."
        sleep 0.5
    fi
done

if [ "$success" = false ]; then
    echo "  所有重试均失败"
fi

# ============================================================
# 15. 实际应用：进度显示
# ============================================================
echo ""
echo "--- 15. 实际应用：进度显示 ---"

echo "处理进度:"
total=20
for ((i = 1; i <= total; i++)); do
    # 计算进度百分比
    percent=$((i * 100 / total))
    # 计算进度条长度
    filled=$((i * 20 / total))
    empty=$((20 - filled))
    
    # 构建进度条
    bar=$(printf "%${filled}s" | tr ' ' '█')
    space=$(printf "%${empty}s" | tr ' ' '░')
    
    # 显示进度（\r回到行首，覆盖显示）
    printf "\r  [%s%s] %3d%%" "$bar" "$space" "$percent"
    
    sleep 0.1
done
echo ""

# ============================================================
# 16. 实际应用：批量处理参数
# ============================================================
echo ""
echo "--- 16. 实际应用：批量处理参数 ---"

# 模拟批量参数
params=("--config" "/etc/app.conf" "--verbose" "--output" "/tmp/result")

echo "解析参数列表:"
i=0
while [ $i -lt ${#params[@]} ]; do
    case "${params[$i]}" in
        --config)
            ((i++))
            echo "  配置文件: ${params[$i]}"
            ;;
        --verbose)
            echo "  详细模式: 开启"
            ;;
        --output)
            ((i++))
            echo "  输出路径: ${params[$i]}"
            ;;
    esac
    ((i++))
done

echo ""
echo "=== 循环结构示例完成 ==="

