#!/bin/bash

# 这是一个基础的 Shell 脚本示例
# 第一行 (Shebang) 告诉系统用哪个解释器来运行这个脚本，这里是 /bin/bash

# 1. 打印信息到屏幕
echo "Hello, HPC World!"
echo "Today is $(date)"

# 2. 定义变量
MY_NAME="Researcher"
WORK_DIR=$(pwd) # 获取当前路径

echo "User: $MY_NAME"
echo "Current Directory: $WORK_DIR"

# 3. 简单的循环
echo "Counting files..."
for i in {1..3}; do
    echo "Processing file_$i.dat..."
    # sleep 1 # 暂停1秒，模拟处理过程
done

echo "Done!"
