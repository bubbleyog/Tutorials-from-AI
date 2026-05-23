#include <iostream>
#include <vector>
#include <thread>
#include <future>
#include <random>
#include <atomic>
#include <cmath>

// 使用 std::thread 和 std::async 进行并行蒙特卡洛模拟
// 计算 PI: 在正方形内随机撒点，落在内切圆内的比例 * 4

// 任务函数：撒 N 个点，返回落在圆内的点数
long long monte_carlo_pi_task(long long num_samples) {
    long long inside_circle = 0;
    // 每个线程需要自己的随机数生成器，否则会有锁竞争
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);

    for (long long i = 0; i < num_samples; ++i) {
        double x = dis(gen);
        double y = dis(gen);
        if (x*x + y*y <= 1.0) {
            inside_circle++;
        }
    }
    return inside_circle;
}

int main() {
    long long total_samples = 100000000; // 1亿个点
    int num_threads = std::thread::hardware_concurrency();
    if (num_threads == 0) num_threads = 4;

    std::cout << "Monte Carlo PI estimation" << std::endl;
    std::cout << "Total Samples: " << total_samples << std::endl;
    std::cout << "Threads: " << num_threads << std::endl;

    // 方法 1: 使用 std::thread + atomic (手动管理)
    // 注意：这里用 atomic 汇总可能会有轻微性能损耗，但比 mutex 好
    // 更好的做法是每个线程返回局部结果，最后主线程汇总 (Reduction)
    std::cout << "\n--- Method 1: std::thread + atomic ---" << std::endl;
    auto start1 = std::chrono::high_resolution_clock::now();
    
    std::atomic<long long> global_inside{0};
    std::vector<std::thread> threads;
    long long samples_per_thread = total_samples / num_threads;

    for(int i=0; i<num_threads; ++i) {
        threads.emplace_back([&, samples_per_thread]() {
            long long local_count = monte_carlo_pi_task(samples_per_thread);
            global_inside += local_count; // 原子加
        });
    }

    for(auto& t : threads) t.join();

    auto end1 = std::chrono::high_resolution_clock::now();
    double pi1 = 4.0 * global_inside / total_samples;
    std::cout << "PI: " << pi1 << std::endl;
    std::cout << "Time: " << std::chrono::duration<double>(end1 - start1).count() << " s" << std::endl;


    // 方法 2: 使用 std::async (更高级的抽象)
    // 类似于 OpenMP 的任务并行，或者 Python 的 ThreadPoolExecutor
    std::cout << "\n--- Method 2: std::async (Futures) ---" << std::endl;
    auto start2 = std::chrono::high_resolution_clock::now();
    
    std::vector<std::future<long long>> futures;
    for(int i=0; i<num_threads; ++i) {
        // std::launch::async 强制开启新线程
        futures.push_back(std::async(std::launch::async, monte_carlo_pi_task, samples_per_thread));
    }

    long long total_inside_async = 0;
    for(auto& f : futures) {
        total_inside_async += f.get(); // 获取结果，如果没算完会阻塞
    }

    auto end2 = std::chrono::high_resolution_clock::now();
    double pi2 = 4.0 * total_inside_async / total_samples;
    std::cout << "PI: " << pi2 << std::endl;
    std::cout << "Time: " << std::chrono::duration<double>(end2 - start2).count() << " s" << std::endl;

    return 0;
}
