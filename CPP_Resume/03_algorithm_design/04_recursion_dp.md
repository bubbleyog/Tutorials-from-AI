# 3.4 递归与动态规划

## 📖 本节概述

递归和动态规划是解决复杂问题的重要工具。递归通过自我调用分解问题，动态规划通过存储子问题的解避免重复计算。本节将从基础开始，带你逐步掌握这两种核心技术。

---

## 1. 递归基础

### 1.1 什么是递归

递归是函数**直接或间接调用自身**的编程技术。

```cpp
// 经典例子：阶乘
int factorial(int n) {
    if (n <= 1) return 1;        // 基准情况（Base Case）
    return n * factorial(n - 1);  // 递归调用
}

// 调用过程：
// factorial(5)
// = 5 * factorial(4)
// = 5 * 4 * factorial(3)
// = 5 * 4 * 3 * factorial(2)
// = 5 * 4 * 3 * 2 * factorial(1)
// = 5 * 4 * 3 * 2 * 1
// = 120
```

### 1.2 递归三要素

1. **基准情况**（Base Case）：递归终止的条件
2. **递归关系**：如何将问题分解为子问题
3. **规模缩小**：每次调用问题规模必须减小

```cpp
// 斐波那契数列
int fib(int n) {
    // 1. 基准情况
    if (n <= 1) return n;
    
    // 2. 递归关系: fib(n) = fib(n-1) + fib(n-2)
    // 3. 规模缩小: n -> n-1, n-2
    return fib(n - 1) + fib(n - 2);
}
```

### 1.3 递归 vs 迭代

```cpp
// 递归版本
int sum_recursive(int n) {
    if (n == 0) return 0;
    return n + sum_recursive(n - 1);
}

// 迭代版本
int sum_iterative(int n) {
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}
```

| 特点 | 递归 | 迭代 |
|------|------|------|
| 代码简洁 | 通常更简洁 | 可能更冗长 |
| 内存开销 | 使用调用栈 | 通常更少 |
| 效率 | 可能有重复计算 | 通常更高 |
| 可读性 | 问题自然递归时更清晰 | 简单问题更直接 |

---

## 2. 递归经典问题

### 2.1 二分查找（递归版）

```cpp
int binary_search(const std::vector<int>& arr, int target, int left, int right) {
    if (left > right) return -1;  // 基准情况：未找到
    
    int mid = left + (right - left) / 2;
    
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) {
        return binary_search(arr, target, mid + 1, right);
    }
    return binary_search(arr, target, left, mid - 1);
}
```

### 2.2 归并排序（递归版）

```cpp
void merge_sort(std::vector<int>& arr, int left, int right) {
    if (left >= right) return;  // 基准情况
    
    int mid = left + (right - left) / 2;
    merge_sort(arr, left, mid);      // 排序左半
    merge_sort(arr, mid + 1, right); // 排序右半
    merge(arr, left, mid, right);    // 合并
}
```

### 2.3 汉诺塔

```cpp
void hanoi(int n, char from, char to, char aux) {
    if (n == 1) {
        std::cout << "Move disk 1 from " << from << " to " << to << std::endl;
        return;
    }
    
    hanoi(n - 1, from, aux, to);  // 将 n-1 个盘子从 from 移到 aux
    std::cout << "Move disk " << n << " from " << from << " to " << to << std::endl;
    hanoi(n - 1, aux, to, from);  // 将 n-1 个盘子从 aux 移到 to
}
```

### 2.4 生成全排列

```cpp
void permute(std::vector<int>& nums, int start, std::vector<std::vector<int>>& result) {
    if (start == nums.size()) {
        result.push_back(nums);
        return;
    }
    
    for (int i = start; i < nums.size(); ++i) {
        std::swap(nums[start], nums[i]);
        permute(nums, start + 1, result);
        std::swap(nums[start], nums[i]);  // 回溯
    }
}

std::vector<std::vector<int>> get_permutations(std::vector<int> nums) {
    std::vector<std::vector<int>> result;
    permute(nums, 0, result);
    return result;
}
```

### 2.5 生成子集

```cpp
void subsets(const std::vector<int>& nums, int index, 
             std::vector<int>& current, std::vector<std::vector<int>>& result) {
    result.push_back(current);
    
    for (int i = index; i < nums.size(); ++i) {
        current.push_back(nums[i]);
        subsets(nums, i + 1, current, result);
        current.pop_back();  // 回溯
    }
}
```

---

## 3. 递归的问题与优化

### 3.1 重复计算问题

```cpp
// 朴素斐波那契：大量重复计算
int fib_naive(int n) {
    if (n <= 1) return n;
    return fib_naive(n - 1) + fib_naive(n - 2);
}

// fib(5) 的调用树：
//           fib(5)
//          /      \
//      fib(4)    fib(3)
//      /    \     /   \
//   fib(3) fib(2) fib(2) fib(1)
//    ...
// fib(2) 被计算了多次！
// 时间复杂度 O(2^n)
```

### 3.2 记忆化递归

```cpp
// 使用哈希表存储已计算的结果
std::unordered_map<int, long long> memo;

long long fib_memo(int n) {
    if (n <= 1) return n;
    
    if (memo.find(n) != memo.end()) {
        return memo[n];  // 直接返回缓存结果
    }
    
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2);
    return memo[n];
}

// 时间复杂度降为 O(n)
```

### 3.3 尾递归优化

```cpp
// 普通递归：每次调用都需要保存状态
int factorial_normal(int n) {
    if (n <= 1) return 1;
    return n * factorial_normal(n - 1);  // 返回后还需要计算
}

// 尾递归：递归调用是最后一步操作
int factorial_tail(int n, int acc = 1) {
    if (n <= 1) return acc;
    return factorial_tail(n - 1, n * acc);  // 直接返回递归结果
}

// 注意：C++ 标准不保证尾递归优化，但编译器（如 GCC -O2）可能优化
```

---

## 4. 动态规划入门

### 4.1 什么是动态规划

动态规划（Dynamic Programming，DP）是一种**通过存储子问题的解来避免重复计算**的算法技术。

**适用条件**：
1. **最优子结构**：问题的最优解包含子问题的最优解
2. **重叠子问题**：子问题会被重复计算

### 4.2 从递归到 DP

```cpp
// 1. 朴素递归 O(2^n)
int fib_recursive(int n) {
    if (n <= 1) return n;
    return fib_recursive(n - 1) + fib_recursive(n - 2);
}

// 2. 记忆化递归（自顶向下）O(n)
long long fib_memo(int n, std::vector<long long>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    return memo[n];
}

// 3. 动态规划（自底向上）O(n) 时间，O(n) 空间
long long fib_dp(int n) {
    if (n <= 1) return n;
    std::vector<long long> dp(n + 1);
    dp[0] = 0;
    dp[1] = 1;
    for (int i = 2; i <= n; ++i) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}

// 4. 空间优化 DP：O(n) 时间，O(1) 空间
long long fib_optimized(int n) {
    if (n <= 1) return n;
    long long prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; ++i) {
        long long curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

### 4.3 DP 解题步骤

1. **定义状态**：`dp[i]` 代表什么？
2. **状态转移方程**：`dp[i]` 如何从其他状态得到？
3. **初始化**：基础情况的值
4. **计算顺序**：确保计算 `dp[i]` 时依赖的状态已计算
5. **返回结果**：通常是 `dp[n]` 或某个状态

---

## 5. 一维 DP 经典问题

### 5.1 爬楼梯

> 每次可以爬 1 或 2 个台阶，问爬到第 n 阶有多少种方法？

```cpp
// 状态：dp[i] = 爬到第 i 阶的方法数
// 转移：dp[i] = dp[i-1] + dp[i-2]
// 初始：dp[1] = 1, dp[2] = 2

int climb_stairs(int n) {
    if (n <= 2) return n;
    
    int prev2 = 1, prev1 = 2;
    for (int i = 3; i <= n; ++i) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

### 5.2 最大子数组和（Kadane 算法）

> 找出数组中和最大的连续子数组。

```cpp
// 状态：dp[i] = 以 nums[i] 结尾的最大子数组和
// 转移：dp[i] = max(nums[i], dp[i-1] + nums[i])

int max_subarray(const std::vector<int>& nums) {
    int max_sum = nums[0];
    int curr_sum = nums[0];
    
    for (size_t i = 1; i < nums.size(); ++i) {
        curr_sum = std::max(nums[i], curr_sum + nums[i]);
        max_sum = std::max(max_sum, curr_sum);
    }
    
    return max_sum;
}
```

### 5.3 打家劫舍

> 不能偷相邻的房子，求最大收益。

```cpp
// 状态：dp[i] = 偷前 i 个房子的最大收益
// 转移：dp[i] = max(dp[i-1], dp[i-2] + nums[i])

int rob(const std::vector<int>& nums) {
    if (nums.empty()) return 0;
    if (nums.size() == 1) return nums[0];
    
    int prev2 = nums[0];
    int prev1 = std::max(nums[0], nums[1]);
    
    for (size_t i = 2; i < nums.size(); ++i) {
        int curr = std::max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    
    return prev1;
}
```

### 5.4 零钱兑换

> 用最少的硬币凑出目标金额。

```cpp
// 状态：dp[i] = 凑出金额 i 需要的最少硬币数
// 转移：dp[i] = min(dp[i], dp[i - coin] + 1) for each coin

int coin_change(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, amount + 1);  // 初始化为不可能的大值
    dp[0] = 0;
    
    for (int i = 1; i <= amount; ++i) {
        for (int coin : coins) {
            if (coin <= i && dp[i - coin] != amount + 1) {
                dp[i] = std::min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    
    return dp[amount] > amount ? -1 : dp[amount];
}
```

### 5.5 最长递增子序列（LIS）

```cpp
// O(n²) 解法
// 状态：dp[i] = 以 nums[i] 结尾的 LIS 长度
// 转移：dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

int length_of_lis(const std::vector<int>& nums) {
    if (nums.empty()) return 0;
    
    std::vector<int> dp(nums.size(), 1);
    int max_len = 1;
    
    for (size_t i = 1; i < nums.size(); ++i) {
        for (size_t j = 0; j < i; ++j) {
            if (nums[j] < nums[i]) {
                dp[i] = std::max(dp[i], dp[j] + 1);
            }
        }
        max_len = std::max(max_len, dp[i]);
    }
    
    return max_len;
}

// O(n log n) 优化：使用二分查找
int length_of_lis_optimized(const std::vector<int>& nums) {
    std::vector<int> tails;  // tails[i] = 长度为 i+1 的 LIS 的最小末尾
    
    for (int num : nums) {
        auto it = std::lower_bound(tails.begin(), tails.end(), num);
        if (it == tails.end()) {
            tails.push_back(num);
        } else {
            *it = num;
        }
    }
    
    return tails.size();
}
```

---

## 6. 二维 DP 经典问题

### 6.1 不同路径

> 从左上角到右下角，只能向右或向下，有多少种走法？

```cpp
// 状态：dp[i][j] = 到达 (i, j) 的路径数
// 转移：dp[i][j] = dp[i-1][j] + dp[i][j-1]

int unique_paths(int m, int n) {
    std::vector<std::vector<int>> dp(m, std::vector<int>(n, 1));
    
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    
    return dp[m - 1][n - 1];
}

// 空间优化为 O(n)
int unique_paths_optimized(int m, int n) {
    std::vector<int> dp(n, 1);
    
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }
    
    return dp[n - 1];
}
```

### 6.2 最小路径和

```cpp
// 状态：dp[i][j] = 到达 (i, j) 的最小路径和
// 转移：dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

int min_path_sum(std::vector<std::vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size();
    
    // 初始化第一行
    for (int j = 1; j < n; ++j) {
        grid[0][j] += grid[0][j - 1];
    }
    
    // 初始化第一列
    for (int i = 1; i < m; ++i) {
        grid[i][0] += grid[i - 1][0];
    }
    
    // DP
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            grid[i][j] += std::min(grid[i - 1][j], grid[i][j - 1]);
        }
    }
    
    return grid[m - 1][n - 1];
}
```

### 6.3 编辑距离

> 将 word1 转换为 word2 的最少操作次数（插入、删除、替换）。

```cpp
// 状态：dp[i][j] = word1[0..i-1] 转换为 word2[0..j-1] 的最小操作数
// 转移：
//   - 如果 word1[i-1] == word2[j-1]：dp[i][j] = dp[i-1][j-1]
//   - 否则：dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

int edit_distance(const std::string& word1, const std::string& word2) {
    int m = word1.size(), n = word2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));
    
    // 初始化
    for (int i = 0; i <= m; ++i) dp[i][0] = i;
    for (int j = 0; j <= n; ++j) dp[0][j] = j;
    
    // DP
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + std::min({
                    dp[i - 1][j],     // 删除
                    dp[i][j - 1],     // 插入
                    dp[i - 1][j - 1]  // 替换
                });
            }
        }
    }
    
    return dp[m][n];
}
```

### 6.4 最长公共子序列（LCS）

```cpp
// 状态：dp[i][j] = text1[0..i-1] 和 text2[0..j-1] 的 LCS 长度
// 转移：
//   - 如果 text1[i-1] == text2[j-1]：dp[i][j] = dp[i-1][j-1] + 1
//   - 否则：dp[i][j] = max(dp[i-1][j], dp[i][j-1])

int longest_common_subsequence(const std::string& text1, const std::string& text2) {
    int m = text1.size(), n = text2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (text1[i - 1] == text2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }
    
    return dp[m][n];
}
```

---

## 7. 背包问题

### 7.1 0-1 背包

> 有 n 个物品，每个物品有重量和价值，容量为 W 的背包最多能装多少价值？

```cpp
// 状态：dp[i][w] = 前 i 个物品，容量为 w 时的最大价值
// 转移：dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])

int knapsack_01(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    int n = weights.size();
    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(W + 1, 0));
    
    for (int i = 1; i <= n; ++i) {
        for (int w = 0; w <= W; ++w) {
            dp[i][w] = dp[i - 1][w];  // 不选第 i 个物品
            if (w >= weights[i - 1]) {
                dp[i][w] = std::max(dp[i][w], 
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]);
            }
        }
    }
    
    return dp[n][W];
}

// 空间优化：从后往前遍历
int knapsack_01_optimized(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    std::vector<int> dp(W + 1, 0);
    
    for (size_t i = 0; i < weights.size(); ++i) {
        for (int w = W; w >= weights[i]; --w) {  // 必须从后往前！
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    
    return dp[W];
}
```

### 7.2 完全背包

> 每个物品可以选无限次。

```cpp
// 与 0-1 背包的区别：从前往后遍历
int knapsack_complete(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    std::vector<int> dp(W + 1, 0);
    
    for (size_t i = 0; i < weights.size(); ++i) {
        for (int w = weights[i]; w <= W; ++w) {  // 从前往后
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    
    return dp[W];
}
```

---

## 📝 练习题

### 练习1：解码方法
给定一个数字字符串，计算有多少种解码方式（A=1, B=2, ..., Z=26）。

### 练习2：单词拆分
判断字符串能否被拆分成词典中的单词。

### 练习3：三角形最小路径和
找从顶到底的最小路径和。

### 练习4：目标和
给数组中的数添加正负号，使和等于目标值。

---

## 💡 要点总结

1. **递归三要素**：基准情况、递归关系、规模缩小
2. **记忆化**：用缓存避免重复计算
3. **DP 两种实现**：自顶向下（记忆化递归）、自底向上（迭代）
4. **DP 关键**：定义状态、写出转移方程
5. **空间优化**：滚动数组减少空间消耗
6. **背包问题**：0-1 背包从后往前，完全背包从前往后

---

## ⏭️ 下一节

[3.5 常用数据结构](./05_data_structures.md) - 实现链表、栈、队列、树

