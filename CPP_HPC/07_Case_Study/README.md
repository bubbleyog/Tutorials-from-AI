# 第七章：综合案例 —— N-Body 模拟

欢迎来到本教程的最后一章！我们将综合运用之前学到的所有知识：C++ 性能优化、OpenMP 共享内存并行、MPI 分布式内存并行以及 CMake 构建系统，来实现一个经典的 HPC 问题 —— **N-Body 模拟**。

## 1. 问题背景

N-Body 问题模拟的是 N 个粒子在引力相互作用下的运动（如星系演化）。
核心计算是每两个粒子之间都要计算引力，时间复杂度为 $O(N^2)$。这使其成为测试 HPC 系统性能的绝佳案例。

公式：
$$ F_{ij} = G \frac{m_i m_j}{r_{ij}^2} \frac{\vec{r}_{ij}}{r_{ij}} $$

## 2. 代码结构

```
07_Case_Study/
├── code/
│   ├── include/
│   │   └── nbody_core.hpp  # 数据结构定义
│   ├── src/
│   │   ├── nbody_core.cpp  # 初始化、IO 等辅助函数
│   │   ├── nbody_omp.cpp   # OpenMP 版本实现
│   │   └── nbody_mpi.cpp   # MPI 版本实现
│   ├── CMakeLists.txt      # 构建脚本
│   └── plot_nbody.py       # Python 可视化脚本
```

## 3. 实现细节

### OpenMP 版本
- **并行策略**: 使用 `#pragma omp parallel for` 并行化最外层的粒子循环。
- **负载均衡**: 由于每个粒子的计算量相同（都要与 N-1 个粒子交互），使用 `schedule(static)` 即可。
- **数据竞争**: 在更新位置时没有竞争，但在计算力时如果使用牛顿第三定律优化 ($F_{ji} = -F_{ij}$) 会引入竞争。为了简单起见，我们不做此优化，直接计算 $O(N^2)$ 次。

### MPI 版本
- **并行策略**: 数据复制 (Replicated Data)。
    - 每个进程存储所有粒子的位置（因为计算力需要知道所有人的位置）。
    - 每个进程只负责更新它分到的那一部分粒子的位置和速度。
- **通信**: 使用 `MPI_Allgather` 在每一步结束后同步位置信息。

## 4. 编译与运行

```bash
cd code
mkdir build && cd build
cmake ..
make

# 运行 OpenMP 版本
# 模拟 2000 个粒子
export OMP_NUM_THREADS=4
./nbody_omp 2000

# 运行 MPI 版本 (如果在支持 MPI 的环境中)
mpirun -n 4 ./nbody_mpi
```

## 5. 性能分析

对于 $N=2000$，交互次数为 $4 \times 10^6$ 次/步。
观察 `MOp/s` (Million Operations per Second) 指标，这是衡量 N-Body 模拟性能的常用单位。

## 6. 结语

恭喜你完成了本教程！
从现代 C++ 的 RAII 和移动语义，到数值计算的坑，再到 OpenMP 和 MPI 的并行魔法，你已经掌握了 HPC 编程的核心基石。

**接下来的路：**
- 学习 **CUDA/HIP**：利用 GPU 进行加速（N-Body 在 GPU 上能快上百倍）。
- 学习 **SIMD Intrinsic**：手动编写 AVX-512 代码压榨 CPU 极限。
- 学习 **MPI+OpenMP 混合编程**：在节点间用 MPI，节点内用 OpenMP，减少通信开销。

祝你在 HPC 的世界里探索愉快！
