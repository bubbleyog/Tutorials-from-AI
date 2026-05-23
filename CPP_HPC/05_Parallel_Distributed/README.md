# 第五章：分布式内存并行 (MPI)

当单台机器的内存和算力无法满足需求时，我们需要将任务分发到多台计算机（节点）上。**MPI (Message Passing Interface)** 是分布式内存并行的事实标准。

与共享内存模型（OpenMP）不同，MPI 进程拥有独立的内存空间。进程间必须通过**显式的消息传递**（发送和接收数据包）来交换信息。

## 1. 核心概念

- **Rank (进程号)**: 每个进程的唯一标识符（0, 1, 2...）。通常 Rank 0 被称为主进程 (Master)，负责分发任务和汇总结果。
- **Size (进程总数)**: 通信域内有多少个进程。
- **Communicator (通信域)**: `MPI_COMM_WORLD` 包含所有启动的进程。

## 2. MPI 编程模型

MPI 程序通常遵循 SPMD (Single Program, Multiple Data) 模式：**同一份代码，在不同进程上运行**，通过 `rank` 来区分行为。

```cpp
if (rank == 0) {
    // 我是 Master，发送任务
} else {
    // 我是 Worker，接收任务并计算
}
```

## 3. 点对点通信 (Point-to-Point)

最基础的通信方式：一个发，一个收。

- **`MPI_Send`**: 发送数据。
- **`MPI_Recv`**: 接收数据（阻塞，直到收到数据）。

### 示例代码解析
请查看 [code/mpi_p2p.cpp](./code/mpi_p2p.cpp)。
Rank 0 和 Rank 1 互相发送数据，模拟乒乓球游戏。

## 4. 集合通信 (Collective Communication)

涉及通信域中所有进程的操作。通常比手动写 Send/Recv 更高效且不易出错。

- **`MPI_Bcast` (Broadcast)**: 一人广播，所有人接收。
- **`MPI_Reduce`**: 所有人提交数据，系统进行归约（求和、最大值等），结果存到 Root 进程。
- **`MPI_Scatter`**: 将一个大数组切分发给所有人。
- **`MPI_Gather`**: 收集所有人的数据拼成一个大数组。

### 示例代码解析
请查看 [code/mpi_coll.cpp](./code/mpi_coll.cpp)。
演示了如何使用 `MPI_Bcast` 分发参数，并用 `MPI_Reduce` 汇总计算出的 PI 值。

## 5. 编译与运行

MPI 程序需要特殊的编译器包装器 (`mpicxx`) 和运行器 (`mpirun`)。

### 编译
CMake 会自动查找 MPI 库。

```bash
cd code
mkdir build && cd build
cmake ..
make
```

### 运行
使用 `mpirun` 或 `mpiexec` 启动多个进程。
`-n 4` 表示启动 4个进程。这些进程可以跑在同一台机器的不同核上，也可以通过 hostfile 跑在不同的机器上。

```bash
# 运行 Hello World
mpirun -n 4 ./mpi_hello

# 运行 Ping Pong (至少需要2个进程)
mpirun -n 2 ./mpi_p2p

# 运行 PI 计算
mpirun -n 4 ./mpi_coll
```

## 6. 总结

- MPI 是超算领域的通用语言。
- **点对点通信**灵活但容易死锁（如两个进程互相 Recv）。
- **集合通信**高效且安全，应优先使用。
- 尽量减少通信次数和数据量，通信往往是分布式计算的瓶颈。

---
[上一章：共享内存并行 (OpenMP & Threads)](../04_Parallel_Shared_Memory) | [下一章：HPC 环境与构建系统](../06_HPC_Environment) (待更新)
