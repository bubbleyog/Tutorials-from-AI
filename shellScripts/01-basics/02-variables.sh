#!/bin/bash
#
# 脚本名称: 02-variables.sh
# 描述: Shell变量的定义与使用示例
# 用法: ./02-variables.sh
#

set -euo pipefail

echo "=== Shell变量示例 ==="
echo ""

# ============================================================
# 1. 基本变量定义
# ============================================================
echo "--- 1. 基本变量定义 ---"

# 注意：等号两边不能有空格！
name="Linux"
version=6.1
year=2025

echo "系统: $name"
echo "版本: $version"
echo "年份: $year"

# ============================================================
# 2. 变量引用方式
# ============================================================
echo ""
echo "--- 2. 变量引用方式 ---"

file="data"
# ${} 形式更安全，避免歧义
echo "文件名: ${file}"
echo "备份文件: ${file}_backup"    # 正确
# echo "$file_backup"              # 错误：会被解释为变量 file_backup

# ============================================================
# 3. 只读变量
# ============================================================
echo ""
echo "--- 3. 只读变量 ---"

readonly PI=3.14159
echo "PI = $PI"
# PI=3.14  # 这行会报错，因为PI是只读的

# ============================================================
# 4. 环境变量
# ============================================================
echo ""
echo "--- 4. 环境变量 ---"

echo "HOME: $HOME"
echo "PATH: $PATH"
echo "USER: $USER"
echo "SHELL: $SHELL"
echo "PWD: $PWD"
echo "LANG: ${LANG:-未设置}"

# 导出自定义环境变量
export MY_APP_DEBUG="true"
echo "MY_APP_DEBUG: $MY_APP_DEBUG"

# ============================================================
# 5. 特殊变量
# ============================================================
echo ""
echo "--- 5. 特殊变量 ---"

echo "脚本名称 (\$0): $0"
echo "参数个数 (\$#): $#"
echo "所有参数 (\$@): $*"
echo "当前PID (\$\$): $$"
echo "上一命令退出状态 (\$?): 0"  # echo命令成功，所以是0

# ============================================================
# 6. 数值运算
# ============================================================
echo ""
echo "--- 6. 数值运算 ---"

a=15
b=4

# 算术扩展 $(( ))
echo "a = $a, b = $b"
echo "a + b = $((a + b))"
echo "a - b = $((a - b))"
echo "a * b = $((a * b))"
echo "a / b = $((a / b))"      # 整数除法
echo "a % b = $((a % b))"      # 取模
echo "a ** 2 = $((a ** 2))"    # 幂运算

# 自增自减
((a++))
echo "a++ 后: a = $a"

# ============================================================
# 7. 字符串操作
# ============================================================
echo ""
echo "--- 7. 字符串操作 ---"

str="Hello, World!"

echo "原始字符串: $str"
echo "字符串长度: ${#str}"

# 子串提取
echo "前5个字符: ${str:0:5}"
echo "第7个字符后: ${str:7}"

# 替换
echo "替换World为Linux: ${str/World/Linux}"

# 大小写转换（Bash 4.0+）
echo "全部大写: ${str^^}"
echo "全部小写: ${str,,}"

# ============================================================
# 8. 默认值处理
# ============================================================
echo ""
echo "--- 8. 默认值处理 ---"

# ${var:-default}: 如果var未定义或为空，使用default
undefined_var=""
echo "使用默认值: ${undefined_var:-默认值}"

# ${var:=default}: 如果var未定义或为空，设置为default并使用
: ${CONFIG_DIR:="/etc/myapp"}
echo "CONFIG_DIR: $CONFIG_DIR"

# ${var:+value}: 如果var已定义且非空，使用value
existing="exists"
echo "存在时替换: ${existing:+替换值}"

# ============================================================
# 9. 路径处理
# ============================================================
echo ""
echo "--- 9. 路径处理 ---"

filepath="/home/user/documents/report.tar.gz"

echo "完整路径: $filepath"
echo "文件名: $(basename "$filepath")"
echo "目录名: $(dirname "$filepath")"

# 扩展名处理
filename=$(basename "$filepath")
echo "去掉.gz: ${filename%.gz}"
echo "去掉所有扩展名: ${filename%%.*}"
echo "只保留扩展名: ${filename##*.}"

# ============================================================
# 10. 数组变量
# ============================================================
echo ""
echo "--- 10. 数组变量 ---"

# 定义数组
fruits=("apple" "banana" "cherry" "date")

echo "第一个元素: ${fruits[0]}"
echo "第三个元素: ${fruits[2]}"
echo "所有元素: ${fruits[@]}"
echo "元素个数: ${#fruits[@]}"
echo "所有索引: ${!fruits[@]}"

# 添加元素
fruits+=("elderberry")
echo "添加后: ${fruits[@]}"

# 遍历数组
echo "遍历数组:"
for fruit in "${fruits[@]}"; do
    echo "  - $fruit"
done

# ============================================================
# 11. 关联数组（Bash 4.0+）
# ============================================================
echo ""
echo "--- 11. 关联数组 ---"

declare -A user_info
user_info[name]="张三"
user_info[age]=30
user_info[city]="北京"

echo "姓名: ${user_info[name]}"
echo "年龄: ${user_info[age]}"
echo "城市: ${user_info[city]}"

# 遍历关联数组
echo "遍历关联数组:"
for key in "${!user_info[@]}"; do
    echo "  $key: ${user_info[$key]}"
done

echo ""
echo "=== 变量示例完成 ==="

