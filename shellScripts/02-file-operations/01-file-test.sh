#!/bin/bash
#
# 脚本名称: 01-file-test.sh
# 描述: 文件测试操作示例
# 用法: ./01-file-test.sh [file_path]
#

set -euo pipefail

echo "=== 文件测试示例 ==="
echo ""

# ============================================================
# 1. 基本文件存在性测试
# ============================================================
echo "--- 1. 基本文件存在性测试 ---"

# 测试常见系统文件
test_files=(
    "/etc/passwd"
    "/etc/shadow"
    "/tmp"
    "/nonexistent"
    "/bin/bash"
)

for file in "${test_files[@]}"; do
    if [[ -e "$file" ]]; then
        echo "✓ $file 存在"
    else
        echo "✗ $file 不存在"
    fi
done

# ============================================================
# 2. 文件类型测试
# ============================================================
echo ""
echo "--- 2. 文件类型测试 ---"

check_file_type() {
    local path="$1"
    
    if [[ ! -e "$path" ]]; then
        echo "$path: 不存在"
        return
    fi
    
    local type_desc=""
    
    if [[ -f "$path" ]]; then
        type_desc="普通文件"
    elif [[ -d "$path" ]]; then
        type_desc="目录"
    elif [[ -L "$path" ]]; then
        type_desc="符号链接"
    elif [[ -b "$path" ]]; then
        type_desc="块设备"
    elif [[ -c "$path" ]]; then
        type_desc="字符设备"
    elif [[ -p "$path" ]]; then
        type_desc="命名管道"
    elif [[ -S "$path" ]]; then
        type_desc="套接字"
    else
        type_desc="未知类型"
    fi
    
    echo "$path: $type_desc"
}

check_file_type "/etc/passwd"
check_file_type "/tmp"
check_file_type "/dev/null"
check_file_type "/dev/sda" 2>/dev/null || check_file_type "/dev/vda" 2>/dev/null || echo "/dev/sda 或 /dev/vda: 设备不存在"

# ============================================================
# 3. 文件权限测试
# ============================================================
echo ""
echo "--- 3. 文件权限测试 ---"

check_permissions() {
    local file="$1"
    
    if [[ ! -e "$file" ]]; then
        echo "$file: 不存在"
        return
    fi
    
    echo "$file 权限检查:"
    
    [[ -r "$file" ]] && echo "  ✓ 可读" || echo "  ✗ 不可读"
    [[ -w "$file" ]] && echo "  ✓ 可写" || echo "  ✗ 不可写"
    [[ -x "$file" ]] && echo "  ✓ 可执行" || echo "  ✗ 不可执行"
}

check_permissions "/etc/passwd"
check_permissions "/etc/shadow"
check_permissions "/bin/bash"

# ============================================================
# 4. 文件属性测试
# ============================================================
echo ""
echo "--- 4. 文件属性测试 ---"

check_attributes() {
    local file="$1"
    
    if [[ ! -e "$file" ]]; then
        echo "$file: 不存在"
        return
    fi
    
    echo "$file 属性:"
    
    # 是否为空
    if [[ -s "$file" ]]; then
        echo "  - 文件非空"
    else
        echo "  - 文件为空"
    fi
    
    # 所有权检查
    if [[ -O "$file" ]]; then
        echo "  - 当前用户是所有者"
    else
        echo "  - 当前用户不是所有者"
    fi
    
    # 获取文件大小（兼容Linux和macOS）
    if command -v stat &>/dev/null; then
        local size
        size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file" 2>/dev/null)
        echo "  - 大小: $size 字节"
    fi
}

check_attributes "/etc/passwd"

# ============================================================
# 5. 文件比较测试
# ============================================================
echo ""
echo "--- 5. 文件比较测试 ---"

# 创建临时测试文件
temp_dir=$(mktemp -d)
file1="$temp_dir/file1.txt"
file2="$temp_dir/file2.txt"

echo "创建于: $(date)" > "$file1"
sleep 1
echo "创建于: $(date)" > "$file2"

echo "比较 $file1 和 $file2:"

if [[ "$file1" -nt "$file2" ]]; then
    echo "  file1 比 file2 新"
elif [[ "$file1" -ot "$file2" ]]; then
    echo "  file1 比 file2 旧"
else
    echo "  修改时间相同"
fi

# 创建硬链接测试
link_file="$temp_dir/link_to_file1"
ln "$file1" "$link_file"

if [[ "$file1" -ef "$link_file" ]]; then
    echo "  file1 和 link_to_file1 是同一文件（硬链接）"
fi

# 清理
rm -rf "$temp_dir"

# ============================================================
# 6. 实用函数：完整文件信息
# ============================================================
echo ""
echo "--- 6. 完整文件信息函数 ---"

file_info() {
    local file="$1"
    
    echo "═══════════════════════════════════════════════════"
    echo "文件信息: $file"
    echo "═══════════════════════════════════════════════════"
    
    # 检查存在
    if [[ ! -e "$file" ]]; then
        echo "状态: 不存在"
        return 1
    fi
    
    # 类型
    local type_str
    if [[ -f "$file" ]]; then
        type_str="普通文件"
    elif [[ -d "$file" ]]; then
        type_str="目录"
    elif [[ -L "$file" ]]; then
        type_str="符号链接 -> $(readlink "$file")"
    else
        type_str="特殊文件"
    fi
    echo "类型: $type_str"
    
    # 权限
    local perm_str=""
    [[ -r "$file" ]] && perm_str+="r" || perm_str+="-"
    [[ -w "$file" ]] && perm_str+="w" || perm_str+="-"
    [[ -x "$file" ]] && perm_str+="x" || perm_str+="-"
    echo "权限: $perm_str"
    
    # 大小
    if [[ -f "$file" ]]; then
        local size
        size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file" 2>/dev/null)
        # 人类可读格式
        if (( size >= 1073741824 )); then
            printf "大小: %.2f GB\n" "$(echo "scale=2; $size/1073741824" | bc)"
        elif (( size >= 1048576 )); then
            printf "大小: %.2f MB\n" "$(echo "scale=2; $size/1048576" | bc)"
        elif (( size >= 1024 )); then
            printf "大小: %.2f KB\n" "$(echo "scale=2; $size/1024" | bc)"
        else
            echo "大小: $size 字节"
        fi
    fi
    
    # 修改时间
    if command -v stat &>/dev/null; then
        local mtime
        mtime=$(stat -c %y "$file" 2>/dev/null || stat -f "%Sm" "$file" 2>/dev/null)
        echo "修改时间: $mtime"
    fi
    
    echo "═══════════════════════════════════════════════════"
}

# 测试文件信息函数
if [[ $# -gt 0 ]]; then
    file_info "$1"
else
    file_info "/etc/passwd"
fi

# ============================================================
# 7. 批量文件检测
# ============================================================
echo ""
echo "--- 7. 批量文件检测 ---"

# 检测多个文件并汇总
batch_check() {
    local files=("$@")
    local exist_count=0
    local file_count=0
    local dir_count=0
    local missing_count=0
    
    for f in "${files[@]}"; do
        if [[ -e "$f" ]]; then
            ((exist_count++))
            if [[ -f "$f" ]]; then
                ((file_count++))
            elif [[ -d "$f" ]]; then
                ((dir_count++))
            fi
        else
            ((missing_count++))
        fi
    done
    
    echo "检测结果汇总:"
    echo "  - 存在: $exist_count"
    echo "    - 文件: $file_count"
    echo "    - 目录: $dir_count"
    echo "  - 缺失: $missing_count"
}

batch_check "/etc/passwd" "/etc/hosts" "/tmp" "/var/log" "/nonexistent1" "/nonexistent2"

# ============================================================
# 8. 条件检查与脚本安全
# ============================================================
echo ""
echo "--- 8. 条件检查与脚本安全 ---"

# 安全的文件操作示例
safe_read() {
    local file="$1"
    
    # 多重检查
    if [[ ! -e "$file" ]]; then
        echo "错误: 文件 '$file' 不存在" >&2
        return 1
    fi
    
    if [[ ! -f "$file" ]]; then
        echo "错误: '$file' 不是普通文件" >&2
        return 1
    fi
    
    if [[ ! -r "$file" ]]; then
        echo "错误: 没有权限读取 '$file'" >&2
        return 1
    fi
    
    if [[ ! -s "$file" ]]; then
        echo "警告: 文件 '$file' 为空" >&2
    fi
    
    echo "✓ 文件检查通过，可以安全读取"
    return 0
}

echo "安全读取检查演示:"
safe_read "/etc/passwd" && echo "  可以读取 /etc/passwd"
safe_read "/nonexistent" || echo "  无法读取 /nonexistent"

echo ""
echo "=== 文件测试示例完成 ==="

