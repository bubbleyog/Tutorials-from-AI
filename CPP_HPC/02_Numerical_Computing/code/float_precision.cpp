#include <iostream>
#include <iomanip>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

// 演示浮点数求和的精度问题
void demonstrate_summation() {
    std::cout << "\n=== Summation Precision Test ===" << std::endl;
    
    // 我们尝试将 0.0000001 加 10,000,000 次，结果应该是 1.0
    float small_val = 1e-7f;
    int N = 10000000;
    
    // 方法 1: 朴素累加
    float sum_naive = 0.0f;
    for (int i = 0; i < N; ++i) {
        sum_naive += small_val;
    }
    
    // 方法 2: 使用 double 进行累加 (推荐)
    double sum_double = 0.0;
    for (int i = 0; i < N; ++i) {
        sum_double += static_cast<double>(small_val);
    }
    
    // 方法 3: Kahan Summation Algorithm (补偿求和)
    float sum_kahan = 0.0f;
    float c = 0.0f; // 运行过程中的补偿值
    for (int i = 0; i < N; ++i) {
        float y = small_val - c;
        float t = sum_kahan + y;
        c = (t - sum_kahan) - y;
        sum_kahan = t;
    }

    std::cout << std::fixed << std::setprecision(10);
    std::cout << "Expected:   1.0000000000" << std::endl;
    std::cout << "Naive float:" << sum_naive << " (Error: " << std::abs(sum_naive - 1.0f) << ")" << std::endl;
    std::cout << "Double acc: " << sum_double << " (Error: " << std::abs(sum_double - 1.0) << ")" << std::endl;
    std::cout << "Kahan sum:  " << sum_kahan << " (Error: " << std::abs(sum_kahan - 1.0f) << ")" << std::endl;
}

// 演示 catastrophic cancellation (大数减小数导致的精度丢失)
void demonstrate_cancellation() {
    std::cout << "\n=== Catastrophic Cancellation Test ===" << std::endl;
    
    // 计算 sqrt(x + 1) - sqrt(x) 当 x 很大时
    // 理论上这等于 1 / (sqrt(x+1) + sqrt(x))
    
    float x = 1e7f;
    
    float val1 = std::sqrt(x + 1.0f) - std::sqrt(x);
    float val2 = 1.0f / (std::sqrt(x + 1.0f) + std::sqrt(x));
    
    std::cout << "x = " << x << std::endl;
    std::cout << "Direct sub: " << std::scientific << val1 << std::endl;
    std::cout << "Algebraic:  " << val2 << std::endl;
    std::cout << "Difference: " << val1 - val2 << std::endl;
}

int main() {
    demonstrate_summation();
    demonstrate_cancellation();
    return 0;
}
