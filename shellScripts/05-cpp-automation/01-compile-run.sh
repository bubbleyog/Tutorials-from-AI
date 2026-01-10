#!/bin/bash
#
# 脚本名称: 01-compile-run.sh
# 描述: C++程序的编译与运行：编译器选择、编译选项、退出码与日志
# 用法: ./01-compile-run.sh
#

set -euo pipefail

echo "=== C++ 编译与运行示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CPP_SRC="$SCRIPT_DIR/sample.cpp"
BUILD_DIR="$SCRIPT_DIR/build"
mkdir -p "$BUILD_DIR"

# ============================================================
# 1. 选择编译器
# ============================================================
echo "--- 1. 选择编译器 ---"

CXX=${CXX:-""}
if [[ -z "$CXX" ]]; then
    if command -v g++ >/dev/null 2>&1; then
        CXX="g++"
    elif command -v clang++ >/dev/null 2>&1; then
        CXX="clang++"
    else
        echo "未找到C++编译器（g++/clang++）" >&2
        echo "请安装编译器，或设置环境变量 CXX 指向编译器路径" >&2
        exit 1
    fi
fi

echo "使用编译器: $CXX"
"$CXX" --version | head -n 2

# ============================================================
# 2. 编译（可通过环境变量覆盖编译选项）
# ============================================================
echo ""
echo "--- 2. 编译 ---"

CXXFLAGS=${CXXFLAGS:-"-std=c++17 -O2 -Wall -Wextra"}
OUT_BIN="$BUILD_DIR/sample_app"

# 简单的增量策略：源文件比产物新才重新编译
need_build=1
if [[ -f "$OUT_BIN" ]] && [[ "$CPP_SRC" -ot "$OUT_BIN" ]]; then
    need_build=0
fi

if [[ $need_build -eq 1 ]]; then
    echo "编译命令: $CXX $CXXFLAGS -o $OUT_BIN $CPP_SRC"
    "$CXX" $CXXFLAGS -o "$OUT_BIN" "$CPP_SRC"
else
    echo "产物已是最新，跳过编译: $OUT_BIN"
fi

# ============================================================
# 3. 运行与退出码
# ============================================================
echo ""
echo "--- 3. 运行与退出码 ---"

"$OUT_BIN" --name "Alice" --seed 1

set +e
"$OUT_BIN" --fail
rc=$?
set -e

echo "失败示例退出码: $rc"

# ============================================================
# 4. 日志重定向（stdout/stderr）
# ============================================================
echo ""
echo "--- 4. 日志重定向（stdout/stderr） ---"

LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

stdout_log="$LOG_DIR/app_stdout.log"
stderr_log="$LOG_DIR/app_stderr.log"
combined_log="$LOG_DIR/app_combined.log"

"$OUT_BIN" --name "LogDemo" --seed 10 >"$stdout_log" 2>"$stderr_log"

# 合并日志（追加）
"$OUT_BIN" --name "Combined" --seed 11 >>"$combined_log" 2>&1
set +e
"$OUT_BIN" --fail >>"$combined_log" 2>&1
set -e

echo "stdout日志: $stdout_log"
echo "stderr日志: $stderr_log"
echo "合并日志:  $combined_log"

echo ""
echo "完成。"
