/**
 * @file recursion_demo.cpp
 * @brief 递归算法示例
 * 
 * 编译：g++ -std=c++20 -O2 -Wall -o recursion_demo recursion_demo.cpp
 * 运行：./recursion_demo
 */

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <unordered_map>
#include <functional>

//==============================================================================
// 辅助函数
//==============================================================================

template<typename Container>
void print(const std::string& label, const Container& c) {
    std::cout << label << ": [";
    bool first = true;
    for (const auto& x : c) {
        if (!first) std::cout << ", ";
        std::cout << x;
        first = false;
    }
    std::cout << "]" << std::endl;
}

//==============================================================================
// 1. 基础递归
//==============================================================================

// 阶乘
long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 斐波那契（朴素递归 - 低效）
long long fib_naive(int n) {
    if (n <= 1) return n;
    return fib_naive(n - 1) + fib_naive(n - 2);
}

// 求和 1 + 2 + ... + n
int sum_recursive(int n) {
    if (n == 0) return 0;
    return n + sum_recursive(n - 1);
}

// 数组求和
int array_sum(const std::vector<int>& arr, int index = 0) {
    if (index >= (int)arr.size()) return 0;
    return arr[index] + array_sum(arr, index + 1);
}

// 反转字符串
std::string reverse_string(const std::string& s) {
    if (s.length() <= 1) return s;
    return reverse_string(s.substr(1)) + s[0];
}

// 幂运算 x^n
double power(double x, int n) {
    if (n == 0) return 1;
    if (n < 0) return 1 / power(x, -n);
    if (n % 2 == 0) {
        double half = power(x, n / 2);
        return half * half;
    }
    return x * power(x, n - 1);
}

//==============================================================================
// 2. 记忆化递归
//==============================================================================

// 斐波那契（带记忆化）
std::unordered_map<int, long long> fib_memo;

long long fib_memoized(int n) {
    if (n <= 1) return n;
    if (fib_memo.count(n)) return fib_memo[n];
    fib_memo[n] = fib_memoized(n - 1) + fib_memoized(n - 2);
    return fib_memo[n];
}

// 使用 vector 的记忆化
long long fib_memo_vec(int n, std::vector<long long>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = fib_memo_vec(n - 1, memo) + fib_memo_vec(n - 2, memo);
    return memo[n];
}

//==============================================================================
// 3. 经典递归问题
//==============================================================================

// 汉诺塔
void hanoi(int n, char from, char to, char aux, std::vector<std::string>& moves) {
    if (n == 1) {
        moves.push_back(std::string("Move disk 1 from ") + from + " to " + to);
        return;
    }
    hanoi(n - 1, from, aux, to, moves);
    moves.push_back(std::string("Move disk ") + std::to_string(n) + " from " + from + " to " + to);
    hanoi(n - 1, aux, to, from, moves);
}

// 生成全排列
void permute_helper(std::vector<int>& nums, int start, std::vector<std::vector<int>>& result) {
    if (start == (int)nums.size()) {
        result.push_back(nums);
        return;
    }
    for (int i = start; i < (int)nums.size(); ++i) {
        std::swap(nums[start], nums[i]);
        permute_helper(nums, start + 1, result);
        std::swap(nums[start], nums[i]);  // 回溯
    }
}

std::vector<std::vector<int>> permutations(std::vector<int> nums) {
    std::vector<std::vector<int>> result;
    permute_helper(nums, 0, result);
    return result;
}

// 生成子集
void subsets_helper(const std::vector<int>& nums, int index, 
                    std::vector<int>& current, std::vector<std::vector<int>>& result) {
    result.push_back(current);
    for (int i = index; i < (int)nums.size(); ++i) {
        current.push_back(nums[i]);
        subsets_helper(nums, i + 1, current, result);
        current.pop_back();  // 回溯
    }
}

std::vector<std::vector<int>> subsets(const std::vector<int>& nums) {
    std::vector<std::vector<int>> result;
    std::vector<int> current;
    subsets_helper(nums, 0, current, result);
    return result;
}

// 二分查找（递归版）
int binary_search_recursive(const std::vector<int>& arr, int target, int left, int right) {
    if (left > right) return -1;
    int mid = left + (right - left) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) {
        return binary_search_recursive(arr, target, mid + 1, right);
    }
    return binary_search_recursive(arr, target, left, mid - 1);
}

//==============================================================================
// 4. 尾递归示例
//==============================================================================

// 普通递归阶乘
long long factorial_normal(int n) {
    if (n <= 1) return 1;
    return n * factorial_normal(n - 1);
}

// 尾递归阶乘
long long factorial_tail(int n, long long acc = 1) {
    if (n <= 1) return acc;
    return factorial_tail(n - 1, n * acc);
}

// 尾递归斐波那契
long long fib_tail(int n, long long a = 0, long long b = 1) {
    if (n == 0) return a;
    if (n == 1) return b;
    return fib_tail(n - 1, b, a + b);
}

//==============================================================================
// 主函数
//==============================================================================

int main() {
    std::cout << "===== 递归算法示例 =====" << std::endl;
    
    // ========== 1. 基础递归 ==========
    std::cout << "\n【1. 基础递归】" << std::endl;
    
    std::cout << "factorial(5) = " << factorial(5) << std::endl;
    std::cout << "factorial(10) = " << factorial(10) << std::endl;
    
    std::cout << "sum_recursive(10) = " << sum_recursive(10) << std::endl;
    
    std::vector<int> arr = {1, 2, 3, 4, 5};
    std::cout << "array_sum({1,2,3,4,5}) = " << array_sum(arr) << std::endl;
    
    std::cout << "reverse_string(\"hello\") = " << reverse_string("hello") << std::endl;
    
    std::cout << "power(2, 10) = " << power(2, 10) << std::endl;
    std::cout << "power(2, -3) = " << power(2, -3) << std::endl;
    
    // ========== 2. 斐波那契：朴素 vs 记忆化 ==========
    std::cout << "\n【2. 斐波那契：朴素 vs 记忆化】" << std::endl;
    
    // 朴素递归（小数字）
    std::cout << "fib_naive(20) = ";
    auto start = std::chrono::high_resolution_clock::now();
    long long result = fib_naive(20);
    auto end = std::chrono::high_resolution_clock::now();
    auto naive_time = std::chrono::duration<double, std::milli>(end - start).count();
    std::cout << result << " (耗时: " << naive_time << " ms)" << std::endl;
    
    // 记忆化递归
    std::cout << "fib_memoized(40) = ";
    fib_memo.clear();
    start = std::chrono::high_resolution_clock::now();
    result = fib_memoized(40);
    end = std::chrono::high_resolution_clock::now();
    auto memo_time = std::chrono::duration<double, std::milli>(end - start).count();
    std::cout << result << " (耗时: " << memo_time << " ms)" << std::endl;
    
    // 尾递归
    std::cout << "fib_tail(40) = ";
    start = std::chrono::high_resolution_clock::now();
    result = fib_tail(40);
    end = std::chrono::high_resolution_clock::now();
    auto tail_time = std::chrono::duration<double, std::milli>(end - start).count();
    std::cout << result << " (耗时: " << tail_time << " ms)" << std::endl;
    
    // ========== 3. 汉诺塔 ==========
    std::cout << "\n【3. 汉诺塔 (n=3)】" << std::endl;
    std::vector<std::string> moves;
    hanoi(3, 'A', 'C', 'B', moves);
    for (const auto& move : moves) {
        std::cout << "  " << move << std::endl;
    }
    std::cout << "总共 " << moves.size() << " 步" << std::endl;
    
    // ========== 4. 全排列 ==========
    std::cout << "\n【4. 全排列 {1, 2, 3}】" << std::endl;
    auto perms = permutations({1, 2, 3});
    for (const auto& perm : perms) {
        std::cout << "  [";
        for (int i = 0; i < (int)perm.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << perm[i];
        }
        std::cout << "]" << std::endl;
    }
    std::cout << "共 " << perms.size() << " 种排列" << std::endl;
    
    // ========== 5. 子集 ==========
    std::cout << "\n【5. 子集 {1, 2, 3}】" << std::endl;
    auto subs = subsets({1, 2, 3});
    for (const auto& sub : subs) {
        std::cout << "  {";
        for (int i = 0; i < (int)sub.size(); ++i) {
            if (i > 0) std::cout << ", ";
            std::cout << sub[i];
        }
        std::cout << "}" << std::endl;
    }
    std::cout << "共 " << subs.size() << " 个子集" << std::endl;
    
    // ========== 6. 递归二分查找 ==========
    std::cout << "\n【6. 递归二分查找】" << std::endl;
    std::vector<int> sorted = {1, 3, 5, 7, 9, 11, 13, 15};
    print("有序数组", sorted);
    std::cout << "查找 7: 位置 " << binary_search_recursive(sorted, 7, 0, sorted.size() - 1) << std::endl;
    std::cout << "查找 6: 位置 " << binary_search_recursive(sorted, 6, 0, sorted.size() - 1) << std::endl;
    
    // ========== 7. 尾递归 vs 普通递归 ==========
    std::cout << "\n【7. 尾递归阶乘】" << std::endl;
    std::cout << "factorial_normal(15) = " << factorial_normal(15) << std::endl;
    std::cout << "factorial_tail(15) = " << factorial_tail(15) << std::endl;
    
    std::cout << "\n===== 完成 =====" << std::endl;
    return 0;
}

