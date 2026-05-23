# Environment Modules 使用指南

在超算中心，系统管理员通常安装了同一个软件的多个版本（例如 gcc 4.8, 7.3, 9.1 等）。为了避免冲突，系统使用 **Modules** 来动态管理环境变量 (`PATH`, `LD_LIBRARY_PATH` 等)。

## 常用命令

| 命令 | 说明 |
| :--- | :--- |
| `module avail` | 列出所有可用的软件模块 |
| `module list` | 列出当前已加载的模块 |
| `module load <name>` | 加载指定模块 (例如 `module load gcc/9.3.0`) |
| `module unload <name>` | 卸载指定模块 |
| `module purge` | 卸载所有模块 (重置环境) |
| `module show <name>` | 查看模块具体修改了哪些环境变量 |

## 示例

假设你需要使用 GCC 9.3 和 OpenMPI 4.0 编译程序：

```bash
# 1. 查看有哪些编译器可用
module avail gcc

# 2. 加载特定版本
module load gcc/9.3.0

# 3. 加载 MPI
module load openmpi/4.0.3

# 4. 验证
gcc --version
mpicxx --version
```

## 最佳实践

- **显式版本号**: 在脚本中尽量写全版本号 `module load gcc/9.3.0`，而不是 `module load gcc`，以保证结果的可重现性。
- **依赖管理**: 有些模块会自动加载依赖（例如加载 openmpi 可能会自动加载对应的 gcc），但也有些需要你手动按顺序加载。使用 `module list` 检查。
- **清理环境**: 在作业脚本开头使用 `module purge` 是个好习惯，可以避免受到登录节点环境的干扰。
