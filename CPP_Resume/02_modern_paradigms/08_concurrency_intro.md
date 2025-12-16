# 2.8 并发编程入门

## 📖 本节概述

并发编程是现代软件开发的重要主题。C++11 引入了标准的线程库，使得跨平台的多线程编程成为可能。本节将介绍线程、互斥锁、条件变量和异步任务的基础知识。

---

## 1. 为什么需要并发

### 1.1 并发的优势

- **利用多核**：现代 CPU 都是多核的，并发可以充分利用硬件
- **提高响应性**：GUI 应用中，后台任务不阻塞界面
- **提高吞吐量**：服务器可以同时处理多个请求

### 1.2 并发 vs 并行

```
并发（Concurrency）：多个任务交替执行，看起来同时进行
并行（Parallelism）：多个任务真正同时执行（需要多核/多CPU）

单核 CPU 上只能并发，不能并行
多核 CPU 可以同时并发和并行
```

---

## 2. std::thread

### 2.1 创建线程

```cpp
#include <thread>
#include <iostream>

// 普通函数
void hello() {
    std::cout << "Hello from thread!" << std::endl;
}

// 带参数的函数
void print_message(const std::string& msg, int n) {
    for (int i = 0; i < n; ++i) {
        std::cout << msg << std::endl;
    }
}

int main() {
    // 创建并启动线程
    std::thread t1(hello);
    
    // 带参数
    std::thread t2(print_message, "Hello", 3);
    
    // Lambda
    std::thread t3([]() {
        std::cout << "Lambda thread!" << std::endl;
    });
    
    // 等待线程结束
    t1.join();
    t2.join();
    t3.join();
    
    return 0;
}
```

### 2.2 join 和 detach

```cpp
void demo_join_detach() {
    std::thread t([]() {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        std::cout << "Thread finished" << std::endl;
    });
    
    // 选项1：join - 等待线程结束
    t.join();  // 阻塞直到线程完成
    
    // 选项2：detach - 分离线程
    // t.detach();  // 线程在后台运行，无法再 join
    
    // ⚠️ 必须选择一个！
    // 如果 thread 对象销毁时既没有 join 也没有 detach，程序会调用 std::terminate
}

// RAII 包装器
class ThreadGuard {
    std::thread& t_;
public:
    explicit ThreadGuard(std::thread& t) : t_(t) {}
    ~ThreadGuard() {
        if (t_.joinable()) {
            t_.join();
        }
    }
    ThreadGuard(const ThreadGuard&) = delete;
    ThreadGuard& operator=(const ThreadGuard&) = delete;
};

// C++20 std::jthread 自动 join
void demo_jthread() {
    std::jthread t([]() {
        std::cout << "jthread!" << std::endl;
    });
    // 离开作用域时自动 join
}
```

### 2.3 传递参数

```cpp
void by_value(int x) { x = 100; }
void by_ref(int& x) { x = 100; }

void demo_parameters() {
    int value = 10;
    
    // 默认按值传递
    std::thread t1(by_value, value);
    t1.join();
    // value 仍然是 10
    
    // 引用传递需要 std::ref
    std::thread t2(by_ref, std::ref(value));
    t2.join();
    // value 现在是 100
    
    // ⚠️ 小心悬垂引用
    // std::thread t3(by_ref, std::ref(local_var));
    // t3.detach();  // 危险！local_var 可能已销毁
}
```

### 2.4 线程信息

```cpp
void demo_thread_info() {
    // 当前线程 ID
    std::thread::id this_id = std::this_thread::get_id();
    std::cout << "Main thread ID: " << this_id << std::endl;
    
    // 硬件并发数
    unsigned int n = std::thread::hardware_concurrency();
    std::cout << "Hardware concurrency: " << n << std::endl;
    
    std::thread t([this_id]() {
        std::cout << "Worker thread ID: " << std::this_thread::get_id() << std::endl;
    });
    
    // 获取线程 ID
    std::cout << "Thread t ID: " << t.get_id() << std::endl;
    
    t.join();
}
```

---

## 3. 互斥锁 (Mutex)

### 3.1 数据竞争问题

```cpp
int counter = 0;

void increment_unsafe() {
    for (int i = 0; i < 100000; ++i) {
        ++counter;  // ❌ 数据竞争！
    }
}

void demo_race_condition() {
    std::thread t1(increment_unsafe);
    std::thread t2(increment_unsafe);
    
    t1.join();
    t2.join();
    
    // counter 可能不是 200000！
    std::cout << "Counter: " << counter << std::endl;
}
```

### 3.2 std::mutex

```cpp
#include <mutex>

int counter = 0;
std::mutex mtx;

void increment_safe() {
    for (int i = 0; i < 100000; ++i) {
        mtx.lock();
        ++counter;
        mtx.unlock();
    }
}

// ❌ 问题：如果中间抛出异常，锁不会释放
```

### 3.3 std::lock_guard（推荐）

```cpp
void increment_with_guard() {
    for (int i = 0; i < 100000; ++i) {
        std::lock_guard<std::mutex> lock(mtx);  // 构造时加锁
        ++counter;
    }  // 析构时自动解锁，即使抛出异常
}

// C++17：可以省略模板参数
void increment_cpp17() {
    std::lock_guard lock(mtx);  // CTAD
    ++counter;
}
```

### 3.4 std::unique_lock（更灵活）

```cpp
void demo_unique_lock() {
    std::unique_lock<std::mutex> lock(mtx);
    
    // 可以手动解锁
    lock.unlock();
    
    // 可以重新加锁
    lock.lock();
    
    // 尝试加锁
    if (lock.try_lock()) {
        // 成功获取锁
    }
    
    // 延迟加锁
    std::unique_lock<std::mutex> lock2(mtx, std::defer_lock);
    // ... 做一些事情 ...
    lock2.lock();  // 稍后加锁
    
    // 可以移动
    std::unique_lock<std::mutex> lock3 = std::move(lock2);
}
```

### 3.5 std::scoped_lock（C++17，多锁）

```cpp
std::mutex mtx1, mtx2;

void demo_scoped_lock() {
    // 同时锁定多个 mutex，避免死锁
    std::scoped_lock lock(mtx1, mtx2);
    
    // 临界区
}

// C++17 之前使用 std::lock
void demo_std_lock() {
    std::unique_lock<std::mutex> lock1(mtx1, std::defer_lock);
    std::unique_lock<std::mutex> lock2(mtx2, std::defer_lock);
    
    std::lock(lock1, lock2);  // 同时加锁，避免死锁
}
```

### 3.6 其他 Mutex 类型

```cpp
// 递归互斥锁：同一线程可以多次加锁
std::recursive_mutex rmtx;

// 带超时的互斥锁
std::timed_mutex tmtx;
if (tmtx.try_lock_for(std::chrono::milliseconds(100))) {
    // 获取锁成功
    tmtx.unlock();
}

// 共享互斥锁（读写锁）
#include <shared_mutex>
std::shared_mutex smtx;

// 独占锁（写锁）
std::unique_lock<std::shared_mutex> write_lock(smtx);

// 共享锁（读锁）
std::shared_lock<std::shared_mutex> read_lock(smtx);
```

---

## 4. 条件变量

### 4.1 基本用法

```cpp
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void worker() {
    std::unique_lock<std::mutex> lock(mtx);
    
    // 等待条件满足
    cv.wait(lock, []{ return ready; });
    // 等价于：
    // while (!ready) cv.wait(lock);
    
    std::cout << "Worker: ready is true" << std::endl;
}

void signaler() {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    {
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
    }
    
    cv.notify_one();  // 通知一个等待的线程
    // cv.notify_all();  // 通知所有等待的线程
}

void demo() {
    std::thread t1(worker);
    std::thread t2(signaler);
    
    t1.join();
    t2.join();
}
```

### 4.2 生产者-消费者模式

```cpp
#include <queue>

std::queue<int> buffer;
std::mutex mtx;
std::condition_variable cv_not_empty;
std::condition_variable cv_not_full;
const size_t MAX_SIZE = 10;

void producer(int id) {
    for (int i = 0; i < 20; ++i) {
        std::unique_lock<std::mutex> lock(mtx);
        
        // 等待缓冲区不满
        cv_not_full.wait(lock, []{ return buffer.size() < MAX_SIZE; });
        
        buffer.push(i);
        std::cout << "Producer " << id << " produced " << i << std::endl;
        
        lock.unlock();
        cv_not_empty.notify_one();
        
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void consumer(int id) {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        
        // 等待缓冲区不空
        cv_not_empty.wait(lock, []{ return !buffer.empty(); });
        
        int value = buffer.front();
        buffer.pop();
        std::cout << "Consumer " << id << " consumed " << value << std::endl;
        
        lock.unlock();
        cv_not_full.notify_one();
    }
}
```

---

## 5. 异步任务

### 5.1 std::async 和 std::future

```cpp
#include <future>

int compute(int x) {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    return x * x;
}

void demo_async() {
    // 异步启动任务
    std::future<int> result = std::async(std::launch::async, compute, 42);
    
    std::cout << "Doing other work..." << std::endl;
    
    // 获取结果（会阻塞等待）
    int value = result.get();
    std::cout << "Result: " << value << std::endl;
    
    // 启动策略
    // std::launch::async - 一定创建新线程
    // std::launch::deferred - 延迟执行，调用 get() 时执行
    // 默认是 async | deferred，由实现决定
    
    auto f1 = std::async(std::launch::async, compute, 10);
    auto f2 = std::async(std::launch::deferred, compute, 20);
}
```

### 5.2 std::promise

```cpp
void worker(std::promise<int>& prom) {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    prom.set_value(42);  // 设置结果
}

void demo_promise() {
    std::promise<int> prom;
    std::future<int> fut = prom.get_future();
    
    std::thread t(worker, std::ref(prom));
    
    std::cout << "Waiting for result..." << std::endl;
    int result = fut.get();  // 阻塞等待
    std::cout << "Got: " << result << std::endl;
    
    t.join();
}

// 异常传递
void worker_with_exception(std::promise<int>& prom) {
    try {
        throw std::runtime_error("Something went wrong");
    } catch (...) {
        prom.set_exception(std::current_exception());
    }
}
```

### 5.3 std::packaged_task

```cpp
void demo_packaged_task() {
    // 包装可调用对象
    std::packaged_task<int(int, int)> task([](int a, int b) {
        return a + b;
    });
    
    std::future<int> result = task.get_future();
    
    // 在另一个线程中执行
    std::thread t(std::move(task), 10, 20);
    
    std::cout << "Result: " << result.get() << std::endl;
    
    t.join();
}
```

### 5.4 等待多个 future

```cpp
void demo_wait_multiple() {
    std::vector<std::future<int>> futures;
    
    for (int i = 0; i < 5; ++i) {
        futures.push_back(std::async(std::launch::async, [i]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(100 * i));
            return i * i;
        }));
    }
    
    // 等待所有完成并获取结果
    for (auto& f : futures) {
        std::cout << f.get() << " ";
    }
    std::cout << std::endl;
}
```

---

## 6. 原子操作

### 6.1 std::atomic

```cpp
#include <atomic>

std::atomic<int> counter{0};

void increment() {
    for (int i = 0; i < 100000; ++i) {
        ++counter;  // 原子操作，无需锁
    }
}

void demo_atomic() {
    std::thread t1(increment);
    std::thread t2(increment);
    
    t1.join();
    t2.join();
    
    std::cout << "Counter: " << counter << std::endl;  // 一定是 200000
}
```

### 6.2 原子操作

```cpp
std::atomic<int> value{0};

void demo_atomic_ops() {
    // 基本操作
    value.store(10);              // 原子存储
    int x = value.load();         // 原子加载
    int y = value.exchange(20);   // 原子交换，返回旧值
    
    // 读-改-写
    value.fetch_add(5);           // 原子加
    value.fetch_sub(3);           // 原子减
    value.fetch_and(0xFF);        // 原子与
    value.fetch_or(0x100);        // 原子或
    
    // 比较并交换（CAS）
    int expected = 10;
    bool success = value.compare_exchange_strong(expected, 20);
    // 如果 value == expected，则 value = 20，返回 true
    // 否则 expected = value，返回 false
}
```

### 6.3 原子标志

```cpp
std::atomic_flag lock = ATOMIC_FLAG_INIT;

void spin_lock_example() {
    // 自旋锁
    while (lock.test_and_set(std::memory_order_acquire)) {
        // 忙等待
    }
    
    // 临界区
    
    lock.clear(std::memory_order_release);
}
```

---

## 7. C++20 新增特性

### 7.1 std::jthread

```cpp
#include <thread>

void demo_jthread() {
    // 自动 join
    std::jthread t1([]() {
        std::cout << "jthread 1" << std::endl;
    });
    
    // 支持取消
    std::jthread t2([](std::stop_token st) {
        while (!st.stop_requested()) {
            std::cout << "Working..." << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
        std::cout << "Stopped!" << std::endl;
    });
    
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    t2.request_stop();  // 请求停止
    
}  // 自动 join
```

### 7.2 std::latch 和 std::barrier

```cpp
#include <latch>
#include <barrier>

// latch：一次性倒计时
void demo_latch() {
    std::latch latch(3);
    
    auto worker = [&latch](int id) {
        std::cout << "Worker " << id << " done" << std::endl;
        latch.count_down();
    };
    
    std::thread t1(worker, 1);
    std::thread t2(worker, 2);
    std::thread t3(worker, 3);
    
    latch.wait();  // 等待计数归零
    std::cout << "All workers done" << std::endl;
    
    t1.join(); t2.join(); t3.join();
}

// barrier：可重用的同步点
void demo_barrier() {
    std::barrier barrier(3, []() noexcept {
        std::cout << "Phase complete" << std::endl;
    });
    
    auto worker = [&barrier](int id) {
        for (int phase = 0; phase < 3; ++phase) {
            std::cout << "Worker " << id << " phase " << phase << std::endl;
            barrier.arrive_and_wait();
        }
    };
    
    std::thread t1(worker, 1);
    std::thread t2(worker, 2);
    std::thread t3(worker, 3);
    
    t1.join(); t2.join(); t3.join();
}
```

### 7.3 std::semaphore

```cpp
#include <semaphore>

// 计数信号量
std::counting_semaphore<10> sem(3);  // 初始计数 3，最大 10

void demo_semaphore() {
    auto worker = [](int id) {
        sem.acquire();  // 获取许可
        std::cout << "Worker " << id << " acquired" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
        sem.release();  // 释放许可
    };
    
    std::vector<std::thread> threads;
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(worker, i);
    }
    
    for (auto& t : threads) t.join();
}

// 二元信号量（类似 mutex）
std::binary_semaphore bsem(1);
```

---

## 8. 最佳实践

### 8.1 避免数据竞争

```cpp
// ✅ 使用互斥锁保护共享数据
class ThreadSafeCounter {
    int value_ = 0;
    mutable std::mutex mtx_;
    
public:
    void increment() {
        std::lock_guard lock(mtx_);
        ++value_;
    }
    
    int get() const {
        std::lock_guard lock(mtx_);
        return value_;
    }
};

// ✅ 使用原子类型
std::atomic<int> atomic_counter{0};

// ✅ 避免共享数据
// 每个线程使用自己的数据，最后合并
```

### 8.2 避免死锁

```cpp
// ✅ 使用 std::scoped_lock 同时锁定多个 mutex
std::scoped_lock lock(mtx1, mtx2);

// ✅ 总是按相同顺序获取锁
// 如果必须分开获取，使用 std::lock

// ❌ 避免持有锁时调用用户代码
// 用户代码可能尝试获取其他锁
```

### 8.3 减少锁的范围

```cpp
// ❌ 锁范围过大
void bad() {
    std::lock_guard lock(mtx);
    prepare_data();      // 不需要锁
    modify_shared();     // 需要锁
    cleanup();           // 不需要锁
}

// ✅ 只锁必要的部分
void good() {
    prepare_data();
    {
        std::lock_guard lock(mtx);
        modify_shared();
    }
    cleanup();
}
```

---

## 📝 练习题

### 练习1：线程池
实现一个简单的线程池，支持提交任务并获取结果。

### 练习2：并发安全队列
实现一个线程安全的队列，支持多生产者多消费者。

### 练习3：读写锁保护的缓存
使用 `std::shared_mutex` 实现一个读写锁保护的缓存。

### 练习4：异步任务链
使用 `std::async` 实现任务链，后一个任务依赖前一个的结果。

---

## 💡 要点总结

1. **std::thread**：创建和管理线程，必须 join 或 detach
2. **std::mutex + lock_guard**：保护共享数据
3. **std::unique_lock**：更灵活的锁管理
4. **std::condition_variable**：线程间通信
5. **std::async/future**：异步任务
6. **std::atomic**：无锁原子操作
7. **C++20 增强**：jthread、latch、barrier、semaphore
8. **避免数据竞争和死锁**

---

## ⏭️ 下一章

[第三章：算法设计初步](../03_algorithm_design/README.md) - 学习基础算法和数据结构

