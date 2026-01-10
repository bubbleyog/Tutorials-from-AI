#!/bin/bash
#
# 脚本名称: 02-venv-manage.sh
# 描述: Python venv 虚拟环境的创建、复用、无激活运行与清理
# 用法:
#   ./02-venv-manage.sh           # 创建/复用 .venv-demo 并运行示例
#   ./02-venv-manage.sh --clean   # 删除 .venv-demo
#

set -euo pipefail

echo "=== Python venv 虚拟环境管理示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PY_SCRIPT="$SCRIPT_DIR/sample.py"
VENV_DIR="$SCRIPT_DIR/.venv-demo"

if [[ ${1:-""} == "--clean" ]]; then
    echo "清理虚拟环境目录: $VENV_DIR"
    rm -rf "$VENV_DIR"
    echo "完成。"
    exit 0
fi

# ============================================================
# 1. 检查python3与venv模块
# ============================================================
echo "--- 1. 检查解释器与venv ---"

if ! command -v python3 >/dev/null 2>&1; then
    echo "未找到 python3，请先安装Python3" >&2
    exit 1
fi

echo "系统Python: $(command -v python3)"
python3 -V

# 检查是否支持 venv
set +e
python3 -m venv --help >/dev/null 2>&1
venv_ok=$?
set -e

if [[ $venv_ok -ne 0 ]]; then
    echo "当前Python缺少 venv 模块。" >&2
    echo "Debian/Ubuntu可尝试安装: sudo apt-get install python3-venv" >&2
    exit 1
fi

# ============================================================
# 2. 创建或复用虚拟环境
# ============================================================
echo ""
echo "--- 2. 创建或复用虚拟环境 ---"

if [[ ! -d "$VENV_DIR" ]]; then
    echo "创建虚拟环境: $VENV_DIR"
    python3 -m venv "$VENV_DIR"
else
    echo "复用已存在虚拟环境: $VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

if [[ ! -x "$VENV_PY" ]]; then
    echo "虚拟环境Python不存在或不可执行: $VENV_PY" >&2
    exit 1
fi

# ============================================================
# 3. 不激活也能运行（推荐给cron/systemd）
# ============================================================
echo ""
echo "--- 3. 不激活运行虚拟环境 ---"

echo "venv Python: $VENV_PY"
"$VENV_PY" -V

echo ""
echo "示例：用venv运行 sample.py"
APP_MODE="venv" APP_RUN_ID="venv-001" "$VENV_PY" "$PY_SCRIPT" --name "VenvUser" --seed 7

# ============================================================
# 4. 查看pip与已安装包（离线友好，不安装第三方依赖）
# ============================================================
echo ""
echo "--- 4. 查看pip与包列表 ---"

if [[ -x "$VENV_PIP" ]]; then
    "$VENV_PIP" --version
    echo "已安装包(前10行):"
    "$VENV_PIP" list | head -10
else
    echo "未找到pip：$VENV_PIP" >&2
fi

echo ""
echo "提示：清理虚拟环境可运行: ./02-venv-manage.sh --clean"
