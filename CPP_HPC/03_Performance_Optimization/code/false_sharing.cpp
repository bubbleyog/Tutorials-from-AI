#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <chrono>
#include <new> // for hardware_destructive_interference_size

// 演示 False Sharing (伪共享) 现象
// 当多个线程修改位于同一个 Cache Line (通常 64 字节) 的不同变量时，
// 缓存一致性协议 (MESI) 会强制这些缓存行在核心间失效和同步，导致性能剧烈下降。

const int NUM_THREADS = 4;
const long long ITERATIONS = 100000000;

// 1. 存在伪共享的结构体
// 这些 atomic 变量紧挨着，极大概率在同一个 Cache Line 中
struct SharedData {
    std::atomic<long long> a{0};
    std::atomic<long long> b{0};
    std::atomic<long long> c{0};
    std::atomic<long long> d{0};
};

// 2. 消除伪共享的结构体
// 使用 alignas 强制每个变量独占一个 Cache Line
// C++17 引入了 std::hardware_destructive_interference_size
struct PaddedData {
    alignas(64) std::atomic<long long> a{0};
    alignas(64) std::atomic<long long> b{0};
    alignas(64) std::atomic<long long> c{0};
    alignas(64) std::atomic<long long> d{0};
};

void worker(std::atomic<long long>& var) {
    for (long long i = 0; i < ITERATIONS; ++i) {
        var.fetch_add(1, std::memory_order_relaxed);
    }
}

int main() {
    std::cout << "Threads: " << NUM_THREADS << std::endl;
    std::cout << "Iterations: " << ITERATIONS << std::endl;

    // Test False Sharing
    {
        SharedData data;
        auto start = std::chrono::high_resolution_clock::now();
        
        std::vector<std::thread> threads;
        threads.emplace_back(worker, std::ref(data.a));
        threads.emplace_back(worker, std::ref(data.b));
        threads.emplace_back(worker, std::ref(data.c));
        threads.emplace_back(worker, std::ref(data.d));
        
        for(auto& t : threads) t.join();
        
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        std::cout << "False Sharing Time: " << diff.count() << " s" << std::endl;
    }

    // Test Padding (No False Sharing)
    {
        PaddedData data;
        auto start = std::chrono::high_resolution_clock::now();
        
        std::vector<std::thread> threads;
        threads.emplace_back(worker, std::ref(data.a));
        threads.emplace_back(worker, std::ref(data.b));
        threads.emplace_back(worker, std::ref(data.c));
        threads.emplace_back(worker, std::ref(data.d));
        
        for(auto& t : threads) t.join();
        
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = end - start;
        std::cout << "Padded Time:        " << diff.count() << " s" << std::endl;
    }

    return 0;
}
