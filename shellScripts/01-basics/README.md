# 第1章：Shell基础

> 本章介绍Shell脚本编程的基础知识，为后续章节打下坚实基础。

## 📋 本章概述

Shell是Linux系统中最重要的用户接口之一。通过Shell脚本，我们可以将一系列命令组织成程序，实现任务自动化。本章将介绍Bash Shell的核心语法。

## 🎯 学习目标

完成本章学习后，你将能够：

- 编写并执行Shell脚本
- 使用变量存储和操作数据
- 使用条件语句进行分支控制
- 使用循环处理重复任务
- 定义和调用函数

---

## 1.1 第一个Shell脚本

### Shebang（释伴）

每个Shell脚本的第一行应该是**Shebang**，它告诉系统使用哪个解释器执行脚本：

```bash
#!/bin/bash
```

常见的Shebang：

| Shebang | 说明 |
|---------|------|
| `#!/bin/bash` | 使用Bash解释器 |
| `#!/bin/sh` | 使用系统默认Shell |
| `#!/usr/bin/env bash` | 在PATH中查找bash（更具可移植性） |

### 创建和执行脚本

```bash
# 1. 创建脚本文件
touch hello.sh

# 2. 编辑脚本（添加内容）
echo '#!/bin/bash' > hello.sh
echo 'echo "Hello, World!"' >> hello.sh

# 3. 添加执行权限
chmod +x hello.sh

# 4. 执行脚本（三种方式）
./hello.sh          # 方式1：直接执行（需要执行权限）
bash hello.sh       # 方式2：通过bash执行（不需要执行权限）
source hello.sh     # 方式3：在当前Shell中执行
```

> 💡 **提示**：`source`或`.`命令会在当前Shell环境中执行脚本，脚本中的变量和函数定义会保留在当前环境中。

### 脚本注释

```bash
# 这是单行注释

: '
这是多行注释的一种方式
可以写很多行
'
```

### 严格模式

在脚本开头添加以下设置，可以让脚本更加健壮：

```bash
#!/bin/bash
set -euo pipefail

# set -e: 命令失败时立即退出
# set -u: 使用未定义变量时报错
# set -o pipefail: 管道中任何命令失败则整个管道失败
```

📄 **示例脚本**: [01-hello.sh](01-hello.sh)

---

## 1.2 变量

### 变量定义与使用

```bash
# 定义变量（等号两边不能有空格！）
name="Linux"
count=42

# 使用变量（$符号或${}）
echo $name
echo ${name}
echo "Welcome to ${name} world"

# 推荐使用 ${} 形式，避免歧义
file="log"
echo "${file}_backup"   # 正确：log_backup
echo "$file_backup"     # 错误：尝试访问变量file_backup
```

### 变量类型

Shell中的变量默认都是**字符串**，但可以进行数值运算：

```bash
# 字符串
str="Hello"

# 数值运算
a=10
b=20
sum=$((a + b))        # 算术扩展
echo "Sum: $sum"      # 输出: Sum: 30

# 声明整数变量
declare -i num=100
num=num+50            # 可以直接运算
echo $num             # 输出: 150
```

### 环境变量

```bash
# 查看环境变量
echo $HOME            # 用户主目录
echo $PATH            # 可执行文件搜索路径
echo $USER            # 当前用户名
echo $PWD             # 当前工作目录
echo $SHELL           # 当前Shell

# 导出变量为环境变量（子进程可继承）
export MY_VAR="value"

# 临时设置环境变量运行命令
MY_VAR="value" ./script.sh
```

### 特殊变量

| 变量 | 含义 |
|------|------|
| `$0` | 脚本名称 |
| `$1`-`$9` | 位置参数（第1-9个参数） |
| `${10}` | 第10个及以后的参数 |
| `$#` | 参数个数 |
| `$@` | 所有参数（作为独立字符串） |
| `$*` | 所有参数（作为单个字符串） |
| `$?` | 上一条命令的退出状态 |
| `$$` | 当前脚本的PID |
| `$!` | 最近一个后台进程的PID |

### 字符串操作

```bash
str="Hello, World!"

# 获取长度
echo ${#str}                  # 输出: 13

# 截取子串
echo ${str:0:5}               # 输出: Hello（从位置0开始，取5个字符）
echo ${str:7}                 # 输出: World!（从位置7到末尾）

# 替换
echo ${str/World/Linux}       # 输出: Hello, Linux!（替换第一个匹配）
echo ${str//o/O}              # 输出: HellO, WOrld!（替换所有匹配）

# 删除匹配
filename="archive.tar.gz"
echo ${filename%.gz}          # 输出: archive.tar（删除最短后缀匹配）
echo ${filename%%.*}          # 输出: archive（删除最长后缀匹配）
echo ${filename#*.}           # 输出: tar.gz（删除最短前缀匹配）
echo ${filename##*.}          # 输出: gz（删除最长前缀匹配）

# 默认值
echo ${undefined_var:-"default"}    # 变量未定义时使用默认值
echo ${undefined_var:="default"}    # 变量未定义时设置并使用默认值
```

📄 **示例脚本**: [02-variables.sh](02-variables.sh)

---

## 1.3 条件判断

### if语句

```bash
if [ condition ]; then
    # 条件为真时执行
    commands
elif [ other_condition ]; then
    # 其他条件为真时执行
    commands
else
    # 所有条件都为假时执行
    commands
fi
```

### 测试条件

#### 文件测试

| 操作符 | 说明 |
|--------|------|
| `-e file` | 文件存在 |
| `-f file` | 是普通文件 |
| `-d file` | 是目录 |
| `-r file` | 可读 |
| `-w file` | 可写 |
| `-x file` | 可执行 |
| `-s file` | 文件大小大于0 |
| `-L file` | 是符号链接 |

#### 字符串测试

| 操作符 | 说明 |
|--------|------|
| `-z str` | 字符串为空 |
| `-n str` | 字符串非空 |
| `str1 = str2` | 字符串相等 |
| `str1 != str2` | 字符串不等 |

#### 数值比较

| 操作符 | 说明 |
|--------|------|
| `-eq` | 等于 (equal) |
| `-ne` | 不等于 (not equal) |
| `-lt` | 小于 (less than) |
| `-le` | 小于等于 (less or equal) |
| `-gt` | 大于 (greater than) |
| `-ge` | 大于等于 (greater or equal) |

### [ ] 与 [[ ]] 的区别

```bash
# [ ] 是传统测试命令（POSIX兼容）
if [ "$str" = "hello" ]; then
    echo "Match"
fi

# [[ ]] 是Bash扩展（更强大，推荐使用）
if [[ $str == "hello" ]]; then
    echo "Match"
fi

# [[ ]] 支持正则匹配
if [[ $str =~ ^[0-9]+$ ]]; then
    echo "Is a number"
fi

# [[ ]] 支持模式匹配
if [[ $file == *.txt ]]; then
    echo "Is a text file"
fi
```

> ⚠️ **注意**：使用`[ ]`时，变量要加双引号防止空值错误；`[[ ]]`则不需要（但加上是好习惯）。

### 逻辑运算

```bash
# 与运算
if [[ condition1 && condition2 ]]; then
    commands
fi

# 或运算
if [[ condition1 || condition2 ]]; then
    commands
fi

# 非运算
if [[ ! condition ]]; then
    commands
fi

# 使用 [ ] 时的逻辑运算
if [ condition1 ] && [ condition2 ]; then
    commands
fi
```

### case语句

```bash
case $variable in
    pattern1)
        commands1
        ;;
    pattern2|pattern3)
        commands2
        ;;
    *)
        default_commands
        ;;
esac
```

示例：

```bash
case $1 in
    start)
        echo "Starting service..."
        ;;
    stop)
        echo "Stopping service..."
        ;;
    restart)
        echo "Restarting service..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

📄 **示例脚本**: [03-conditions.sh](03-conditions.sh)

---

## 1.4 循环结构

### for循环

```bash
# 遍历列表
for item in item1 item2 item3; do
    echo $item
done

# 遍历数组
arr=("apple" "banana" "cherry")
for fruit in "${arr[@]}"; do
    echo $fruit
done

# 遍历文件
for file in *.txt; do
    echo "Processing: $file"
done

# C风格for循环
for ((i=0; i<10; i++)); do
    echo $i
done

# 遍历数字范围
for i in {1..5}; do
    echo $i
done

# 带步长的范围
for i in {0..10..2}; do
    echo $i   # 输出: 0 2 4 6 8 10
done

# 使用seq命令
for i in $(seq 1 5); do
    echo $i
done
```

### while循环

```bash
# 基本while循环
count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    ((count++))
done

# 读取文件行
while IFS= read -r line; do
    echo "Line: $line"
done < filename.txt

# 无限循环
while true; do
    echo "Running..."
    sleep 1
done
```

### until循环

```bash
# until: 条件为假时执行（与while相反）
count=0
until [ $count -ge 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

### 循环控制

```bash
# break: 跳出循环
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done

# continue: 跳过当前迭代
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        continue
    fi
    echo $i   # 输出: 1 2 4 5
done

# break n: 跳出n层循环
for i in {1..3}; do
    for j in {1..3}; do
        if [ $j -eq 2 ]; then
            break 2   # 跳出两层循环
        fi
        echo "$i-$j"
    done
done
```

📄 **示例脚本**: [04-loops.sh](04-loops.sh)

---

## 1.5 函数

### 函数定义

```bash
# 方式1（推荐）
function_name() {
    commands
}

# 方式2
function function_name {
    commands
}
```

### 函数调用

```bash
# 定义函数
greet() {
    echo "Hello, $1!"
}

# 调用函数
greet "World"    # 输出: Hello, World!
greet "Linux"    # 输出: Hello, Linux!
```

### 函数参数

```bash
# 函数内使用 $1, $2, $@ 等访问参数
print_args() {
    echo "第一个参数: $1"
    echo "第二个参数: $2"
    echo "所有参数: $@"
    echo "参数个数: $#"
}

print_args "apple" "banana" "cherry"
```

### 返回值

```bash
# 方式1: 使用return返回状态码（0-255）
is_even() {
    if (( $1 % 2 == 0 )); then
        return 0   # 成功/真
    else
        return 1   # 失败/假
    fi
}

if is_even 4; then
    echo "4 is even"
fi

# 方式2: 使用echo输出结果（推荐用于返回数据）
get_sum() {
    local a=$1
    local b=$2
    echo $((a + b))
}

result=$(get_sum 10 20)
echo "Sum: $result"    # 输出: Sum: 30
```

### 局部变量

```bash
# 使用 local 声明局部变量
my_function() {
    local local_var="I am local"
    global_var="I am global"
    echo $local_var
}

my_function
echo $global_var     # 可以访问
echo $local_var      # 空（无法访问）
```

### 递归函数

```bash
# 计算阶乘
factorial() {
    local n=$1
    if [ $n -le 1 ]; then
        echo 1
    else
        local sub=$(factorial $((n - 1)))
        echo $((n * sub))
    fi
}

echo "5! = $(factorial 5)"    # 输出: 5! = 120
```

📄 **示例脚本**: [05-functions.sh](05-functions.sh)

---

## 1.6 数组

### 索引数组

```bash
# 定义数组
arr=("apple" "banana" "cherry")

# 或者逐个赋值
arr[0]="apple"
arr[1]="banana"
arr[2]="cherry"

# 访问元素
echo ${arr[0]}        # 第一个元素
echo ${arr[@]}        # 所有元素
echo ${arr[*]}        # 所有元素（作为单个字符串）
echo ${#arr[@]}       # 数组长度
echo ${!arr[@]}       # 所有索引

# 切片
echo ${arr[@]:1:2}    # 从索引1开始，取2个元素

# 添加元素
arr+=("date")

# 删除元素
unset arr[1]
```

### 关联数组（字典）

```bash
# 声明关联数组（必须先声明）
declare -A user

# 赋值
user[name]="John"
user[age]=30
user[email]="john@example.com"

# 或者一次性定义
declare -A config=(
    [host]="localhost"
    [port]="8080"
    [debug]="true"
)

# 访问
echo ${user[name]}
echo ${config[port]}

# 遍历
for key in "${!user[@]}"; do
    echo "$key: ${user[$key]}"
done
```

---

## 📝 快速参考

### 运算符速查

| 类型 | 语法 | 示例 |
|------|------|------|
| 算术运算 | `$(( ))` | `$((a + b))` |
| 算术运算 | `let` | `let "a = a + 1"` |
| 算术运算 | `expr` | `expr $a + $b` |
| 条件测试 | `[ ]` | `[ $a -eq $b ]` |
| 扩展测试 | `[[ ]]` | `[[ $a == $b ]]` |
| 算术测试 | `(( ))` | `(( a > b ))` |

### 常用快捷操作

```bash
# 自增自减
((count++))
((count--))
((count += 5))

# 三元运算
result=$(( a > b ? a : b ))

# 命令替换
today=$(date +%Y-%m-%d)

# 默认值
name=${1:-"default"}
```

---

## 📂 本章示例文件

| 文件 | 说明 |
|------|------|
| [01-hello.sh](01-hello.sh) | Hello World与脚本基础 |
| [02-variables.sh](02-variables.sh) | 变量定义与操作 |
| [03-conditions.sh](03-conditions.sh) | 条件判断示例 |
| [04-loops.sh](04-loops.sh) | 循环结构示例 |
| [05-functions.sh](05-functions.sh) | 函数定义与使用 |

---

## 🎯 练习建议

1. **Hello World扩展**：修改`01-hello.sh`，接受用户名参数并个性化问候
2. **变量练习**：创建脚本，接收两个数字参数并输出它们的和、差、积、商
3. **条件判断**：编写脚本判断一个数是正数、负数还是零
4. **循环练习**：使用循环打印九九乘法表
5. **函数练习**：编写一个函数，判断输入是否为素数

---

[下一章：文件与目录操作 →](../02-file-operations/README.md)

