#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <omp.h>

// OpenMP 示例：计算数值积分 (Numerical Integration)
// 计算 pi = integral of 4/(1+x^2) from 0 to 1

// 串行版本
double calc_pi_serial(long num_steps) {
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;
    for (long i = 0; i < num_steps; i++) {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }
    return step * sum;
}

// 并行版本 1：朴素 Parallel For (存在竞争条件或需要锁，这里演示 Reduction)
// reduction(+:sum) 会自动为每个线程创建一个私有的 sum 变量，最后汇总
double calc_pi_omp_reduction(long num_steps) {
    double step = 1.0 / (double)num_steps;
    double sum = 0.0;

    #pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < num_steps; i++) {
        double x = (i + 0.5) * step;
        sum += 4.0 / (1.0 + x * x);
    }
    return step * sum;
}

// 演示 schedule 调度策略
// 模拟负载不均衡的情况：每个任务的计算量不同
void unbalanced_workload() {
    const int N = 100;
    std::cout << "\n=== Unbalanced Workload Test (Schedule) ===" << std::endl;
    
    // 静态调度 (Static): 任务均分，如果某些任务特别慢，其他线程会空等
    auto start = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for schedule(static)
    for(int i=0; i<N; ++i) {
        // 模拟计算量随 i 增加 (i 越大越慢)
        double res = 0;
        for(int j=0; j<i*10000; ++j) res += std::sin(j); 
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Static Schedule: " << std::chrono::duration<double>(end-start).count() << " s" << std::endl;

    // 动态调度 (Dynamic): 线程做完一个任务就去领下一个，适合负载不均衡
    start = std::chrono::high_resolution_clock::now();
    #pragma omp parallel for schedule(dynamic)
    for(int i=0; i<N; ++i) {
        double res = 0;
        for(int j=0; j<i*10000; ++j) res += std::sin(j);
    }
    end = std::chrono::high_resolution_clock::now();
    std::cout << "Dynamic Schedule: " << std::chrono::duration<double>(end-start).count() << " s" << std::endl;
}

int main() {
    const long num_steps = 100000000;
    
    std::cout << "Calculating PI with " << num_steps << " steps." << std::endl;
    std::cout << "Max Threads: " << omp_get_max_threads() << std::endl;

    // 1. Serial
    auto start = std::chrono::high_resolution_clock::now();
    double pi = calc_pi_serial(num_steps);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Serial: " << pi << " Time: " << std::chrono::duration<double>(end-start).count() << " s" << std::endl;

    // 2. OpenMP
    start = std::chrono::high_resolution_clock::now();
    pi = calc_pi_omp_reduction(num_steps);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "OpenMP: " << pi << " Time: " << std::chrono::duration<double>(end-start).count() << " s" << std::endl;

    // 3. 调度策略演示
    unbalanced_workload();

    return 0;
}
