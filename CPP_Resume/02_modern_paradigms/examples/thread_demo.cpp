/**
 * @file thread_demo.cpp
 * @brief 并发编程入门示例
 * 
 * 编译：g++ -std=c++20 -Wall -pthread -o thread_demo thread_demo.cpp
 * 运行：./thread_demo
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <atomic>
#include <vector>
#include <queue>
#include <chrono>

// ============================================================
// 1. 创建线程
// ============================================================

void simple_function() {
    std::cout << "  [Thread] 简单函数在线程中执行\n";
    std::cout << "  [Thread] 线程 ID: " << std::this_thread::get_id() << "\n";
}

void demo_create_threads() {
    std::cout << "\n=== 创建线程 ===\n";
    
    std::cout << "主线程 ID: " << std::this_thread::get_id() << "\n";
    
    // 使用普通函数
    std::thread t1(simple_function);
    
    // 使用 Lambda
    std::thread t2([]() {
        std::cout << "  [Lambda Thread] Lambda 线程\n";
    });
    
    // 带参数
    std::thread t3([](int x, const std::string& msg) {
        std::cout << "  [Param Thread] " << msg << ": " << x << "\n";
    }, 42, "参数值");
    
    t1.join();
    t2.join();
    t3.join();
    
    std::cout << "所有线程已结束\n";
}

// ============================================================
// 2. 数据竞争问题
// ============================================================

int unsafe_counter = 0;
int safe_counter = 0;
std::mutex counter_mutex;

void increment_unsafe(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        ++unsafe_counter;  // 数据竞争！
    }
}

void increment_safe(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        std::lock_guard<std::mutex> lock(counter_mutex);
        ++safe_counter;
    }
}

void demo_data_race() {
    std::cout << "\n=== 数据竞争问题 ===\n";
    
    const int iterations = 100000;
    
    // 不安全版本
    unsafe_counter = 0;
    std::thread t1(increment_unsafe, iterations);
    std::thread t2(increment_unsafe, iterations);
    t1.join();
    t2.join();
    std::cout << "不安全计数器 (期望 " << iterations * 2 << "): " << unsafe_counter << "\n";
    
    // 安全版本
    safe_counter = 0;
    std::thread t3(increment_safe, iterations);
    std::thread t4(increment_safe, iterations);
    t3.join();
    t4.join();
    std::cout << "安全计数器 (期望 " << iterations * 2 << "): " << safe_counter << "\n";
}

// ============================================================
// 3. 互斥锁
// ============================================================

std::mutex print_mutex;

void safe_print(const std::string& msg) {
    std::lock_guard<std::mutex> lock(print_mutex);
    std::cout << msg << "\n";
}

void demo_mutex() {
    std::cout << "\n=== 互斥锁 ===\n";
    
    std::vector<std::thread> threads;
    
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([i]() {
            for (int j = 0; j < 3; ++j) {
                safe_print("  线程 " + std::to_string(i) + " 输出 " + std::to_string(j));
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        });
    }
    
    for (auto& t : threads) {
        t.join();
    }
}

// ============================================================
// 4. 条件变量
// ============================================================

std::mutex cv_mutex;
std::condition_variable cv;
bool ready = false;

void worker_thread(int id) {
    std::unique_lock<std::mutex> lock(cv_mutex);
    cv.wait(lock, []{ return ready; });
    std::cout << "  工作线程 " << id << " 收到信号，开始工作\n";
}

void demo_condition_variable() {
    std::cout << "\n=== 条件变量 ===\n";
    
    ready = false;
    
    std::vector<std::thread> workers;
    for (int i = 0; i < 3; ++i) {
        workers.emplace_back(worker_thread, i);
    }
    
    std::cout << "主线程：准备发送信号...\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    {
        std::lock_guard<std::mutex> lock(cv_mutex);
        ready = true;
    }
    cv.notify_all();
    
    for (auto& w : workers) {
        w.join();
    }
}

// ============================================================
// 5. 生产者-消费者
// ============================================================

std::queue<int> buffer;
std::mutex buffer_mutex;
std::condition_variable buffer_cv;
bool producer_done = false;

void producer(int count) {
    for (int i = 0; i < count; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        {
            std::lock_guard<std::mutex> lock(buffer_mutex);
            buffer.push(i);
            std::cout << "  [生产者] 生产: " << i << "\n";
        }
        buffer_cv.notify_one();
    }
    
    {
        std::lock_guard<std::mutex> lock(buffer_mutex);
        producer_done = true;
    }
    buffer_cv.notify_all();
}

void consumer(int id) {
    while (true) {
        std::unique_lock<std::mutex> lock(buffer_mutex);
        buffer_cv.wait(lock, []{ return !buffer.empty() || producer_done; });
        
        if (buffer.empty() && producer_done) {
            break;
        }
        
        int value = buffer.front();
        buffer.pop();
        lock.unlock();
        
        std::cout << "  [消费者 " << id << "] 消费: " << value << "\n";
    }
}

void demo_producer_consumer() {
    std::cout << "\n=== 生产者-消费者 ===\n";
    
    producer_done = false;
    while (!buffer.empty()) buffer.pop();
    
    std::thread prod(producer, 5);
    std::thread cons1(consumer, 1);
    std::thread cons2(consumer, 2);
    
    prod.join();
    cons1.join();
    cons2.join();
}

// ============================================================
// 6. async 和 future
// ============================================================

int compute(int x) {
    std::cout << "  [Async] 开始计算 " << x << "^2\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    return x * x;
}

void demo_async_future() {
    std::cout << "\n=== async 和 future ===\n";
    
    // 异步启动任务
    std::future<int> f1 = std::async(std::launch::async, compute, 5);
    std::future<int> f2 = std::async(std::launch::async, compute, 7);
    
    std::cout << "任务已启动，做其他工作...\n";
    
    // 获取结果（会阻塞等待）
    int result1 = f1.get();
    int result2 = f2.get();
    
    std::cout << "结果: 5^2 = " << result1 << ", 7^2 = " << result2 << "\n";
}

// ============================================================
// 7. promise
// ============================================================

void worker_with_promise(std::promise<int>& prom) {
    std::cout << "  [Promise Worker] 开始工作...\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    prom.set_value(42);
    std::cout << "  [Promise Worker] 已设置结果\n";
}

void demo_promise() {
    std::cout << "\n=== promise ===\n";
    
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();
    
    std::thread t(worker_with_promise, std::ref(prom));
    
    std::cout << "等待结果...\n";
    int result = fut.get();
    std::cout << "收到结果: " << result << "\n";
    
    t.join();
}

// ============================================================
// 8. 原子操作
// ============================================================

std::atomic<int> atomic_counter{0};

void increment_atomic(int iterations) {
    for (int i = 0; i < iterations; ++i) {
        ++atomic_counter;  // 原子操作，无需锁
    }
}

void demo_atomic() {
    std::cout << "\n=== 原子操作 ===\n";
    
    const int iterations = 100000;
    atomic_counter = 0;
    
    std::thread t1(increment_atomic, iterations);
    std::thread t2(increment_atomic, iterations);
    
    t1.join();
    t2.join();
    
    std::cout << "原子计数器 (期望 " << iterations * 2 << "): " << atomic_counter << "\n";
}

// ============================================================
// 9. 硬件并发
// ============================================================

void demo_hardware_concurrency() {
    std::cout << "\n=== 硬件并发信息 ===\n";
    
    unsigned int n = std::thread::hardware_concurrency();
    std::cout << "硬件并发线程数: " << n << "\n";
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================\n";
    std::cout << "        并发编程入门示例\n";
    std::cout << "========================================\n";
    
    demo_create_threads();
    demo_data_race();
    demo_mutex();
    demo_condition_variable();
    demo_producer_consumer();
    demo_async_future();
    demo_promise();
    demo_atomic();
    demo_hardware_concurrency();
    
    std::cout << "\n========================================\n";
    std::cout << "            示例结束\n";
    std::cout << "========================================\n";
    
    return 0;
}

