# 第2章：文件与目录操作

> 本章介绍Shell脚本中的文件系统操作，包括文件测试、读写、文本处理和目录遍历。

## 📋 本章概述

文件操作是Shell脚本最常见的任务之一。无论是日志分析、配置管理还是批量文件处理，都离不开对文件系统的操作。本章将系统介绍这些核心技能。

## 🎯 学习目标

完成本章学习后，你将能够：

- 检测文件和目录的各种属性
- 读取和写入文件内容
- 使用grep、sed、awk处理文本
- 遍历目录和批量处理文件

---

## 2.1 文件测试

### 文件存在性与类型测试

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `-e file` | 文件存在（任意类型） | `[ -e /etc/passwd ]` |
| `-f file` | 是普通文件 | `[ -f config.txt ]` |
| `-d file` | 是目录 | `[ -d /home ]` |
| `-L file` | 是符号链接 | `[ -L /usr/bin/python ]` |
| `-b file` | 是块设备 | `[ -b /dev/sda ]` |
| `-c file` | 是字符设备 | `[ -c /dev/tty ]` |
| `-p file` | 是命名管道(FIFO) | `[ -p /tmp/mypipe ]` |
| `-S file` | 是套接字 | `[ -S /var/run/docker.sock ]` |

### 文件权限测试

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `-r file` | 可读 | `[ -r file.txt ]` |
| `-w file` | 可写 | `[ -w file.txt ]` |
| `-x file` | 可执行 | `[ -x script.sh ]` |
| `-u file` | 设置了SUID位 | `[ -u /usr/bin/passwd ]` |
| `-g file` | 设置了SGID位 | `[ -g /usr/bin/wall ]` |
| `-k file` | 设置了粘滞位 | `[ -k /tmp ]` |

### 文件属性测试

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `-s file` | 文件大小大于0 | `[ -s data.log ]` |
| `-O file` | 当前用户是文件所有者 | `[ -O myfile ]` |
| `-G file` | 当前用户属于文件所属组 | `[ -G groupfile ]` |
| `-N file` | 文件自上次读取后被修改 | `[ -N config ]` |

### 文件比较测试

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `file1 -nt file2` | file1 比 file2 新 | `[ a.txt -nt b.txt ]` |
| `file1 -ot file2` | file1 比 file2 旧 | `[ old.log -ot new.log ]` |
| `file1 -ef file2` | file1 和 file2 是同一文件（硬链接） | `[ a -ef b ]` |

### 示例代码

```bash
#!/bin/bash

file="/etc/passwd"

# 综合检查
if [[ -e "$file" ]]; then
    echo "文件存在"
    
    if [[ -f "$file" ]]; then
        echo "  - 是普通文件"
    elif [[ -d "$file" ]]; then
        echo "  - 是目录"
    fi
    
    [[ -r "$file" ]] && echo "  - 可读"
    [[ -w "$file" ]] && echo "  - 可写"
    [[ -x "$file" ]] && echo "  - 可执行"
    
    # 获取文件大小
    size=$(stat -c %s "$file" 2>/dev/null || stat -f %z "$file" 2>/dev/null)
    echo "  - 大小: $size 字节"
else
    echo "文件不存在"
fi
```

📄 **示例脚本**: [01-file-test.sh](01-file-test.sh)

---

## 2.2 文件读写

### 读取文件

#### 方法1：使用 `cat`

```bash
# 读取整个文件
content=$(cat file.txt)

# 显示文件内容
cat file.txt
```

#### 方法2：使用 `while read` 循环

```bash
# 逐行读取（推荐）
while IFS= read -r line; do
    echo "行: $line"
done < file.txt

# IFS= 保留行首空格
# -r 防止反斜杠转义
```

#### 方法3：使用 `readarray`/`mapfile`

```bash
# 读取到数组（Bash 4.0+）
readarray -t lines < file.txt

# 或者
mapfile -t lines < file.txt

# 遍历数组
for line in "${lines[@]}"; do
    echo "$line"
done
```

#### 方法4：读取特定行

```bash
# 第N行
sed -n '5p' file.txt

# 第M到N行
sed -n '5,10p' file.txt

# 最后N行
tail -n 5 file.txt

# 前N行
head -n 5 file.txt
```

### 写入文件

#### 重定向操作符

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `>` | 覆盖写入 | `echo "text" > file.txt` |
| `>>` | 追加写入 | `echo "text" >> file.txt` |
| `2>` | 重定向stderr | `cmd 2> error.log` |
| `2>&1` | stderr合并到stdout | `cmd > all.log 2>&1` |
| `&>` | stdout和stderr都重定向 | `cmd &> all.log` |
| `>|` | 强制覆盖（即使设置了noclobber） | `echo "text" >| file.txt` |

#### 使用 Here Document

```bash
# 写入多行内容
cat > config.txt << EOF
server=localhost
port=8080
debug=true
EOF

# 禁止变量扩展
cat > script.sh << 'EOF'
echo "当前目录: $PWD"
EOF

# 追加模式
cat >> config.txt << EOF
# 附加配置
timeout=30
EOF
```

#### 使用 `tee` 命令

```bash
# 同时输出到屏幕和文件
echo "Hello" | tee output.txt

# 追加模式
echo "World" | tee -a output.txt

# 写入多个文件
echo "Data" | tee file1.txt file2.txt file3.txt

# 需要sudo写入时
echo "content" | sudo tee /etc/somefile > /dev/null
```

### 读取用户输入

```bash
# 基本读取
read -p "请输入姓名: " name
echo "你好, $name"

# 带超时
read -t 5 -p "5秒内输入: " input

# 隐藏输入（密码）
read -s -p "请输入密码: " password

# 读取单个字符
read -n 1 -p "按任意键继续..."

# 读取到数组
read -a arr <<< "a b c d"
echo "${arr[1]}"  # 输出: b
```

📄 **示例脚本**: [02-file-process.sh](02-file-process.sh)

---

## 2.3 文本处理工具

### grep - 文本搜索

```bash
# 基本搜索
grep "pattern" file.txt

# 常用选项
grep -i "pattern" file.txt      # 忽略大小写
grep -n "pattern" file.txt      # 显示行号
grep -c "pattern" file.txt      # 统计匹配行数
grep -l "pattern" *.txt         # 只显示文件名
grep -L "pattern" *.txt         # 显示不匹配的文件名
grep -v "pattern" file.txt      # 反向匹配（不包含）
grep -w "word" file.txt         # 全词匹配
grep -r "pattern" dir/          # 递归搜索目录

# 正则表达式
grep -E "regex" file.txt        # 扩展正则（或 egrep）
grep -P "regex" file.txt        # Perl正则

# 上下文显示
grep -A 3 "pattern" file.txt    # 显示匹配行及后3行
grep -B 3 "pattern" file.txt    # 显示匹配行及前3行
grep -C 3 "pattern" file.txt    # 显示匹配行及前后各3行

# 实际示例
# 查找日志中的错误
grep -i "error\|fail\|exception" app.log

# 查找包含IP地址的行
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log

# 在代码中查找函数定义
grep -rn "def main" --include="*.py" .
```

### sed - 流编辑器

```bash
# 基本替换
sed 's/old/new/' file.txt           # 替换每行第一个匹配
sed 's/old/new/g' file.txt          # 替换所有匹配
sed 's/old/new/gi' file.txt         # 忽略大小写

# 原地修改文件
sed -i 's/old/new/g' file.txt       # Linux
sed -i '' 's/old/new/g' file.txt    # macOS

# 删除行
sed '/pattern/d' file.txt           # 删除匹配行
sed '5d' file.txt                   # 删除第5行
sed '5,10d' file.txt                # 删除第5-10行
sed '/^$/d' file.txt                # 删除空行
sed '/^#/d' file.txt                # 删除注释行

# 打印特定行
sed -n '5p' file.txt                # 打印第5行
sed -n '5,10p' file.txt             # 打印第5-10行
sed -n '/pattern/p' file.txt        # 打印匹配行

# 插入和追加
sed '3i\新行内容' file.txt          # 在第3行前插入
sed '3a\新行内容' file.txt          # 在第3行后追加
sed '/pattern/i\新行' file.txt      # 在匹配行前插入

# 替换整行
sed '/pattern/c\替换内容' file.txt

# 多个操作
sed -e 's/a/A/g' -e 's/b/B/g' file.txt
sed 's/a/A/g; s/b/B/g' file.txt

# 实际示例
# 修改配置文件中的值
sed -i 's/^port=.*/port=8080/' config.txt

# 在文件开头添加行
sed -i '1i\#!/bin/bash' script.sh

# 删除行首空格
sed 's/^[[:space:]]*//' file.txt
```

### awk - 文本处理语言

```bash
# 基本语法
awk 'pattern { action }' file.txt

# 打印特定列（默认空格分隔）
awk '{print $1}' file.txt           # 第1列
awk '{print $1, $3}' file.txt       # 第1和第3列
awk '{print $NF}' file.txt          # 最后一列
awk '{print $(NF-1)}' file.txt      # 倒数第二列

# 指定分隔符
awk -F: '{print $1}' /etc/passwd    # 冒号分隔
awk -F',' '{print $2}' data.csv     # 逗号分隔

# 条件过滤
awk '$3 > 100' file.txt             # 第3列大于100的行
awk '/pattern/' file.txt            # 包含pattern的行
awk '$1 == "root"' /etc/passwd      # 第1列等于root

# 内置变量
awk '{print NR, $0}' file.txt       # NR: 行号
awk '{print NF}' file.txt           # NF: 字段数
awk 'END {print NR}' file.txt       # 总行数

# 计算统计
awk '{sum += $1} END {print sum}' file.txt                  # 求和
awk '{sum += $1} END {print sum/NR}' file.txt               # 平均值
awk 'BEGIN {max=0} $1>max {max=$1} END {print max}' file    # 最大值

# BEGIN 和 END 块
awk 'BEGIN {print "开始处理"} {print $0} END {print "处理完成"}' file.txt

# 格式化输出
awk '{printf "%-10s %5d\n", $1, $2}' file.txt

# 实际示例
# 统计日志中每个IP的访问次数
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head

# 计算CSV文件某列的总和
awk -F',' '{sum += $3} END {printf "总计: %.2f\n", sum}' data.csv

# 提取passwd文件中的用户名和shell
awk -F: '{print $1 " -> " $7}' /etc/passwd
```

### 其他常用文本工具

```bash
# cut - 提取列
cut -d: -f1 /etc/passwd             # 提取第1列
cut -d: -f1,7 /etc/passwd           # 提取第1和第7列
cut -c1-10 file.txt                 # 提取每行前10个字符

# sort - 排序
sort file.txt                       # 默认排序
sort -n file.txt                    # 数值排序
sort -r file.txt                    # 逆序
sort -k2 file.txt                   # 按第2列排序
sort -t: -k3 -n /etc/passwd         # 按第3列数值排序，冒号分隔
sort -u file.txt                    # 排序并去重

# uniq - 去重（需要先排序）
sort file.txt | uniq                # 去重
sort file.txt | uniq -c             # 统计重复次数
sort file.txt | uniq -d             # 只显示重复行

# wc - 统计
wc -l file.txt                      # 行数
wc -w file.txt                      # 单词数
wc -c file.txt                      # 字节数
wc -m file.txt                      # 字符数

# tr - 字符转换
tr 'a-z' 'A-Z' < file.txt           # 小写转大写
tr -d '\r' < file.txt               # 删除回车符
tr -s ' ' < file.txt                # 压缩连续空格

# paste - 合并文件
paste file1.txt file2.txt           # 按列合并
paste -d',' file1.txt file2.txt     # 用逗号分隔

# diff - 比较文件
diff file1.txt file2.txt            # 比较差异
diff -u file1.txt file2.txt         # 统一格式（更易读）
diff -y file1.txt file2.txt         # 并排显示
```

📄 **示例脚本**: [02-file-process.sh](02-file-process.sh)

---

## 2.4 目录操作

### 基本目录操作

```bash
# 创建目录
mkdir mydir                         # 创建单个目录
mkdir -p path/to/deep/dir           # 创建多级目录
mkdir -m 755 mydir                  # 创建时指定权限

# 删除目录
rmdir emptydir                      # 删除空目录
rm -r mydir                         # 递归删除
rm -rf mydir                        # 强制递归删除（危险！）

# 切换目录
cd /path/to/dir                     # 绝对路径
cd relative/path                    # 相对路径
cd ~                                # 用户主目录
cd -                                # 返回上一个目录
cd ..                               # 上级目录

# 列出目录内容
ls                                  # 基本列表
ls -l                               # 详细信息
ls -la                              # 包含隐藏文件
ls -lh                              # 人类可读大小
ls -lt                              # 按时间排序
ls -lS                              # 按大小排序
ls -R                               # 递归列出

# 复制和移动
cp -r srcdir destdir                # 递归复制目录
mv oldname newname                  # 重命名/移动目录
```

### find - 查找文件

```bash
# 基本语法
find [路径] [条件] [动作]

# 按名称查找
find . -name "*.txt"                # 当前目录下所有txt文件
find . -iname "*.TXT"               # 忽略大小写
find . -name "file?.txt"            # ?匹配单个字符

# 按类型查找
find . -type f                      # 普通文件
find . -type d                      # 目录
find . -type l                      # 符号链接

# 按大小查找
find . -size +100M                  # 大于100MB
find . -size -1k                    # 小于1KB
find . -size 0                      # 空文件

# 按时间查找
find . -mtime -7                    # 7天内修改过
find . -mtime +30                   # 30天前修改
find . -mmin -60                    # 60分钟内修改

# 按权限查找
find . -perm 755                    # 权限为755
find . -perm -u+x                   # 所有者可执行

# 按所有者查找
find . -user root                   # 属于root用户
find . -group admin                 # 属于admin组

# 组合条件
find . -name "*.log" -size +10M                    # AND
find . -name "*.txt" -o -name "*.md"               # OR
find . ! -name "*.tmp"                              # NOT
find . -name "*.py" -not -path "./venv/*"          # 排除目录

# 执行动作
find . -name "*.tmp" -delete                       # 删除
find . -name "*.sh" -exec chmod +x {} \;           # 执行命令
find . -name "*.log" -exec ls -l {} \;             # 查看详情
find . -type f -exec grep -l "pattern" {} \;       # 搜索内容

# 使用 xargs（更高效）
find . -name "*.txt" | xargs grep "pattern"
find . -name "*.txt" -print0 | xargs -0 grep "pattern"  # 处理空格文件名

# 实际示例
# 删除所有空目录
find . -type d -empty -delete

# 查找大文件
find /var -type f -size +100M -exec ls -lh {} \;

# 查找并压缩旧日志
find /var/log -name "*.log" -mtime +7 -exec gzip {} \;

# 统计Python代码行数
find . -name "*.py" -exec wc -l {} + | tail -1
```

### 目录遍历

```bash
# 使用 for 循环遍历
for file in /path/to/dir/*; do
    if [[ -f "$file" ]]; then
        echo "文件: $file"
    elif [[ -d "$file" ]]; then
        echo "目录: $file"
    fi
done

# 递归遍历（使用 find）
find /path/to/dir -type f | while read -r file; do
    echo "处理: $file"
done

# 递归遍历（使用 globstar）
shopt -s globstar
for file in /path/to/dir/**/*; do
    [[ -f "$file" ]] && echo "$file"
done

# 使用函数递归
traverse_dir() {
    local dir="$1"
    for item in "$dir"/*; do
        if [[ -d "$item" ]]; then
            echo "目录: $item"
            traverse_dir "$item"  # 递归调用
        elif [[ -f "$item" ]]; then
            echo "文件: $item"
        fi
    done
}
traverse_dir "/path/to/dir"
```

### 通配符模式

| 模式 | 说明 | 示例 |
|------|------|------|
| `*` | 匹配任意字符串 | `*.txt` |
| `?` | 匹配单个字符 | `file?.txt` |
| `[abc]` | 匹配其中任意一个字符 | `file[123].txt` |
| `[a-z]` | 匹配范围内字符 | `file[a-z].txt` |
| `[!abc]` | 不匹配其中任何字符 | `file[!0-9].txt` |
| `{a,b,c}` | 匹配列表中任意一个 | `file.{txt,md,log}` |
| `**` | 递归匹配（需启用globstar） | `**/*.py` |

```bash
# 启用扩展通配符
shopt -s extglob

# 扩展模式
ls !(*.txt)                         # 排除txt文件
ls *.@(txt|md)                      # txt或md文件
ls *(pattern)                       # 0次或多次匹配
ls +(pattern)                       # 1次或多次匹配
ls ?(pattern)                       # 0次或1次匹配
```

📄 **示例脚本**: [03-directory-ops.sh](03-directory-ops.sh)

---

## 📝 快速参考

### 文件测试速查

```bash
[[ -e file ]]   # 存在
[[ -f file ]]   # 普通文件
[[ -d file ]]   # 目录
[[ -r file ]]   # 可读
[[ -w file ]]   # 可写
[[ -x file ]]   # 可执行
[[ -s file ]]   # 非空
```

### 重定向速查

```bash
cmd > file      # 覆盖
cmd >> file     # 追加
cmd 2> file     # stderr
cmd &> file     # 全部
cmd > file 2>&1 # 全部（兼容写法）
```

### 文本处理速查

| 任务 | 命令 |
|------|------|
| 搜索 | `grep "pattern" file` |
| 替换 | `sed 's/old/new/g' file` |
| 提取列 | `awk '{print $1}' file` |
| 排序 | `sort file` |
| 去重 | `sort file \| uniq` |
| 统计行数 | `wc -l file` |
| 查找文件 | `find . -name "*.txt"` |

---

## 📂 本章示例文件

| 文件 | 说明 |
|------|------|
| [01-file-test.sh](01-file-test.sh) | 文件测试示例 |
| [02-file-process.sh](02-file-process.sh) | 文件读写与文本处理 |
| [03-directory-ops.sh](03-directory-ops.sh) | 目录操作与遍历 |

---

## 🎯 练习建议

1. **文件检测器**：编写脚本，接受文件路径参数，输出文件的完整属性信息
2. **日志分析**：分析一个日志文件，统计每个小时的日志数量
3. **批量重命名**：将目录下所有`.txt`文件重命名为`.bak`
4. **大文件查找**：查找系统中大于指定大小的文件并生成报告
5. **代码统计**：统计项目中各类源代码文件的行数

---

[← 上一章：Shell基础](../01-basics/README.md) | [下一章：进程与后台任务 →](../03-process-management/README.md)

