# 第三章：性能分析与单核优化

在并行化代码之前，我们必须确保单核代码已经足够高效。一个低效的串行算法并行化后，往往比不上一个高度优化的串行算法。

本章将深入探讨决定 CPU 性能的两个关键因素：**内存访问 (Memory Access)** 和 **指令级并行 (Instruction Level Parallelism)**。

## 1. 性能分析 (Profiling)

不要猜测瓶颈在哪里，测量它！

### 常用工具
- **Linux perf**: 强大的系统级性能分析工具。
    - `perf stat ./app`: 查看 CPU 周期、指令数、Cache Miss 等宏观指标。
    - `perf record -g ./app` & `perf report`: 查看具体哪个函数占用了 CPU 时间。
- **Intel VTune Profiler** / **AMD uProf**: 厂商提供的可视化分析工具，能提供更深层的微架构建议。
- **gprof**: GNU 传统的分析工具，需要编译时加 `-pg` 选项。

## 2. 编译器优化

现代编译器非常聪明，但需要你给出正确的指令。

- **`-O2` vs `-O3`**: `-O3` 开启了更激进的优化（如循环展开、函数内联），通常是 HPC 的首选。
- **`-march=native`**: 告诉编译器“针对当前这台机器的 CPU 生成代码”。这允许使用最新的指令集（如 AVX2, AVX-512），可能会带来 2-8 倍的加速。
- **`-ffast-math`**: 允许编译器打破 IEEE 754 标准，进行更快的浮点运算（注意：可能会改变精度，见第二章）。

## 3. CPU 缓存友好编程 (Cache Friendliness)

CPU 计算速度远快于内存读取速度。数据从 RAM 加载到 CPU 需要几百个时钟周期，而从 L1 Cache 加载只需几个周期。**Cache Miss 是性能杀手**。

### 原则
1.  **空间局部性 (Spatial Locality)**: 如果你访问了内存地址 $x$，很可能马上会访问 $x+1$。因此，按顺序访问数组（`vector`）比跳跃访问（链表、指针追逐）快得多。
2.  **时间局部性 (Temporal Locality)**: 如果你访问了内存地址 $x$，很可能马上会再次访问它。

### 示例：矩阵乘法优化
在 [code/matrix_multiply_opt.cpp](./code/matrix_multiply_opt.cpp) 中，我们演示了三种实现：

1.  **Naive (i-j-k)**: 最直观的实现，但对矩阵 B 的访问是列优先（在 C++ 行优先存储中是跳跃访问），导致大量 Cache Miss。
2.  **Optimized (i-k-j)**: 仅仅交换了循环顺序，使得对 C 和 B 的访问都变成了连续访问。**性能通常提升 5-10 倍！**
3.  **Tiled (分块)**: 将矩阵切分成小块，确保每个块的数据都能完全装入 L1/L2 Cache，进一步减少内存带宽压力。

## 4. 伪共享 (False Sharing)

在多线程编程中，这是一个极易被忽视的陷阱。

当多个线程分别修改不同的变量，但这些变量恰好位于同一个 **Cache Line** (通常 64 字节) 上时，CPU 核心之间会不断争抢这个 Cache Line 的所有权，导致性能剧烈下降。

### 解决方案
使用 `alignas(64)` 或 `padding` 将频繁修改的变量隔离开。

请运行 [code/false_sharing.cpp](./code/false_sharing.cpp) 查看惊人的性能差异（通常差 10 倍以上）。

## 5. SIMD 与自动向量化

**SIMD (Single Instruction, Multiple Data)** 允许 CPU 一条指令处理多个数据（如一次加 4 个 double）。

- **自动向量化**: 编译器（开启 `-O3`）会自动尝试将循环转换为 SIMD 指令。
- **帮助编译器**:
    - 确保内存对齐。
    - 循环结构简单，没有复杂的 if/else 跳转。
    - 避免数据依赖。

## 6. 编译与运行

```bash
cd code
mkdir build && cd build
cmake ..
make

# 运行矩阵乘法对比
echo "--- Matrix Multiplication ---"
./gemm_O3

# 运行 False Sharing 对比
echo -e "\n--- False Sharing ---"
./false_sharing
```

## 7. 总结

- 优化第一步：使用 `-O3 -march=native`。
- 优化核心：**让数据在内存中连续，并按顺序访问**。
- 多线程陷阱：警惕伪共享，使用 padding 隔离热点数据。

---
[上一章：数值计算基础与库的使用](../02_Numerical_Computing) | [下一章：共享内存并行 (OpenMP & Threads)](../04_Parallel_Shared_Memory) (待更新)
