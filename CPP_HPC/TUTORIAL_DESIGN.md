# C++ 高性能计算 (HPC) 教程项目设计文档

## 1. 项目概述
本项目旨在为具备一定 C++ 基础的开发者提供一份系统性的高性能计算入门与进阶教程。教程将涵盖现代 C++ 在科学计算中的应用、性能优化技术、并行计算模型（共享内存与分布式内存）、以及在高性能计算集群环境下的开发与部署。

## 2. 目标受众
- 理工科研究生与科研人员
- 对高性能计算感兴趣的软件工程师
- 希望从 C++98/03 迁移到现代 C++ (C++11/14/17/20) 进行科学计算的开发者

## 3. 项目结构与目录规划
项目根目录将包含各个章节的子目录，每个子目录结构如下：
```
Chapter_XX_Topic/
├── README.md       # 教程正文（理论讲解、代码解析）
└── code/           # 示例代码目录
    ├── CMakeLists.txt
    ├── example1.cpp
    └── ...
```

## 4. 章节详细规划

### 第一阶段：基础夯实与现代特性

#### [01_Modern_CPP_Base](./01_Modern_CPP_Base) - 现代 C++ 高性能计算基础
- **目标**: 掌握对性能至关重要的现代 C++ 特性。
- **内容**:
    - RAII 与资源管理 (Smart Pointers)。
    - 移动语义 (Move Semantics) 与完美转发 (Perfect Forwarding) 避免不必要的拷贝。
    - `constexpr` 与编译期计算。
    - 常用 STL 容器在 HPC 中的性能考量 (`std::vector` vs `std::array`)。
- **示例**: 矩阵类的简单实现（对比拷贝构造与移动构造的性能差异）。

#### [02_Numerical_Computing](./02_Numerical_Computing) - 数值计算基础与库的使用
- **目标**: 理解浮点数陷阱并学会使用成熟的数学库。
- **内容**:
    - IEEE 754 浮点数标准、精度丢失与数值稳定性。
    - 线性代数库 Eigen 或 Armadillo 的使用。
    - BLAS 与 LAPACK 简介。
- **示例**: 使用 Eigen 求解线性方程组；浮点数精度测试程序。

### 第二阶段：单节点性能优化

#### [03_Performance_Optimization](./03_Performance_Optimization) - 性能分析与单核优化
- **目标**: 学会“压榨”单核性能。
- **内容**:
    - 性能分析工具 (Profiling): `gprof`, `perf`, `Valgrind`.
    - 编译器优化选项 (`-O2`, `-O3`, `-march=native`, `-ffast-math`).
    - CPU 架构基础：缓存 (Cache) 友好编程（数据局部性）。
    - SIMD (单指令多数据) 简介与自动向量化。
- **示例**: 矩阵乘法的朴素实现 vs 循环分块 (Tiling) 优化 vs 向量化实现。

### 第三阶段：并行计算

#### [04_Parallel_Shared_Memory](./04_Parallel_Shared_Memory) - 共享内存并行 (OpenMP & Threads)
- **目标**: 利用多核 CPU 提升性能。
- **内容**:
    - OpenMP 基础指令 (`#pragma omp parallel for`, reduction, collapse)。
    - C++ 标准线程库 (`std::thread`, `std::async`) 与原子操作 (`std::atomic`)。
    - 竞争条件 (Race Condition) 与死锁避免。
- **示例**: 并行蒙特卡洛积分；OpenMP 加速的矩阵向量乘法。

#### [05_Parallel_Distributed](./05_Parallel_Distributed) - 分布式内存并行 (MPI)
- **目标**: 跨越多台服务器进行计算。
- **内容**:
    - MPI (Message Passing Interface) 编程模型。
    - 点对点通信 (`MPI_Send`, `MPI_Recv`)。
    - 集合通信 (`MPI_Bcast`, `MPI_Reduce`, `MPI_Scatter`, `MPI_Gather`)。
    - 简单的域分解 (Domain Decomposition) 思想。
- **示例**: MPI 实现的并行求和；简单的并行热传导模拟。

### 第四阶段：环境与进阶

#### [06_HPC_Environment](./06_HPC_Environment) - HPC 环境与构建系统
- **目标**: 在真实的超算集群上工作。
- **内容**:
    - CMake 进阶：管理复杂的 HPC 项目依赖。
    - 作业调度系统 Slurm 基础 (编写 sbatch 脚本)。
    - Environment Modules (`module load ...`)。
- **示例**: 编写一个完整的 CMake 项目并提交 Slurm 作业脚本。

#### [07_Case_Study](./07_Case_Study) - 综合案例：N-Body 模拟或热传导方程
- **目标**: 综合运用所学知识解决实际问题。
- **内容**:
    - 问题物理背景介绍。
    - 离散化方法。
    - 混合并行 (MPI + OpenMP) 实现。
    - 性能测试与扩展性分析 (Scalability)。
- **示例**: 完整的 N-Body 粒子模拟程序。

## 5. 编写规范
- **代码风格**: 遵循 Google C++ Style Guide 或 LLVM Style Guide。
- **构建工具**: 所有示例均使用 CMake 构建。
- **环境**: 
    - OS: Linux (Ubuntu/CentOS)
    - Compiler: GCC >= 9.0 或 Clang >= 10.0
    - MPI: OpenMPI or MPICH
    - Libraries: Eigen3

## 6. 后续扩展计划 (Optional)
- GPU 编程 (CUDA / HIP / OpenACC)
- 并行 I/O (HDF5)
- 性能模型 (Roofline Model)
