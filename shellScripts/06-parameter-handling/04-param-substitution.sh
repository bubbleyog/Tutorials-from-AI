#!/bin/bash
#
# 脚本名称: 04-param-substitution.sh
# 描述: 参数替换与模板渲染：默认值/必填检查/字符串替换/截取，envsubst或sed
# 用法: ./04-param-substitution.sh
#

set -euo pipefail

echo "=== 参数替换与模板渲染示例 ==="
echo ""

# ============================================================
# 1. 默认值、赋值、必填检查
# ============================================================
echo "--- 1. 默认值、赋值、必填检查 ---"

unset DEMO_VAR || true
empty_var=""

# ${var:-default} 未定义或为空时使用默认值（不修改var）
echo "DEMO_VAR(default): ${DEMO_VAR:-default_value}"

# ${var:=default} 未定义或为空时设置var为默认值
: ${DEMO_VAR:="now_set"}
echo "DEMO_VAR(after :=): $DEMO_VAR"

# ${var:+value} var已定义且非空时使用value
non_empty="x"
echo "non_empty:+ => ${non_empty:+yes}"
echo "empty_var:+  => ${empty_var:+yes}"

# ${var:?message} var未定义或为空则报错退出（演示时注释掉）
# : ${REQUIRED:?"REQUIRED is missing"}

# ============================================================
# 2. 字符串操作（替换/截取/删除前后缀）
# ============================================================
echo ""
echo "--- 2. 字符串操作 ---"

s="archive.tar.gz"

echo "原始: $s"
echo "去掉最短后缀%.gz: ${s%.gz}"
echo "去掉最长后缀%%.*: ${s%%.*}"
echo "去掉最短前缀#*. : ${s#*.}"
echo "去掉最长前缀##*. : ${s##*.}"

t="Hello, World!"
echo "替换第一个匹配: ${t/World/Linux}"
echo "替换全部匹配: ${t//o/O}"

echo "子串(0,5): ${t:0:5}"
echo "子串(7..): ${t:7}"

# ============================================================
# 3. 模板渲染：envsubst 或 sed
# ============================================================
echo ""
echo "--- 3. 模板渲染：envsubst 或 sed ---"

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

tpl="$TEMP_DIR/config.tpl"
out="$TEMP_DIR/config.out"

cat >"$tpl" << 'EOF'
name=${APP_NAME}
port=${APP_PORT}
mode=${APP_MODE}
EOF

# 准备变量
APP_NAME=${APP_NAME:-"DemoApp"}
APP_PORT=${APP_PORT:-"8080"}
APP_MODE=${APP_MODE:-"dev"}
export APP_NAME APP_PORT APP_MODE

echo "模板文件: $tpl"
echo "渲染输出: $out"

echo ""
if command -v envsubst >/dev/null 2>&1; then
    echo "使用 envsubst 渲染..."
    envsubst <"$tpl" >"$out"
else
    echo "未找到 envsubst，使用 sed 渲染（仅演示最常见的${VAR}替换）..."
    sed \
        -e "s|\${APP_NAME}|${APP_NAME}|g" \
        -e "s|\${APP_PORT}|${APP_PORT}|g" \
        -e "s|\${APP_MODE}|${APP_MODE}|g" \
        "$tpl" >"$out"
fi

echo "渲染结果:"
cat "$out"
