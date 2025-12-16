/**
 * @file complexity_demo.cpp
 * @brief 复杂度分析示例
 * 
 * 编译：g++ -std=c++20 -O2 -Wall -o complexity_demo complexity_demo.cpp
 * 运行：./complexity_demo
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <unordered_set>
#include <iomanip>

//==============================================================================
// 1. 不同复杂度的函数示例
//==============================================================================

// O(1) - 常数时间
int constant_time(const std::vector<int>& arr) {
    if (arr.empty()) return 0;
    return arr[0] + arr[arr.size() - 1];
}

// O(log n) - 对数时间
int logarithmic_time(int n) {
    int count = 0;
    while (n > 1) {
        n /= 2;
        count++;
    }
    return count;
}

// O(n) - 线性时间
long long linear_time(const std::vector<int>& arr) {
    long long sum = 0;
    for (int x : arr) {
        sum += x;
    }
    return sum;
}

// O(n log n) - 线性对数时间
void nlogn_time(int n) {
    int operations = 0;
    for (int i = 1; i < n; i *= 2) {      // log n 次
        for (int j = 0; j < n; ++j) {      // n 次
            operations++;
        }
    }
    // std::cout << "Operations: " << operations << std::endl;
}

// O(n²) - 平方时间
int quadratic_time(const std::vector<int>& arr) {
    int pairs = 0;
    int n = arr.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] + arr[j] == 0) {
                pairs++;
            }
        }
    }
    return pairs;
}

//==============================================================================
// 2. 复杂度对比：查找重复元素
//==============================================================================

// 方法1：O(n²) 暴力查找
bool has_duplicate_slow(const std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] == arr[j]) return true;
        }
    }
    return false;
}

// 方法2：O(n) 哈希表
bool has_duplicate_fast(const std::vector<int>& arr) {
    std::unordered_set<int> seen;
    for (int x : arr) {
        if (seen.count(x)) return true;
        seen.insert(x);
    }
    return false;
}

//==============================================================================
// 3. 复杂度对比：求和 1 + 2 + ... + n
//==============================================================================

// 方法1：O(n) 循环
long long sum_loop(int n) {
    long long sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

// 方法2：O(1) 公式
long long sum_formula(int n) {
    return (long long)n * (n + 1) / 2;
}

//==============================================================================
// 4. 性能测量工具
//==============================================================================

template<typename Func>
double measure_time(Func f, int iterations = 1) {
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
        f();
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;
    return elapsed.count() / iterations;
}

//==============================================================================
// 5. 主函数：演示复杂度差异
//==============================================================================

int main() {
    std::cout << "===== 复杂度分析演示 =====" << std::endl << std::endl;
    
    // ========== 演示1：不同规模下 O(n²) vs O(n) ==========
    std::cout << "【演示1】查找重复元素 - O(n²) vs O(n)" << std::endl;
    std::cout << std::setw(10) << "n" 
              << std::setw(15) << "O(n²) ms" 
              << std::setw(15) << "O(n) ms" 
              << std::setw(15) << "加速比" << std::endl;
    std::cout << std::string(55, '-') << std::endl;
    
    for (int n : {1000, 5000, 10000, 20000}) {
        std::vector<int> arr(n);
        for (int i = 0; i < n; ++i) arr[i] = i;
        
        double slow_time = measure_time([&]() { has_duplicate_slow(arr); });
        double fast_time = measure_time([&]() { has_duplicate_fast(arr); });
        
        std::cout << std::setw(10) << n 
                  << std::setw(15) << std::fixed << std::setprecision(3) << slow_time
                  << std::setw(15) << fast_time
                  << std::setw(15) << slow_time / fast_time << "x" << std::endl;
    }
    
    std::cout << std::endl;
    
    // ========== 演示2：O(n) vs O(1) ==========
    std::cout << "【演示2】求和 1+2+...+n - O(n) vs O(1)" << std::endl;
    std::cout << std::setw(15) << "n" 
              << std::setw(15) << "O(n) ms" 
              << std::setw(15) << "O(1) ms" << std::endl;
    std::cout << std::string(45, '-') << std::endl;
    
    for (int n : {1000000, 10000000, 100000000}) {
        double loop_time = measure_time([&]() { sum_loop(n); }, 10);
        double formula_time = measure_time([&]() { sum_formula(n); }, 1000);
        
        std::cout << std::setw(15) << n 
                  << std::setw(15) << std::fixed << std::setprecision(3) << loop_time
                  << std::setw(15) << formula_time << std::endl;
    }
    
    std::cout << std::endl;
    
    // ========== 演示3：复杂度验证 ==========
    std::cout << "【演示3】验证 O(n log n) 增长" << std::endl;
    std::cout << std::setw(10) << "n" 
              << std::setw(15) << "时间 ms" 
              << std::setw(20) << "时间 / n log n" << std::endl;
    std::cout << std::string(45, '-') << std::endl;
    
    for (int n : {10000, 50000, 100000, 500000, 1000000}) {
        double time = measure_time([&]() { nlogn_time(n); }, 5);
        double normalized = time / (n * std::log2(n)) * 1e6;
        
        std::cout << std::setw(10) << n 
                  << std::setw(15) << std::fixed << std::setprecision(3) << time
                  << std::setw(20) << std::setprecision(6) << normalized << std::endl;
    }
    
    std::cout << "\n（如果是 O(n log n)，最后一列应该接近常数）" << std::endl;
    
    return 0;
}

