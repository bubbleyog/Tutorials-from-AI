#!/bin/bash
#
# 脚本名称: 03-config-files.sh
# 描述: 配置文件读取示例：.env / ini风格 key=value，以及可选JSON读取
# 用法: ./03-config-files.sh
#

set -euo pipefail

echo "=== 配置文件读取示例 ==="
echo ""

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

ENV_FILE="$TEMP_DIR/app.env"
INI_FILE="$TEMP_DIR/app.ini"
JSON_FILE="$TEMP_DIR/app.json"

# ============================================================
# 1. 生成示例配置文件
# ============================================================
echo "--- 1. 生成示例配置文件 ---"

cat >"$ENV_FILE" << 'EOF'
# .env风格（支持注释与空行）
APP_NAME=DemoApp
APP_PORT=8080
APP_DEBUG=true
# 值中包含空格时建议加引号（本示例解析会去掉外层引号）
APP_GREETING="hello world"
EOF

cat >"$INI_FILE" << 'EOF'
# ini风格（这里演示最简单的 key=value）
# 复杂ini(分节[section])通常需要更专门的解析器

timeout=30
retries=2
log_level=INFO
EOF

cat >"$JSON_FILE" << 'EOF'
{
  "dataset": "/data/train.csv",
  "epochs": 10,
  "lr": 0.001
}
EOF

echo "ENV:  $ENV_FILE"
echo "INI:  $INI_FILE"
echo "JSON: $JSON_FILE"

# ============================================================
# 2. 解析 key=value 文件（通用函数）
# ============================================================
echo ""
echo "--- 2. 解析 key=value（忽略注释/空行） ---"

# 解析规则（够用版本）：
# - 忽略空行、忽略以 # 开头的注释行
# - 允许 key = value 两侧有空格
# - 如果value被单引号/双引号包裹，去掉最外层引号
# - 只接受合法key（字母数字下划线，且不以数字开头）
load_kv_file() {
    local file="$1"

    while IFS= read -r raw || [[ -n "$raw" ]]; do
        # 去掉首尾空白
        line=$(echo "$raw" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

        # 空行/注释跳过
        [[ -z "$line" ]] && continue
        [[ "$line" == \#* ]] && continue

        # 只处理包含 '=' 的行
        if [[ "$line" != *"="* ]]; then
            continue
        fi

        key=${line%%=*}
        val=${line#*=}

        key=$(echo "$key" | sed -e 's/[[:space:]]*$//')
        val=$(echo "$val" | sed -e 's/^[[:space:]]*//')

        # key合法性检查
        if ! [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
            echo "跳过非法key: $key" >&2
            continue
        fi

        # 去掉最外层引号
        if [[ "$val" =~ ^\".*\"$ ]]; then
            val=${val:1:${#val}-2}
        elif [[ "$val" =~ ^\'.*\'$ ]]; then
            val=${val:1:${#val}-2}
        fi

        # 使用printf -v避免eval
        printf -v "$key" '%s' "$val"
        export "$key"
    done <"$file"
}

# 加载配置（会导出为环境变量）
load_kv_file "$ENV_FILE"
load_kv_file "$INI_FILE"

# 打印结果
echo "读取后的变量（部分）:"
echo "  APP_NAME=$APP_NAME"
echo "  APP_PORT=$APP_PORT"
echo "  APP_DEBUG=$APP_DEBUG"
echo "  APP_GREETING=$APP_GREETING"
echo "  timeout=$timeout"
echo "  retries=$retries"
echo "  log_level=$log_level"

# ============================================================
# 3. 可选：读取JSON（需要python3）
# ============================================================
echo ""
echo "--- 3. 可选：读取JSON（需要python3） ---"

if command -v python3 >/dev/null 2>&1; then
    json_line=$(python3 - "$JSON_FILE" << 'PY'
import json
import sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

dataset = data.get('dataset', '')
epochs = data.get('epochs', '')
lr = data.get('lr', '')

print(f"dataset={dataset}\tepochs={epochs}\tlr={lr}")
PY
)

    dataset=$(echo "$json_line" | awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^dataset=/){sub(/^dataset=/,"",$i); print $i; exit}}}')
    epochs=$(echo "$json_line" | awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^epochs=/){sub(/^epochs=/,"",$i); print $i; exit}}}')
    lr=$(echo "$json_line" | awk -F'\t' '{for(i=1;i<=NF;i++){if($i ~ /^lr=/){sub(/^lr=/,"",$i); print $i; exit}}}')

    echo "JSON读取结果:"
    echo "  dataset=$dataset"
    echo "  epochs=$epochs"
    echo "  lr=$lr"
else
    echo "未找到 python3，跳过JSON读取演示"
fi

# ============================================================
# 4. 配置优先级（常见约定）
# ============================================================
echo ""
echo "--- 4. 配置优先级：默认值 < 配置文件 < 环境变量 < 命令行参数 ---"

default_port=80
port_from_file=${APP_PORT:-""}
port_from_env=${APP_PORT_OVERRIDE:-""}

final_port="$default_port"
[[ -n "$port_from_file" ]] && final_port="$port_from_file"
[[ -n "$port_from_env" ]] && final_port="$port_from_env"

echo "default_port=$default_port"
echo "APP_PORT(from file)=$port_from_file"
echo "APP_PORT_OVERRIDE(from env, optional)=${APP_PORT_OVERRIDE:-<未设置>}"
echo "final_port=$final_port"
