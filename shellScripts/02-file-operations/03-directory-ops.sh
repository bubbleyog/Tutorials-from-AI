#!/bin/bash
#
# 脚本名称: 03-directory-ops.sh
# 描述: 目录操作与遍历示例
# 用法: ./03-directory-ops.sh
#

set -euo pipefail

echo "=== 目录操作与遍历示例 ==="
echo ""

# 创建临时工作目录
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

echo "工作目录: $WORK_DIR"
echo ""

# ============================================================
# 1. 创建测试目录结构
# ============================================================
echo "--- 1. 创建测试目录结构 ---"

# 创建多级目录
mkdir -p "$WORK_DIR/project/src/main"
mkdir -p "$WORK_DIR/project/src/test"
mkdir -p "$WORK_DIR/project/docs"
mkdir -p "$WORK_DIR/project/data/raw"
mkdir -p "$WORK_DIR/project/data/processed"
mkdir -p "$WORK_DIR/project/logs"

# 创建测试文件
echo "print('hello')" > "$WORK_DIR/project/src/main/app.py"
echo "import unittest" > "$WORK_DIR/project/src/test/test_app.py"
echo "# README" > "$WORK_DIR/project/docs/README.md"
echo "API文档" > "$WORK_DIR/project/docs/api.md"
echo "1,2,3" > "$WORK_DIR/project/data/raw/data1.csv"
echo "4,5,6" > "$WORK_DIR/project/data/raw/data2.csv"
echo "processed" > "$WORK_DIR/project/data/processed/output.csv"
echo "log entry" > "$WORK_DIR/project/logs/app.log"
echo "old log" > "$WORK_DIR/project/logs/app.log.old"
touch "$WORK_DIR/project/logs/empty.log"

# 创建一些临时文件
touch "$WORK_DIR/project/src/main/temp.pyc"
touch "$WORK_DIR/project/src/main/.hidden"

echo "目录结构创建完成"
echo ""

# 显示目录树
echo "目录结构:"
if command -v tree &>/dev/null; then
    tree "$WORK_DIR/project"
else
    find "$WORK_DIR/project" -print | sed 's|'"$WORK_DIR/project"'|.|' | sort
fi

# ============================================================
# 2. 基本目录操作
# ============================================================
echo ""
echo "--- 2. 基本目录操作 ---"

echo ""
echo "列出目录内容:"
ls -la "$WORK_DIR/project/src/main/"

echo ""
echo "只列出目录:"
find "$WORK_DIR/project" -maxdepth 2 -type d | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "只列出文件:"
ls "$WORK_DIR/project/docs/"

# ============================================================
# 3. find 命令 - 按名称查找
# ============================================================
echo ""
echo "--- 3. find - 按名称查找 ---"

echo ""
echo "查找所有 .py 文件:"
find "$WORK_DIR/project" -name "*.py" | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "查找所有 .md 文件:"
find "$WORK_DIR/project" -name "*.md" | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "查找所有 .log 或 .csv 文件:"
find "$WORK_DIR/project" \( -name "*.log" -o -name "*.csv" \) | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "忽略大小写查找 (iname):"
touch "$WORK_DIR/project/docs/Notes.MD"
find "$WORK_DIR/project" -iname "*.md" | sed 's|'"$WORK_DIR/project"'|.|'

# ============================================================
# 4. find 命令 - 按类型和属性查找
# ============================================================
echo ""
echo "--- 4. find - 按类型和属性查找 ---"

echo ""
echo "只查找目录:"
find "$WORK_DIR/project" -type d | wc -l
echo "共有 $(find "$WORK_DIR/project" -type d | wc -l) 个目录"

echo ""
echo "只查找普通文件:"
echo "共有 $(find "$WORK_DIR/project" -type f | wc -l) 个文件"

echo ""
echo "查找空文件:"
find "$WORK_DIR/project" -type f -empty | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "查找空目录:"
mkdir "$WORK_DIR/project/empty_dir"
find "$WORK_DIR/project" -type d -empty | sed 's|'"$WORK_DIR/project"'|.|'

# ============================================================
# 5. find 命令 - 按大小查找
# ============================================================
echo ""
echo "--- 5. find - 按大小查找 ---"

# 创建不同大小的文件
dd if=/dev/zero of="$WORK_DIR/project/data/large.bin" bs=1024 count=100 2>/dev/null
dd if=/dev/zero of="$WORK_DIR/project/data/small.bin" bs=10 count=1 2>/dev/null

echo "查找大于50KB的文件:"
find "$WORK_DIR/project" -type f -size +50k -exec ls -lh {} \; 2>/dev/null | awk '{print $NF, $5}'

echo ""
echo "查找小于100字节的文件:"
find "$WORK_DIR/project" -type f -size -100c | wc -l
echo "共有 $(find "$WORK_DIR/project" -type f -size -100c | wc -l) 个小于100字节的文件"

# ============================================================
# 6. find 命令 - 排除目录
# ============================================================
echo ""
echo "--- 6. find - 排除目录 ---"

echo ""
echo "查找 .py 文件，排除 test 目录:"
find "$WORK_DIR/project" -path "*/test/*" -prune -o -name "*.py" -print | \
    grep -v "test" | sed 's|'"$WORK_DIR/project"'|.|'

echo ""
echo "排除隐藏文件:"
find "$WORK_DIR/project" -type f ! -name ".*" | wc -l
echo "共有 $(find "$WORK_DIR/project" -type f ! -name ".*" | wc -l) 个非隐藏文件"

# ============================================================
# 7. find 命令 - 执行操作
# ============================================================
echo ""
echo "--- 7. find - 执行操作 ---"

echo ""
echo "使用 -exec 显示文件详情:"
find "$WORK_DIR/project/docs" -name "*.md" -exec ls -l {} \;

echo ""
echo "使用 -exec 统计行数:"
find "$WORK_DIR/project" -name "*.py" -exec wc -l {} \;

echo ""
echo "使用 xargs 批量处理:"
echo "所有Python文件的内容:"
find "$WORK_DIR/project" -name "*.py" -print0 | xargs -0 cat

# ============================================================
# 8. 目录遍历 - for循环
# ============================================================
echo ""
echo "--- 8. 目录遍历 - for循环 ---"

echo ""
echo "遍历目录中的文件:"
for file in "$WORK_DIR/project/docs"/*; do
    if [[ -f "$file" ]]; then
        echo "  文件: $(basename "$file")"
    fi
done

echo ""
echo "使用通配符遍历特定类型:"
for pyfile in "$WORK_DIR/project"/src/*/*.py; do
    if [[ -f "$pyfile" ]]; then
        echo "  Python文件: $(basename "$pyfile") - $(wc -l < "$pyfile") 行"
    fi
done

# ============================================================
# 9. 目录遍历 - 递归函数
# ============================================================
echo ""
echo "--- 9. 目录遍历 - 递归函数 ---"

traverse_directory() {
    local dir="$1"
    local indent="${2:-}"
    
    for item in "$dir"/*; do
        [[ -e "$item" ]] || continue
        
        local name=$(basename "$item")
        
        if [[ -d "$item" ]]; then
            echo "${indent}📁 $name/"
            traverse_directory "$item" "  $indent"
        else
            local size=$(stat -c %s "$item" 2>/dev/null || stat -f %z "$item" 2>/dev/null)
            echo "${indent}📄 $name ($size bytes)"
        fi
    done
}

echo "递归遍历目录树:"
traverse_directory "$WORK_DIR/project/src"

# ============================================================
# 10. globstar - 递归通配符
# ============================================================
echo ""
echo "--- 10. globstar - 递归通配符 ---"

# 启用 globstar
shopt -s globstar

echo "使用 ** 递归匹配所有 .csv 文件:"
for file in "$WORK_DIR/project"/**/*.csv; do
    [[ -f "$file" ]] && echo "  $(basename "$file")"
done

echo ""
echo "使用 ** 递归匹配所有 .py 文件:"
for file in "$WORK_DIR/project"/**/*.py; do
    [[ -f "$file" ]] && echo "  $(basename "$file")"
done

# ============================================================
# 11. 实用示例 - 批量文件操作
# ============================================================
echo ""
echo "--- 11. 实用示例 - 批量文件操作 ---"

echo ""
echo "批量重命名 .log.old 为 .log.bak:"
for file in "$WORK_DIR/project"/**/*.old; do
    if [[ -f "$file" ]]; then
        new_name="${file%.old}.bak"
        mv "$file" "$new_name"
        echo "  重命名: $(basename "$file") -> $(basename "$new_name")"
    fi
done

echo ""
echo "删除所有 .pyc 文件:"
find "$WORK_DIR/project" -name "*.pyc" -type f -print -delete

echo ""
echo "复制所有 .md 文件到新目录:"
mkdir -p "$WORK_DIR/project/backup/docs"
find "$WORK_DIR/project/docs" -name "*.md" -exec cp {} "$WORK_DIR/project/backup/docs/" \;
echo "已复制 $(ls "$WORK_DIR/project/backup/docs" | wc -l) 个文件"

# ============================================================
# 12. 实用示例 - 目录统计
# ============================================================
echo ""
echo "--- 12. 实用示例 - 目录统计 ---"

dir_stats() {
    local dir="$1"
    
    local total_files=$(find "$dir" -type f | wc -l)
    local total_dirs=$(find "$dir" -type d | wc -l)
    local total_size=$(du -sh "$dir" 2>/dev/null | cut -f1)
    
    echo "目录统计: $dir"
    echo "  文件数: $total_files"
    echo "  目录数: $total_dirs"
    echo "  总大小: $total_size"
    
    echo "  文件类型分布:"
    find "$dir" -type f -name "*.*" | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -5 | \
        while read count ext; do
            printf "    .%-6s %d\n" "$ext" "$count"
        done
}

dir_stats "$WORK_DIR/project"

# ============================================================
# 13. 实用示例 - 查找大文件
# ============================================================
echo ""
echo "--- 13. 实用示例 - 查找大文件 ---"

find_large_files() {
    local dir="$1"
    local min_size="${2:-1M}"
    
    echo "查找大于 $min_size 的文件:"
    find "$dir" -type f -size +"$min_size" -exec ls -lh {} \; 2>/dev/null | \
        awk '{printf "  %s %s\n", $5, $NF}'
}

find_large_files "$WORK_DIR/project" "10k"

# ============================================================
# 14. 实用示例 - 清理临时文件
# ============================================================
echo ""
echo "--- 14. 实用示例 - 清理临时文件 ---"

cleanup_temp_files() {
    local dir="$1"
    local patterns=("*.tmp" "*.temp" "*.pyc" "*.pyo" "__pycache__" ".DS_Store" "*.swp")
    local count=0
    
    echo "清理临时文件..."
    
    for pattern in "${patterns[@]}"; do
        while IFS= read -r -d '' file; do
            echo "  删除: $file"
            rm -rf "$file"
            ((count++))
        done < <(find "$dir" -name "$pattern" -print0 2>/dev/null)
    done
    
    echo "共清理 $count 个临时文件/目录"
}

# 创建一些临时文件用于演示
touch "$WORK_DIR/project/temp.tmp"
touch "$WORK_DIR/project/cache.temp"

cleanup_temp_files "$WORK_DIR/project"

# ============================================================
# 15. 实用示例 - 项目文件汇总
# ============================================================
echo ""
echo "--- 15. 实用示例 - 项目文件汇总 ---"

project_summary() {
    local dir="$1"
    
    echo "=================================="
    echo "项目结构汇总"
    echo "=================================="
    
    # 源代码统计
    echo ""
    echo "源代码文件:"
    for ext in py js ts cpp c h java go rs; do
        local count=$(find "$dir" -name "*.$ext" -type f 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
            local lines=$(find "$dir" -name "*.$ext" -type f -exec cat {} \; 2>/dev/null | wc -l)
            printf "  .%-6s %3d 个文件, %5d 行代码\n" "$ext" "$count" "$lines"
        fi
    done
    
    # 文档统计
    echo ""
    echo "文档文件:"
    for ext in md txt rst doc; do
        local count=$(find "$dir" -name "*.$ext" -type f 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
            printf "  .%-6s %3d 个文件\n" "$ext" "$count"
        fi
    done
    
    # 数据文件统计
    echo ""
    echo "数据文件:"
    for ext in csv json xml yaml yml; do
        local count=$(find "$dir" -name "*.$ext" -type f 2>/dev/null | wc -l)
        if [[ $count -gt 0 ]]; then
            printf "  .%-6s %3d 个文件\n" "$ext" "$count"
        fi
    done
    
    echo "=================================="
}

project_summary "$WORK_DIR/project"

echo ""
echo "=== 目录操作与遍历示例完成 ==="

