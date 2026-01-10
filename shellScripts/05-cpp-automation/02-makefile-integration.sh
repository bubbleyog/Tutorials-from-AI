#!/bin/bash
#
# 脚本名称: 02-makefile-integration.sh
# 描述: Makefile集成示例：生成最小Makefile、调用make、覆盖变量
# 用法: ./02-makefile-integration.sh
#

set -euo pipefail

echo "=== Makefile 集成示例 ==="
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CPP_SRC="$SCRIPT_DIR/sample.cpp"
BUILD_DIR="$SCRIPT_DIR/build-make"
mkdir -p "$BUILD_DIR"

if ! command -v make >/dev/null 2>&1; then
    echo "未找到 make，请先安装 make" >&2
    exit 1
fi

# 选择默认编译器（可被 make CXX= 覆盖）
DEFAULT_CXX="g++"
if ! command -v g++ >/dev/null 2>&1 && command -v clang++ >/dev/null 2>&1; then
    DEFAULT_CXX="clang++"
fi

MAKEFILE="$BUILD_DIR/Makefile"
cat >"$MAKEFILE" << 'EOF'
# 最小Makefile：用于演示 make 与脚本集成

CXX ?= g++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra

SRC := sample.cpp
BIN := sample_app

.PHONY: all clean run

all: $(BIN)

$(BIN): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

run: $(BIN)
	./$(BIN) --name MakeUser --seed 42

clean:
	rm -f $(BIN)
EOF

# 把源码复制到build目录，保证Makefile自包含
cp -f "$CPP_SRC" "$BUILD_DIR/sample.cpp"

# ============================================================
# 1. 默认构建与运行
# ============================================================
echo "--- 1. 默认构建与运行 ---"

pushd "$BUILD_DIR" >/dev/null
make -j
make run
popd >/dev/null

# ============================================================
# 2. 覆盖变量（编译器与编译选项）
# ============================================================
echo ""
echo "--- 2. 覆盖变量（CXX/CXXFLAGS） ---"

# 尝试用clang++（如果存在）
if command -v clang++ >/dev/null 2>&1; then
    echo "使用 clang++ + -O3 重新构建并运行"
    pushd "$BUILD_DIR" >/dev/null
    make clean
    make -j CXX=clang++ CXXFLAGS="-std=c++17 -O3 -Wall -Wextra"
    ./sample_app --name Clang --seed 7
    popd >/dev/null
else
    echo "当前环境未安装 clang++，跳过clang++演示"
fi

# ============================================================
# 3. 清理
# ============================================================
echo ""
echo "--- 3. 清理 ---"

echo "可运行以下命令清理构建产物:"
echo "  (cd $BUILD_DIR && make clean)"
