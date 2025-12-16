/**
 * @file dp_demo.cpp
 * @brief 动态规划示例
 * 
 * 编译：g++ -std=c++20 -O2 -Wall -o dp_demo dp_demo.cpp
 * 运行：./dp_demo
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <climits>

//==============================================================================
// 辅助函数
//==============================================================================

template<typename T>
void print_2d(const std::string& label, const std::vector<std::vector<T>>& matrix) {
    std::cout << label << ":" << std::endl;
    for (const auto& row : matrix) {
        std::cout << "  ";
        for (const auto& x : row) {
            std::cout << x << " ";
        }
        std::cout << std::endl;
    }
}

//==============================================================================
// 1. 斐波那契数列
//==============================================================================

// 自顶向下（记忆化）
long long fib_memo(int n, std::vector<long long>& memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    return memo[n];
}

// 自底向上
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

// 空间优化
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

//==============================================================================
// 2. 爬楼梯
//==============================================================================

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

//==============================================================================
// 3. 最大子数组和
//==============================================================================

int max_subarray(const std::vector<int>& nums) {
    int max_sum = nums[0];
    int curr_sum = nums[0];
    
    for (size_t i = 1; i < nums.size(); ++i) {
        curr_sum = std::max(nums[i], curr_sum + nums[i]);
        max_sum = std::max(max_sum, curr_sum);
    }
    
    return max_sum;
}

// 返回区间
std::tuple<int, int, int> max_subarray_range(const std::vector<int>& nums) {
    int max_sum = nums[0], curr_sum = nums[0];
    int start = 0, end = 0, temp_start = 0;
    
    for (size_t i = 1; i < nums.size(); ++i) {
        if (nums[i] > curr_sum + nums[i]) {
            curr_sum = nums[i];
            temp_start = i;
        } else {
            curr_sum = curr_sum + nums[i];
        }
        
        if (curr_sum > max_sum) {
            max_sum = curr_sum;
            start = temp_start;
            end = i;
        }
    }
    
    return {max_sum, start, end};
}

//==============================================================================
// 4. 打家劫舍
//==============================================================================

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

//==============================================================================
// 5. 零钱兑换
//==============================================================================

int coin_change(const std::vector<int>& coins, int amount) {
    std::vector<int> dp(amount + 1, amount + 1);
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

//==============================================================================
// 6. 最长递增子序列
//==============================================================================

// O(n²) 解法
int length_of_lis_n2(const std::vector<int>& nums) {
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

// O(n log n) 解法
int length_of_lis(const std::vector<int>& nums) {
    std::vector<int> tails;
    
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

//==============================================================================
// 7. 不同路径
//==============================================================================

int unique_paths(int m, int n) {
    std::vector<int> dp(n, 1);
    
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }
    
    return dp[n - 1];
}

//==============================================================================
// 8. 最小路径和
//==============================================================================

int min_path_sum(std::vector<std::vector<int>> grid) {
    int m = grid.size(), n = grid[0].size();
    
    for (int j = 1; j < n; ++j) {
        grid[0][j] += grid[0][j - 1];
    }
    for (int i = 1; i < m; ++i) {
        grid[i][0] += grid[i - 1][0];
    }
    
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            grid[i][j] += std::min(grid[i - 1][j], grid[i][j - 1]);
        }
    }
    
    return grid[m - 1][n - 1];
}

//==============================================================================
// 9. 编辑距离
//==============================================================================

int edit_distance(const std::string& word1, const std::string& word2) {
    int m = word1.size(), n = word2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));
    
    for (int i = 0; i <= m; ++i) dp[i][0] = i;
    for (int j = 0; j <= n; ++j) dp[0][j] = j;
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (word1[i - 1] == word2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + std::min({
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                });
            }
        }
    }
    
    return dp[m][n];
}

//==============================================================================
// 10. 最长公共子序列
//==============================================================================

int lcs(const std::string& text1, const std::string& text2) {
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

//==============================================================================
// 11. 0-1 背包
//==============================================================================

int knapsack_01(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    std::vector<int> dp(W + 1, 0);
    
    for (size_t i = 0; i < weights.size(); ++i) {
        for (int w = W; w >= weights[i]; --w) {
            dp[w] = std::max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    
    return dp[W];
}

//==============================================================================
// 主函数
//==============================================================================

int main() {
    std::cout << "===== 动态规划示例 =====" << std::endl;
    
    // ========== 1. 斐波那契 ==========
    std::cout << "\n【1. 斐波那契数列】" << std::endl;
    std::cout << "fib(10) = " << fib_dp(10) << std::endl;
    std::cout << "fib(20) = " << fib_dp(20) << std::endl;
    std::cout << "fib(50) = " << fib_optimized(50) << std::endl;
    
    // ========== 2. 爬楼梯 ==========
    std::cout << "\n【2. 爬楼梯】" << std::endl;
    for (int n : {3, 5, 10}) {
        std::cout << "climb_stairs(" << n << ") = " << climb_stairs(n) << std::endl;
    }
    
    // ========== 3. 最大子数组和 ==========
    std::cout << "\n【3. 最大子数组和】" << std::endl;
    std::vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    std::cout << "数组: [-2, 1, -3, 4, -1, 2, 1, -5, 4]" << std::endl;
    auto [max_sum, start, end] = max_subarray_range(arr);
    std::cout << "最大和: " << max_sum << " (区间 [" << start << ", " << end << "])" << std::endl;
    
    // ========== 4. 打家劫舍 ==========
    std::cout << "\n【4. 打家劫舍】" << std::endl;
    std::vector<int> houses = {2, 7, 9, 3, 1};
    std::cout << "房屋价值: [2, 7, 9, 3, 1]" << std::endl;
    std::cout << "最大收益: " << rob(houses) << std::endl;
    
    // ========== 5. 零钱兑换 ==========
    std::cout << "\n【5. 零钱兑换】" << std::endl;
    std::vector<int> coins = {1, 2, 5};
    int amount = 11;
    std::cout << "硬币: [1, 2, 5], 金额: " << amount << std::endl;
    std::cout << "最少硬币数: " << coin_change(coins, amount) << std::endl;
    
    // ========== 6. 最长递增子序列 ==========
    std::cout << "\n【6. 最长递增子序列】" << std::endl;
    std::vector<int> lis_arr = {10, 9, 2, 5, 3, 7, 101, 18};
    std::cout << "数组: [10, 9, 2, 5, 3, 7, 101, 18]" << std::endl;
    std::cout << "LIS 长度: " << length_of_lis(lis_arr) << std::endl;
    
    // ========== 7. 不同路径 ==========
    std::cout << "\n【7. 不同路径】" << std::endl;
    std::cout << "3x7 网格的路径数: " << unique_paths(3, 7) << std::endl;
    std::cout << "7x3 网格的路径数: " << unique_paths(7, 3) << std::endl;
    
    // ========== 8. 最小路径和 ==========
    std::cout << "\n【8. 最小路径和】" << std::endl;
    std::vector<std::vector<int>> grid = {
        {1, 3, 1},
        {1, 5, 1},
        {4, 2, 1}
    };
    print_2d("网格", grid);
    std::cout << "最小路径和: " << min_path_sum(grid) << std::endl;
    
    // ========== 9. 编辑距离 ==========
    std::cout << "\n【9. 编辑距离】" << std::endl;
    std::string w1 = "horse", w2 = "ros";
    std::cout << "\"" << w1 << "\" -> \"" << w2 << "\": " << edit_distance(w1, w2) << std::endl;
    w1 = "intention"; w2 = "execution";
    std::cout << "\"" << w1 << "\" -> \"" << w2 << "\": " << edit_distance(w1, w2) << std::endl;
    
    // ========== 10. 最长公共子序列 ==========
    std::cout << "\n【10. 最长公共子序列】" << std::endl;
    std::string t1 = "abcde", t2 = "ace";
    std::cout << "\"" << t1 << "\" 和 \"" << t2 << "\" 的 LCS 长度: " << lcs(t1, t2) << std::endl;
    t1 = "AGGTAB"; t2 = "GXTXAYB";
    std::cout << "\"" << t1 << "\" 和 \"" << t2 << "\" 的 LCS 长度: " << lcs(t1, t2) << std::endl;
    
    // ========== 11. 0-1 背包 ==========
    std::cout << "\n【11. 0-1 背包】" << std::endl;
    std::vector<int> weights = {2, 3, 4, 5};
    std::vector<int> values = {3, 4, 5, 6};
    int W = 8;
    std::cout << "物品重量: [2, 3, 4, 5]" << std::endl;
    std::cout << "物品价值: [3, 4, 5, 6]" << std::endl;
    std::cout << "背包容量: " << W << std::endl;
    std::cout << "最大价值: " << knapsack_01(weights, values, W) << std::endl;
    
    std::cout << "\n===== 完成 =====" << std::endl;
    return 0;
}

