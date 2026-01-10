#!/bin/bash
#
# 脚本名称: 05-functions.sh
# 描述: Shell函数定义与使用示例
# 用法: ./05-functions.sh
#

set -euo pipefail

echo "=== Shell函数示例 ==="
echo ""

# ============================================================
# 1. 基本函数定义
# ============================================================
echo "--- 1. 基本函数定义 ---"

# 方式1：标准语法（推荐）
greet() {
    echo "你好，欢迎学习Shell函数!"
}

# 方式2：带function关键字
function say_goodbye {
    echo "再见，祝学习愉快!"
}

# 调用函数
greet
say_goodbye

# ============================================================
# 2. 带参数的函数
# ============================================================
echo ""
echo "--- 2. 带参数的函数 ---"

greet_user() {
    local name="$1"
    local time="$2"
    echo "$time好, $name!"
}

greet_user "张三" "上午"
greet_user "李四" "下午"

# 显示所有参数
show_params() {
    echo "参数个数: $#"
    echo "所有参数: $@"
    echo "第一个参数: ${1:-无}"
    echo "第二个参数: ${2:-无}"
    echo "第三个参数: ${3:-无}"
}

echo ""
echo "调用 show_params a b c:"
show_params a b c

# ============================================================
# 3. 返回值
# ============================================================
echo ""
echo "--- 3. 返回值 ---"

# 使用return返回状态码 (0-255)
is_even() {
    local num=$1
    if (( num % 2 == 0 )); then
        return 0  # 成功/真
    else
        return 1  # 失败/假
    fi
}

echo "检查数字是否为偶数:"
for n in 2 3 4 5; do
    if is_even $n; then
        echo "  $n 是偶数 ✓"
    else
        echo "  $n 是奇数"
    fi
done

# 使用echo返回数据
get_sum() {
    local a=$1
    local b=$2
    echo $((a + b))  # 通过echo输出结果
}

result=$(get_sum 15 25)
echo ""
echo "15 + 25 = $result"

# 返回多个值
get_stats() {
    local nums=("$@")
    local sum=0
    local count=${#nums[@]}
    
    for n in "${nums[@]}"; do
        ((sum += n))
    done
    
    local avg=$((sum / count))
    
    # 返回多个值（空格分隔）
    echo "$sum $avg $count"
}

echo ""
echo "统计 10 20 30 40 50:"
read -r sum avg count <<< "$(get_stats 10 20 30 40 50)"
echo "  总和: $sum, 平均: $avg, 个数: $count"

# ============================================================
# 4. 局部变量与全局变量
# ============================================================
echo ""
echo "--- 4. 局部变量与全局变量 ---"

global_var="我是全局变量"

test_scope() {
    local local_var="我是局部变量"
    global_var="全局变量被修改了"
    new_global="函数内创建的全局变量"
    
    echo "函数内 - local_var: $local_var"
    echo "函数内 - global_var: $global_var"
}

echo "调用前 - global_var: $global_var"
test_scope
echo "调用后 - global_var: $global_var"
echo "调用后 - new_global: $new_global"
echo "调用后 - local_var: ${local_var:-未定义（正常，因为是局部变量）}"

# ============================================================
# 5. 递归函数
# ============================================================
echo ""
echo "--- 5. 递归函数 ---"

# 计算阶乘
factorial() {
    local n=$1
    if (( n <= 1 )); then
        echo 1
    else
        local sub=$(factorial $((n - 1)))
        echo $((n * sub))
    fi
}

echo "阶乘计算:"
for n in 1 3 5 7; do
    echo "  $n! = $(factorial $n)"
done

# 斐波那契数列
fibonacci() {
    local n=$1
    if (( n <= 1 )); then
        echo $n
    else
        local a=$(fibonacci $((n - 1)))
        local b=$(fibonacci $((n - 2)))
        echo $((a + b))
    fi
}

echo ""
echo "斐波那契数列 (前8项):"
for ((i = 0; i < 8; i++)); do
    echo -n "  $(fibonacci $i)"
done
echo ""

# ============================================================
# 6. 默认参数值
# ============================================================
echo ""
echo "--- 6. 默认参数值 ---"

create_user() {
    local username="${1:-guest}"
    local role="${2:-user}"
    local active="${3:-true}"
    
    echo "创建用户: $username, 角色: $role, 激活: $active"
}

create_user                           # 使用全部默认值
create_user "admin"                   # 指定用户名
create_user "developer" "dev"         # 指定用户名和角色
create_user "tester" "qa" "false"     # 指定所有参数

# ============================================================
# 7. 函数库模式
# ============================================================
echo ""
echo "--- 7. 函数库模式 ---"

# 日志函数库
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_warn() {
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

log_info "这是一条信息日志"
log_warn "这是一条警告日志"
log_error "这是一条错误日志"

# ============================================================
# 8. 实用函数示例
# ============================================================
echo ""
echo "--- 8. 实用函数示例 ---"

# 检查命令是否存在
command_exists() {
    command -v "$1" &> /dev/null
}

echo "检查命令是否存在:"
for cmd in bash python3 nonexistent_cmd; do
    if command_exists "$cmd"; then
        echo "  ✓ $cmd 已安装"
    else
        echo "  ✗ $cmd 未安装"
    fi
done

# 安全读取文件
safe_read_file() {
    local file="$1"
    if [[ -f "$file" && -r "$file" ]]; then
        cat "$file"
        return 0
    else
        echo "无法读取文件: $file" >&2
        return 1
    fi
}

# 带超时的等待
wait_for_condition() {
    local timeout="$1"
    local interval="${2:-1}"
    local condition="$3"
    local elapsed=0
    
    while (( elapsed < timeout )); do
        if eval "$condition"; then
            return 0
        fi
        sleep "$interval"
        ((elapsed += interval))
    done
    
    return 1
}

echo ""
echo "带超时的条件等待示例:"
# 创建临时文件模拟条件
temp_file=$(mktemp)
(sleep 1 && touch "${temp_file}.ready") &

if wait_for_condition 5 0.5 "[[ -f '${temp_file}.ready' ]]"; then
    echo "  ✓ 条件满足"
else
    echo "  ✗ 等待超时"
fi

rm -f "$temp_file" "${temp_file}.ready"

# ============================================================
# 9. 错误处理函数
# ============================================================
echo ""
echo "--- 9. 错误处理函数 ---"

# 退出时清理
cleanup() {
    echo "  执行清理操作..."
    # 这里可以删除临时文件、关闭连接等
}

# 错误处理
handle_error() {
    local line_no="$1"
    local error_code="$2"
    echo "  错误发生在第 $line_no 行，退出码: $error_code"
}

# 注册trap（这里仅作演示，不实际触发）
echo "错误处理trap示例（仅展示语法）:"
echo "  trap 'cleanup' EXIT"
echo "  trap 'handle_error \$LINENO \$?' ERR"

# ============================================================
# 10. 高级函数技巧
# ============================================================
echo ""
echo "--- 10. 高级函数技巧 ---"

# 使用nameref传递变量名 (Bash 4.3+)
if (( BASH_VERSINFO[0] >= 4 && BASH_VERSINFO[1] >= 3 )); then
    modify_array() {
        local -n arr_ref=$1  # nameref
        arr_ref+=("新元素")
    }
    
    my_array=("元素1" "元素2")
    echo "修改前: ${my_array[*]}"
    modify_array my_array
    echo "修改后: ${my_array[*]}"
else
    echo "nameref需要Bash 4.3+，当前版本: $BASH_VERSION"
fi

# 函数作为参数（回调模式）
echo ""
echo "回调函数模式:"

process_each() {
    local callback="$1"
    shift
    for item in "$@"; do
        "$callback" "$item"
    done
}

print_upper() {
    echo "  ${1^^}"
}

process_each print_upper "hello" "world" "shell"

# ============================================================
# 11. 实际应用：配置解析函数
# ============================================================
echo ""
echo "--- 11. 实际应用：配置解析函数 ---"

# 解析key=value格式的配置
parse_config() {
    local config_content="$1"
    
    while IFS='=' read -r key value; do
        # 跳过空行和注释
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        # 去除空格
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        echo "  $key = $value"
    done <<< "$config_content"
}

config="
# 应用配置
app_name = MyApp
version = 1.0.0
debug = true
port = 8080
"

echo "解析配置:"
parse_config "$config"

# ============================================================
# 12. 实际应用：参数验证函数
# ============================================================
echo ""
echo "--- 12. 实际应用：参数验证函数 ---"

validate_email() {
    local email="$1"
    if [[ "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        return 0
    fi
    return 1
}

validate_ip() {
    local ip="$1"
    if [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        return 0
    fi
    return 1
}

echo "验证Email:"
for email in "test@example.com" "invalid-email" "user@domain.org"; do
    if validate_email "$email"; then
        echo "  ✓ $email 有效"
    else
        echo "  ✗ $email 无效"
    fi
done

echo ""
echo "验证IP地址:"
for ip in "192.168.1.1" "256.1.1.1" "10.0.0.1"; do
    if validate_ip "$ip"; then
        echo "  ✓ $ip 格式正确"
    else
        echo "  ✗ $ip 格式错误"
    fi
done

echo ""
echo "=== 函数示例完成 ==="

