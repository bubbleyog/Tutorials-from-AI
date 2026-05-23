# 第四章：共享内存并行 (OpenMP & Threads)

单核优化到极致后，下一步就是利用多核 CPU。**共享内存并行**是指所有线程都可以访问同一个内存空间（变量），这是最简单的并行模式。

本章介绍两种主要方法：
1.  **OpenMP (Open Multi-Processing)**: 基于指令（Pragma）的并行，简单易用，适合循环并行化。
2.  **C++ Standard Threads (`std::thread`, `std::async`)**: 基于库的并行，灵活强大，适合任务并行和复杂同步。

## 1. OpenMP 基础

OpenMP 是 HPC 领域的标准。你只需要在代码中添加一行 `#pragma omp ...`，编译器就会自动帮你生成多线程代码。

### 核心指令
- **`#pragma omp parallel for`**: 最常用的指令。将紧随其后的 `for` 循环分配给多个线程执行。
- **`reduction(op:var)`**: 归约操作。解决多线程累加同一个变量时的竞争问题。例如 `reduction(+:sum)` 会让每个线程维护一个局部 `sum`，最后自动加到全局 `sum` 上。
- **`schedule(static/dynamic)`**: 任务调度策略。
    - `static`: 任务平均分配，开销小，适合负载均衡。
    - `dynamic`: 抢占式分配，适合负载不均衡（有的任务快，有的慢）。

### 示例代码解析
请查看 [code/omp_demo.cpp](./code/omp_demo.cpp)。

```cpp
// 只需要这一行，原本串行的代码就变成了并行！
#pragma omp parallel for reduction(+:sum)
for (long i = 0; i < num_steps; i++) {
    double x = (i + 0.5) * step;
    sum += 4.0 / (1.0 + x * x);
}
```

## 2. C++ 标准线程库

对于更复杂的并行模式（如生产者-消费者模型，或者任务图），OpenMP 可能不够灵活。C++11 引入了 `std::thread`，C++17 引入了并行算法。

### 核心组件
- **`std::thread`**: 创建一个新线程。
- **`std::async` & `std::future`**: 更高级的抽象。`async` 启动任务，`future.get()` 获取结果（如果没算完会等待）。
- **`std::atomic`**: 原子变量，保证多线程修改时的安全性，比 `std::mutex` 锁更轻量。

### 示例代码解析
请查看 [code/thread_demo.cpp](./code/thread_demo.cpp)。我们演示了如何使用多线程进行蒙特卡洛 PI 模拟。

```cpp
// 使用 std::async 启动异步任务
std::vector<std::future<long long>> futures;
for(int i=0; i<num_threads; ++i) {
    futures.push_back(std::async(std::launch::async, monte_carlo_pi_task, samples_per_thread));
}

// 获取结果
for(auto& f : futures) {
    total += f.get();
}
```

## 3. 编译与运行

OpenMP 需要编译器支持（GCC/Clang 默认支持，需加 `-fopenmp`）。

```bash
cd code
mkdir build && cd build
cmake ..
make

# 运行 OpenMP 示例
# 可以通过环境变量 OMP_NUM_THREADS 控制线程数
export OMP_NUM_THREADS=4
./omp_demo

# 运行 Thread 示例
./thread_demo
```

## 4. 总结

- **优先使用 OpenMP**: 如果你的任务是“把一个大循环拆开算”，OpenMP 是最快、最不易出错的选择。
- **使用 std::async**: 如果你需要从线程获取返回值，或者任务之间有复杂的依赖关系。
- **避免锁竞争**: 尽量让每个线程操作自己的局部变量，最后再汇总（Reduction），而不是频繁锁住全局变量。

---
[上一章：性能分析与单核优化](../03_Performance_Optimization) | [下一章：分布式内存并行 (MPI)](../05_Parallel_Distributed) (待更新)
