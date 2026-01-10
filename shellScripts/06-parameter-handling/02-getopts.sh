#!/bin/bash
#
# 脚本名称: 02-getopts.sh
# 描述: 使用 getopts 解析短选项（-i/-o/-n/-v/-h），并处理错误与usage
# 用法:
#   ./02-getopts.sh -i input.txt -o output.txt -n 3 -v
#   ./02-getopts.sh -h
#

set -euo pipefail

usage() {
    cat << 'EOF'
用法:
  ./02-getopts.sh -i <input> -o <output> [-n <num>] [-v] [-h]

选项:
  -i <input>   输入文件路径（必填）
  -o <output>  输出文件路径（必填）
  -n <num>     处理次数（默认: 1）
  -v           详细模式
  -h           显示帮助

示例:
  ./02-getopts.sh -i data.txt -o out.txt -n 2 -v
EOF
}

echo "=== getopts 短选项解析示例 ==="
echo ""

input=""
output=""
num=1
verbose=0

# 选项字符串说明：
# - 以 ':' 开头：让getopts在遇到缺参时把opt设为 ':' 并把OPTARG设为缺参的选项
# - 某个选项后跟 ':'：表示该选项需要参数
while getopts ":i:o:n:vh" opt; do
    case "$opt" in
        i)
            input="$OPTARG"
            ;;
        o)
            output="$OPTARG"
            ;;
        n)
            num="$OPTARG"
            ;;
        v)
            verbose=1
            ;;
        h)
            usage
            exit 0
            ;;
        :)  # 缺少参数
            echo "选项 -$OPTARG 缺少参数" >&2
            usage >&2
            exit 2
            ;;
        \?)
            echo "未知选项: -$OPTARG" >&2
            usage >&2
            exit 2
            ;;
    esac

done

# 移除已解析的选项，剩余的是位置参数
shift $((OPTIND - 1))

# 校验必填参数
if [[ -z "$input" || -z "$output" ]]; then
    echo "-i 与 -o 为必填参数" >&2
    usage >&2
    exit 2
fi

# 校验 -n 是否为正整数
if ! [[ "$num" =~ ^[0-9]+$ ]] || [[ "$num" -lt 1 ]]; then
    echo "-n 必须是 >=1 的整数: $num" >&2
    exit 2
fi

# ============================================================
# 执行逻辑（演示用）
# ============================================================
echo "--- 解析结果 ---"
echo "input : $input"
echo "output: $output"
echo "num   : $num"
echo "verbose: $verbose"

echo ""
echo "--- 剩余位置参数（shift后） ---"
if [[ $# -eq 0 ]]; then
    echo "(无)"
else
    idx=0
    for a in "$@"; do
        idx=$((idx + 1))
        echo "  [$idx] = '$a'"
    done
fi

# 模拟处理：把input内容复制/追加到output
# 为了可运行，若input不存在则生成一个示例文件
if [[ ! -f "$input" ]]; then
    echo "输入文件不存在，生成示例文件: $input"
    mkdir -p "$(dirname "$input")" 2>/dev/null || true
    cat >"$input" << 'EOF'
line1
line2
line3
EOF
fi

: >"$output"  # 清空输出

for ((i=1; i<=num; i++)); do
    if [[ $verbose -eq 1 ]]; then
        echo "第 $i 次处理..."
    fi
    cat "$input" >>"$output"
done

echo ""
echo "完成：已写入 $output"
