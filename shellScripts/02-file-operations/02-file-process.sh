#!/bin/bash
#
# 脚本名称: 02-file-process.sh
# 描述: 文件读写与文本处理示例
# 用法: ./02-file-process.sh
#

set -euo pipefail

echo "=== 文件读写与文本处理示例 ==="
echo ""

# 创建临时工作目录
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

echo "工作目录: $WORK_DIR"
echo ""

# ============================================================
# 1. 创建测试文件
# ============================================================
echo "--- 1. 创建测试文件 ---"

# 使用重定向创建文件
echo "第一行内容" > "$WORK_DIR/test.txt"
echo "第二行内容" >> "$WORK_DIR/test.txt"
echo "第三行内容" >> "$WORK_DIR/test.txt"

echo "使用 > 和 >> 创建文件完成"

# 使用 Here Document 创建配置文件
cat > "$WORK_DIR/config.ini" << 'EOF'
# 应用程序配置文件
[server]
host=localhost
port=8080
debug=true

[database]
host=db.example.com
port=5432
name=myapp
user=admin
password=secret123

[logging]
level=INFO
file=/var/log/app.log
EOF

echo "使用 Here Document 创建配置文件完成"

# 创建CSV数据文件
cat > "$WORK_DIR/data.csv" << 'EOF'
name,age,city,salary
张三,28,北京,15000
李四,35,上海,22000
王五,24,广州,12000
赵六,42,深圳,35000
钱七,31,杭州,18000
EOF

echo "创建CSV数据文件完成"

# 创建日志文件
cat > "$WORK_DIR/app.log" << 'EOF'
2025-01-15 08:30:15 [INFO] Application started
2025-01-15 08:30:16 [DEBUG] Loading configuration
2025-01-15 08:31:00 [INFO] Connected to database
2025-01-15 08:32:45 [WARN] High memory usage detected
2025-01-15 08:33:00 [ERROR] Failed to process request: timeout
2025-01-15 08:35:20 [INFO] Request processed successfully
2025-01-15 08:40:00 [ERROR] Database connection lost
2025-01-15 08:40:05 [INFO] Reconnecting to database
2025-01-15 08:40:10 [INFO] Connection restored
EOF

echo "创建日志文件完成"
echo ""

# ============================================================
# 2. 读取文件 - 多种方法
# ============================================================
echo "--- 2. 读取文件 - 多种方法 ---"

echo ""
echo "方法1: 使用 cat 读取整个文件"
echo "----------------------------------------"
cat "$WORK_DIR/test.txt"

echo ""
echo "方法2: 使用 while read 逐行读取"
echo "----------------------------------------"
line_num=0
while IFS= read -r line; do
    ((line_num++))
    echo "第${line_num}行: $line"
done < "$WORK_DIR/test.txt"

echo ""
echo "方法3: 读取到数组"
echo "----------------------------------------"
mapfile -t lines < "$WORK_DIR/test.txt"
echo "文件共 ${#lines[@]} 行"
echo "第2行内容: ${lines[1]}"

echo ""
echo "方法4: 读取特定行"
echo "----------------------------------------"
echo "配置文件第5行: $(sed -n '5p' "$WORK_DIR/config.ini")"
echo "配置文件第8-10行:"
sed -n '8,10p' "$WORK_DIR/config.ini"

# ============================================================
# 3. grep - 文本搜索
# ============================================================
echo ""
echo "--- 3. grep - 文本搜索 ---"

echo ""
echo "搜索包含 'host' 的行:"
grep "host" "$WORK_DIR/config.ini"

echo ""
echo "搜索包含 'error' 的行（忽略大小写）:"
grep -i "error" "$WORK_DIR/app.log"

echo ""
echo "显示行号搜索 INFO 日志:"
grep -n "INFO" "$WORK_DIR/app.log"

echo ""
echo "统计 ERROR 出现次数:"
error_count=$(grep -c "ERROR" "$WORK_DIR/app.log")
echo "ERROR 出现 $error_count 次"

echo ""
echo "反向匹配 - 不包含注释的配置行:"
grep -v "^#" "$WORK_DIR/config.ini" | grep -v "^$" | grep -v "^\["

echo ""
echo "使用正则表达式搜索 - 查找时间戳:"
grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}" "$WORK_DIR/app.log" | head -3

# ============================================================
# 4. sed - 流编辑器
# ============================================================
echo ""
echo "--- 4. sed - 流编辑器 ---"

echo ""
echo "替换 localhost 为 127.0.0.1:"
sed 's/localhost/127.0.0.1/g' "$WORK_DIR/config.ini" | grep "host="

echo ""
echo "删除注释行:"
sed '/^#/d' "$WORK_DIR/config.ini" | head -5

echo ""
echo "删除空行:"
sed '/^$/d' "$WORK_DIR/config.ini" | head -8

echo ""
echo "在第2行后插入新行:"
sed '2a\# 这是插入的新注释' "$WORK_DIR/config.ini" | head -5

echo ""
echo "替换整行（修改端口）:"
sed 's/^port=.*/port=9090/' "$WORK_DIR/config.ini" | grep "port="

echo ""
echo "多个替换操作:"
sed -e 's/INFO/信息/g' -e 's/ERROR/错误/g' "$WORK_DIR/app.log" | head -5

# ============================================================
# 5. awk - 文本处理
# ============================================================
echo ""
echo "--- 5. awk - 文本处理 ---"

echo ""
echo "打印CSV第1列（姓名）:"
awk -F',' 'NR>1 {print $1}' "$WORK_DIR/data.csv"

echo ""
echo "打印姓名和薪资:"
awk -F',' 'NR>1 {print $1, "-", $4}' "$WORK_DIR/data.csv"

echo ""
echo "筛选薪资大于15000的人:"
awk -F',' 'NR>1 && $4 > 15000 {print $1, $4}' "$WORK_DIR/data.csv"

echo ""
echo "计算平均薪资:"
awk -F',' 'NR>1 {sum += $4; count++} END {printf "平均薪资: %.2f\n", sum/count}' "$WORK_DIR/data.csv"

echo ""
echo "计算薪资总和:"
awk -F',' 'NR>1 {sum += $4} END {print "薪资总和:", sum}' "$WORK_DIR/data.csv"

echo ""
echo "格式化输出表格:"
awk -F',' 'BEGIN {printf "%-8s %-4s %-8s %s\n", "姓名", "年龄", "城市", "薪资"; print "----------------------------"}
     NR>1 {printf "%-8s %-4s %-8s %s\n", $1, $2, $3, $4}' "$WORK_DIR/data.csv"

echo ""
echo "从日志中提取时间和级别:"
awk '{print $1, $2, $3}' "$WORK_DIR/app.log"

echo ""
echo "统计各日志级别数量:"
awk '{
    # 提取 [LEVEL] 中的级别
    match($0, /\[([A-Z]+)\]/, arr)
    if (arr[1] != "") levels[arr[1]]++
}
END {
    for (level in levels) print level ":", levels[level]
}' "$WORK_DIR/app.log"

# ============================================================
# 6. 其他文本工具
# ============================================================
echo ""
echo "--- 6. 其他文本工具 ---"

echo ""
echo "cut - 提取字段:"
echo "提取CSV第1和第4列:"
cut -d',' -f1,4 "$WORK_DIR/data.csv"

echo ""
echo "sort - 排序:"
echo "按第4列（薪资）数值排序:"
tail -n +2 "$WORK_DIR/data.csv" | sort -t',' -k4 -n

echo ""
echo "wc - 统计:"
echo "日志文件统计: $(wc -l < "$WORK_DIR/app.log") 行, $(wc -w < "$WORK_DIR/app.log") 词, $(wc -c < "$WORK_DIR/app.log") 字节"

echo ""
echo "tr - 字符转换:"
echo "转换为大写:"
echo "hello world" | tr 'a-z' 'A-Z'

echo ""
echo "head 和 tail:"
echo "日志前2行:"
head -2 "$WORK_DIR/app.log"
echo "日志后2行:"
tail -2 "$WORK_DIR/app.log"

# ============================================================
# 7. 管道组合
# ============================================================
echo ""
echo "--- 7. 管道组合 ---"

echo ""
echo "示例1: 查找并统计唯一值"
echo "统计每个城市的人数:"
tail -n +2 "$WORK_DIR/data.csv" | cut -d',' -f3 | sort | uniq -c

echo ""
echo "示例2: 多级管道处理"
echo "日志级别按频率排序:"
grep -oE '\[(INFO|WARN|ERROR|DEBUG)\]' "$WORK_DIR/app.log" | \
    sort | uniq -c | sort -rn

echo ""
echo "示例3: 复杂数据提取"
echo "薪资最高的人:"
tail -n +2 "$WORK_DIR/data.csv" | sort -t',' -k4 -rn | head -1 | \
    awk -F',' '{print $1 " 薪资最高: " $4}'

# ============================================================
# 8. 实用脚本示例
# ============================================================
echo ""
echo "--- 8. 实用脚本示例 ---"

echo ""
echo "解析INI配置文件:"

parse_ini() {
    local file="$1"
    local section="$2"
    local key="$3"
    
    awk -F= -v section="[$section]" -v key="$key" '
        $0 == section { found=1; next }
        /^\[/ { found=0 }
        found && $1 == key { gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2; exit }
    ' "$file"
}

echo "获取 [database] 的 host: $(parse_ini "$WORK_DIR/config.ini" database host)"
echo "获取 [server] 的 port: $(parse_ini "$WORK_DIR/config.ini" server port)"

echo ""
echo "日志分析 - 按小时统计:"
awk '{
    split($2, time, ":")
    hour = time[1]
    hours[hour]++
}
END {
    for (h in hours) printf "  %s:00 - %d 条日志\n", h, hours[h]
}' "$WORK_DIR/app.log" | sort

# ============================================================
# 9. 文件写入的高级用法
# ============================================================
echo ""
echo "--- 9. 文件写入高级用法 ---"

echo ""
echo "使用 tee 同时输出到屏幕和文件:"
echo "这是tee命令的演示" | tee "$WORK_DIR/tee_output.txt"
echo "(文件已保存到 $WORK_DIR/tee_output.txt)"

echo ""
echo "使用 process substitution 处理多个输入:"
paste <(cut -d',' -f1 "$WORK_DIR/data.csv") <(cut -d',' -f4 "$WORK_DIR/data.csv") | head -3

echo ""
echo "生成报告并保存:"
{
    echo "=== 数据报告 ==="
    echo "生成时间: $(date)"
    echo ""
    echo "人员统计:"
    awk -F',' 'NR>1 {print "  -", $1, "(" $3 ")"}' "$WORK_DIR/data.csv"
    echo ""
    echo "薪资汇总:"
    awk -F',' 'NR>1 {sum+=$4; count++} END {
        print "  总人数:", count
        print "  薪资总额:", sum
        printf "  平均薪资: %.2f\n", sum/count
    }' "$WORK_DIR/data.csv"
} > "$WORK_DIR/report.txt"

echo "报告已生成:"
cat "$WORK_DIR/report.txt"

echo ""
echo "=== 文件读写与文本处理示例完成 ==="

