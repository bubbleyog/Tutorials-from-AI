# 第六章：HPC 环境与构建系统

在个人电脑上开发代码和在超算集群上运行代码是两回事。本章将介绍如何在真实的 HPC 环境中生存和工作。

## 1. 复杂的 CMake 项目管理

当项目变大时，将所有代码塞进一个文件是不现实的。规范的 C++ 项目结构如下：

```
Project/
├── CMakeLists.txt      # 根构建脚本
├── include/            # 头文件 (.hpp)
│   └── hpc_utils.hpp
├── src/                # 源文件 (.cpp)
│   ├── main.cpp
│   └── hpc_utils.cpp
└── build/              # 构建目录 (不要提交到 Git)
```

### 关键 CMake 技巧
- **`add_library`**: 将功能模块编译成静态库或动态库，提高编译速度和模块化。
- **`target_link_libraries`**: 管理依赖关系。
- **`install`**: 定义安装规则，方便部署。

请查看 [code/CMakeLists.txt](./code/CMakeLists.txt) 学习如何编写规范的构建脚本。

## 2. Environment Modules

超算中心通常安装了海量的软件版本。为了切换不同版本的编译器或库（如 GCC 9 vs GCC 10），我们使用 `module` 命令。

详细指南请参考：[modules_guide.md](./modules_guide.md)

## 3. 作业调度系统 (Slurm)

你不能直接在登录节点（Login Node）上运行耗时的计算任务！这会卡死其他用户，甚至导致你被管理员封号。

正确做法是：**编写作业脚本，提交给调度系统 (Scheduler)**。
Slurm 是目前最流行的调度系统。

### 核心流程
1.  编写脚本 `job.slurm`，指定需要的资源（多少个节点、多少核、运行多久）。
2.  使用 `sbatch job.slurm` 提交作业。
3.  使用 `squeue -u <username>` 查看作业排队/运行状态。
4.  作业结束后，查看生成的 `result.out` 和 `result.err` 文件。

### 脚本模板
请查看 [code/job_script.slurm](./code/job_script.slurm)，这是一个可以直接拿去用的模板。

```bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00

module load openmpi/4.0.3
srun ./build/app
```

## 4. 总结

- **CMake** 是管理 C++ 项目构建的标准。
- **Modules** 让你在复杂的软件环境中游刃有余。
- **Slurm** 是你获取计算资源的唯一途径，学会写 `sbatch` 脚本是 HPC 工程师的基本功。

---
[上一章：分布式内存并行 (MPI)](../05_Parallel_Distributed) | [下一章：综合案例 (N-Body)](../07_Case_Study) (待更新)
