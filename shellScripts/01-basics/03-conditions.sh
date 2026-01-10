#!/bin/bash
#
# 脚本名称: 03-conditions.sh
# 描述: Shell条件判断示例
# 用法: ./03-conditions.sh [number]
#

set -euo pipefail

echo "=== Shell条件判断示例 ==="
echo ""

# ============================================================
# 1. 基本if语句
# ============================================================
echo "--- 1. 基本if语句 ---"

num=${1:-10}  # 使用第一个参数，默认为10
echo "输入数字: $num"

if [ "$num" -gt 0 ]; then
    echo "结果: 正数"
elif [ "$num" -lt 0 ]; then
    echo "结果: 负数"
else
    echo "结果: 零"
fi

# ============================================================
# 2. 文件测试
# ============================================================
echo ""
echo "--- 2. 文件测试 ---"

test_file="/etc/passwd"
test_dir="/tmp"

# 文件存在性检查
if [ -e "$test_file" ]; then
    echo "✓ $test_file 存在"
fi

# 是否为普通文件
if [ -f "$test_file" ]; then
    echo "✓ $test_file 是普通文件"
fi

# 是否为目录
if [ -d "$test_dir" ]; then
    echo "✓ $test_dir 是目录"
fi

# 是否可读
if [ -r "$test_file" ]; then
    echo "✓ $test_file 可读"
fi

# 文件大小是否大于0
if [ -s "$test_file" ]; then
    echo "✓ $test_file 非空"
fi

# 检查不存在的文件
if [ ! -e "/nonexistent/file" ]; then
    echo "✓ /nonexistent/file 不存在"
fi

# ============================================================
# 3. 字符串测试
# ============================================================
echo ""
echo "--- 3. 字符串测试 ---"

str1="hello"
str2="world"
empty_str=""

# 字符串非空
if [ -n "$str1" ]; then
    echo "✓ str1 非空: '$str1'"
fi

# 字符串为空
if [ -z "$empty_str" ]; then
    echo "✓ empty_str 为空"
fi

# 字符串相等
if [ "$str1" = "hello" ]; then
    echo "✓ str1 等于 'hello'"
fi

# 字符串不等
if [ "$str1" != "$str2" ]; then
    echo "✓ str1 ('$str1') 不等于 str2 ('$str2')"
fi

# ============================================================
# 4. 数值比较
# ============================================================
echo ""
echo "--- 4. 数值比较 ---"

a=10
b=20

echo "a = $a, b = $b"

if [ "$a" -eq 10 ]; then
    echo "✓ a 等于 10 (-eq)"
fi

if [ "$a" -ne "$b" ]; then
    echo "✓ a 不等于 b (-ne)"
fi

if [ "$a" -lt "$b" ]; then
    echo "✓ a 小于 b (-lt)"
fi

if [ "$a" -le 10 ]; then
    echo "✓ a 小于等于 10 (-le)"
fi

if [ "$b" -gt "$a" ]; then
    echo "✓ b 大于 a (-gt)"
fi

if [ "$b" -ge 20 ]; then
    echo "✓ b 大于等于 20 (-ge)"
fi

# ============================================================
# 5. [[ ]] 扩展测试（Bash专用）
# ============================================================
echo ""
echo "--- 5. [[ ]] 扩展测试 ---"

filename="report_2025.txt"

# 模式匹配
if [[ $filename == *.txt ]]; then
    echo "✓ $filename 是txt文件（模式匹配）"
fi

# 正则匹配
if [[ $filename =~ ^report_[0-9]{4}\.txt$ ]]; then
    echo "✓ $filename 匹配正则表达式 (report_YYYY.txt格式)"
fi

# 逻辑运算符可以直接在 [[ ]] 内使用
if [[ $a -lt 100 && $b -gt 10 ]]; then
    echo "✓ a < 100 且 b > 10"
fi

if [[ $a -lt 5 || $b -gt 15 ]]; then
    echo "✓ a < 5 或 b > 15"
fi

# ============================================================
# 6. (( )) 算术测试
# ============================================================
echo ""
echo "--- 6. (( )) 算术测试 ---"

x=15
y=20

# 在 (( )) 中可以使用标准数学比较符
if (( x < y )); then
    echo "✓ x < y (使用 < 运算符)"
fi

if (( x >= 10 && y <= 30 )); then
    echo "✓ 10 <= x 且 y <= 30"
fi

if (( (x + y) == 35 )); then
    echo "✓ x + y = 35"
fi

# ============================================================
# 7. 逻辑运算
# ============================================================
echo ""
echo "--- 7. 逻辑运算 ---"

age=25
has_license=true

# AND 运算
if [ "$age" -ge 18 ] && [ "$has_license" = "true" ]; then
    echo "✓ 可以开车（年龄>=18 且 有驾照）"
fi

# OR 运算
score=55
if [ "$score" -ge 60 ] || [ "$score" -ge 50 ]; then
    echo "✓ 通过测试（分数>=60 或 分数>=50）"
fi

# NOT 运算
is_debug=false
if [ ! "$is_debug" = "true" ]; then
    echo "✓ 非调试模式"
fi

# ============================================================
# 8. case语句
# ============================================================
echo ""
echo "--- 8. case语句 ---"

fruit="apple"
echo "水果: $fruit"

case $fruit in
    apple)
        echo "  这是苹果 🍎"
        ;;
    banana)
        echo "  这是香蕉 🍌"
        ;;
    orange|lemon)
        echo "  这是柑橘类水果 🍊"
        ;;
    *)
        echo "  未知水果"
        ;;
esac

# case用于服务控制的典型用法
action="status"
echo ""
echo "服务操作: $action"

case $action in
    start)
        echo "  启动服务..."
        ;;
    stop)
        echo "  停止服务..."
        ;;
    restart)
        echo "  重启服务..."
        ;;
    status)
        echo "  服务状态: 运行中"
        ;;
    *)
        echo "  用法: {start|stop|restart|status}"
        ;;
esac

# ============================================================
# 9. 条件表达式的简写
# ============================================================
echo ""
echo "--- 9. 条件表达式简写 ---"

# && 短路与：前面成功才执行后面
[ -d "/tmp" ] && echo "✓ /tmp 目录存在（使用 && 简写）"

# || 短路或：前面失败才执行后面
[ -d "/nonexistent" ] || echo "✓ /nonexistent 不存在（使用 || 简写）"

# 组合使用
file_check="/etc/passwd"
[ -f "$file_check" ] && echo "✓ $file_check 是文件" || echo "✗ $file_check 不是文件"

# ============================================================
# 10. 实际应用示例：命令行参数验证
# ============================================================
echo ""
echo "--- 10. 实际应用：参数验证 ---"

# 模拟验证脚本参数
validate_input() {
    local input="${1:-}"
    
    # 检查是否为空
    if [[ -z "$input" ]]; then
        echo "错误: 输入不能为空"
        return 1
    fi
    
    # 检查是否为数字
    if [[ ! "$input" =~ ^[0-9]+$ ]]; then
        echo "错误: 输入必须是数字"
        return 1
    fi
    
    # 检查范围
    if (( input < 1 || input > 100 )); then
        echo "错误: 数字必须在1-100之间"
        return 1
    fi
    
    echo "✓ 输入验证通过: $input"
    return 0
}

# 测试验证函数
validate_input "50"
validate_input "" || true  # 允许失败
validate_input "abc" || true
validate_input "150" || true

echo ""
echo "=== 条件判断示例完成 ==="

