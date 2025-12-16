# 3.6 实战练习题

## 📖 本节概述

学习算法的最佳方式是动手实践。本节提供一系列精心挑选的练习题，涵盖前面章节的所有知识点，从简单到困难分级，帮助你巩固所学。

---

## 1. 练习题分级说明

| 难度 | 说明 | 建议时间 |
|------|------|----------|
| ⭐ | 入门级，直接应用基础知识 | 10-15 分钟 |
| ⭐⭐ | 简单级，需要稍加思考 | 15-30 分钟 |
| ⭐⭐⭐ | 中等级，需要综合多个知识点 | 30-60 分钟 |
| ⭐⭐⭐⭐ | 困难级，需要巧妙的思路 | 60+ 分钟 |

---

## 2. 数组与字符串

### 题目 2.1：两数之和 ⭐

> 给定一个整数数组和目标值，找出数组中和为目标值的两个数的索引。

```cpp
// 示例：
// 输入：nums = [2, 7, 11, 15], target = 9
// 输出：[0, 1] (因为 nums[0] + nums[1] = 9)

std::vector<int> two_sum(const std::vector<int>& nums, int target) {
    // 你的代码
}
```

**提示**：使用哈希表优化到 O(n)

<details>
<summary>参考解答</summary>

```cpp
std::vector<int> two_sum(const std::vector<int>& nums, int target) {
    std::unordered_map<int, int> seen;  // value -> index
    
    for (int i = 0; i < nums.size(); ++i) {
        int complement = target - nums[i];
        if (seen.count(complement)) {
            return {seen[complement], i};
        }
        seen[nums[i]] = i;
    }
    return {};
}
```
</details>

---

### 题目 2.2：移除元素 ⭐

> 原地移除数组中所有等于给定值的元素，返回新长度。

```cpp
// 示例：
// 输入：nums = [3, 2, 2, 3], val = 3
// 输出：2，且 nums 的前两个元素为 [2, 2]

int remove_element(std::vector<int>& nums, int val) {
    // 你的代码
}
```

**提示**：双指针

<details>
<summary>参考解答</summary>

```cpp
int remove_element(std::vector<int>& nums, int val) {
    int slow = 0;
    for (int fast = 0; fast < nums.size(); ++fast) {
        if (nums[fast] != val) {
            nums[slow++] = nums[fast];
        }
    }
    return slow;
}
```
</details>

---

### 题目 2.3：最长无重复子串 ⭐⭐

> 找出字符串中不含重复字符的最长子串的长度。

```cpp
// 示例：
// 输入："abcabcbb"
// 输出：3 ("abc")

int length_of_longest_substring(const std::string& s) {
    // 你的代码
}
```

**提示**：滑动窗口 + 哈希表

<details>
<summary>参考解答</summary>

```cpp
int length_of_longest_substring(const std::string& s) {
    std::unordered_map<char, int> last_pos;
    int max_len = 0, start = 0;
    
    for (int i = 0; i < s.size(); ++i) {
        if (last_pos.count(s[i]) && last_pos[s[i]] >= start) {
            start = last_pos[s[i]] + 1;
        }
        last_pos[s[i]] = i;
        max_len = std::max(max_len, i - start + 1);
    }
    return max_len;
}
```
</details>

---

### 题目 2.4：盛最多水的容器 ⭐⭐

> 给定 n 个非负整数 a1, a2, ..., an，每个数代表一个垂直线段的高度。找出两条线，使得它们与 x 轴构成的容器可以容纳最多的水。

```cpp
// 示例：
// 输入：[1, 8, 6, 2, 5, 4, 8, 3, 7]
// 输出：49

int max_area(const std::vector<int>& height) {
    // 你的代码
}
```

**提示**：双指针从两端向中间移动

<details>
<summary>参考解答</summary>

```cpp
int max_area(const std::vector<int>& height) {
    int left = 0, right = height.size() - 1;
    int max_water = 0;
    
    while (left < right) {
        int h = std::min(height[left], height[right]);
        max_water = std::max(max_water, h * (right - left));
        
        if (height[left] < height[right]) {
            ++left;
        } else {
            --right;
        }
    }
    return max_water;
}
```
</details>

---

### 题目 2.5：三数之和 ⭐⭐⭐

> 找出数组中所有和为 0 的三元组，不能重复。

```cpp
// 示例：
// 输入：[-1, 0, 1, 2, -1, -4]
// 输出：[[-1, -1, 2], [-1, 0, 1]]

std::vector<std::vector<int>> three_sum(std::vector<int>& nums) {
    // 你的代码
}
```

**提示**：先排序，固定一个数，双指针找另外两个

<details>
<summary>参考解答</summary>

```cpp
std::vector<std::vector<int>> three_sum(std::vector<int>& nums) {
    std::vector<std::vector<int>> result;
    std::sort(nums.begin(), nums.end());
    int n = nums.size();
    
    for (int i = 0; i < n - 2; ++i) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;  // 跳过重复
        
        int left = i + 1, right = n - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.push_back({nums[i], nums[left], nums[right]});
                while (left < right && nums[left] == nums[left + 1]) ++left;
                while (left < right && nums[right] == nums[right - 1]) --right;
                ++left;
                --right;
            } else if (sum < 0) {
                ++left;
            } else {
                --right;
            }
        }
    }
    return result;
}
```
</details>

---

## 3. 链表

### 题目 3.1：反转链表 ⭐

```cpp
ListNode* reverse_list(ListNode* head) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
ListNode* reverse_list(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;
}
```
</details>

---

### 题目 3.2：合并两个有序链表 ⭐

```cpp
ListNode* merge_two_lists(ListNode* l1, ListNode* l2) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
ListNode* merge_two_lists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* curr = &dummy;
    
    while (l1 && l2) {
        if (l1->val <= l2->val) {
            curr->next = l1;
            l1 = l1->next;
        } else {
            curr->next = l2;
            l2 = l2->next;
        }
        curr = curr->next;
    }
    curr->next = l1 ? l1 : l2;
    return dummy.next;
}
```
</details>

---

### 题目 3.3：删除链表倒数第 N 个节点 ⭐⭐

```cpp
// 示例：
// 输入：1->2->3->4->5, n = 2
// 输出：1->2->3->5

ListNode* remove_nth_from_end(ListNode* head, int n) {
    // 你的代码
}
```

**提示**：快慢指针，快指针先走 n 步

<details>
<summary>参考解答</summary>

```cpp
ListNode* remove_nth_from_end(ListNode* head, int n) {
    ListNode dummy(0);
    dummy.next = head;
    ListNode* fast = &dummy;
    ListNode* slow = &dummy;
    
    for (int i = 0; i <= n; ++i) {
        fast = fast->next;
    }
    
    while (fast) {
        fast = fast->next;
        slow = slow->next;
    }
    
    ListNode* to_delete = slow->next;
    slow->next = slow->next->next;
    delete to_delete;
    
    return dummy.next;
}
```
</details>

---

### 题目 3.4：环形链表 II ⭐⭐⭐

> 找出环的入口节点。

```cpp
ListNode* detect_cycle(ListNode* head) {
    // 你的代码
}
```

**提示**：快慢指针相遇后，一个从头开始，一个从相遇点开始

<details>
<summary>参考解答</summary>

```cpp
ListNode* detect_cycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* ptr = head;
            while (ptr != slow) {
                ptr = ptr->next;
                slow = slow->next;
            }
            return ptr;
        }
    }
    return nullptr;
}
```
</details>

---

## 4. 栈与队列

### 题目 4.1：有效的括号 ⭐

```cpp
bool is_valid(const std::string& s) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
bool is_valid(const std::string& s) {
    std::stack<char> st;
    std::unordered_map<char, char> pairs = {{')', '('}, {']', '['}, {'}', '{'}};
    
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.empty() || st.top() != pairs[c]) return false;
            st.pop();
        }
    }
    return st.empty();
}
```
</details>

---

### 题目 4.2：最小栈 ⭐⭐

> 设计一个栈，支持 push、pop、top 以及 O(1) 获取最小元素。

```cpp
class MinStack {
public:
    void push(int val);
    void pop();
    int top();
    int getMin();
};
```

<details>
<summary>参考解答</summary>

```cpp
class MinStack {
private:
    std::stack<int> data;
    std::stack<int> mins;
    
public:
    void push(int val) {
        data.push(val);
        if (mins.empty() || val <= mins.top()) {
            mins.push(val);
        }
    }
    
    void pop() {
        if (data.top() == mins.top()) {
            mins.pop();
        }
        data.pop();
    }
    
    int top() {
        return data.top();
    }
    
    int getMin() {
        return mins.top();
    }
};
```
</details>

---

### 题目 4.3：滑动窗口最大值 ⭐⭐⭐

> 给定数组和滑动窗口大小 k，返回每个窗口的最大值。

```cpp
// 示例：
// 输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
// 输出：[3,3,5,5,6,7]

std::vector<int> max_sliding_window(const std::vector<int>& nums, int k) {
    // 你的代码
}
```

**提示**：单调递减队列

<details>
<summary>参考解答</summary>

```cpp
std::vector<int> max_sliding_window(const std::vector<int>& nums, int k) {
    std::vector<int> result;
    std::deque<int> dq;  // 存储索引
    
    for (int i = 0; i < nums.size(); ++i) {
        // 移除窗口外的元素
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }
        // 保持单调递减
        while (!dq.empty() && nums[dq.back()] < nums[i]) {
            dq.pop_back();
        }
        dq.push_back(i);
        
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    return result;
}
```
</details>

---

## 5. 二叉树

### 题目 5.1：二叉树的最大深度 ⭐

```cpp
int max_depth(TreeNode* root) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
int max_depth(TreeNode* root) {
    if (!root) return 0;
    return 1 + std::max(max_depth(root->left), max_depth(root->right));
}
```
</details>

---

### 题目 5.2：对称二叉树 ⭐⭐

> 检查二叉树是否镜像对称。

```cpp
bool is_symmetric(TreeNode* root) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
bool is_symmetric(TreeNode* root) {
    auto check = [](TreeNode* p, TreeNode* q, auto&& self) -> bool {
        if (!p && !q) return true;
        if (!p || !q) return false;
        return p->val == q->val 
            && self(p->left, q->right, self) 
            && self(p->right, q->left, self);
    };
    return check(root, root, check);
}
```
</details>

---

### 题目 5.3：从前序与中序遍历构造二叉树 ⭐⭐⭐

```cpp
TreeNode* build_tree(std::vector<int>& preorder, std::vector<int>& inorder) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
TreeNode* build_tree(std::vector<int>& preorder, std::vector<int>& inorder) {
    std::unordered_map<int, int> in_map;
    for (int i = 0; i < inorder.size(); ++i) {
        in_map[inorder[i]] = i;
    }
    
    std::function<TreeNode*(int, int, int, int)> build = 
        [&](int pre_l, int pre_r, int in_l, int in_r) -> TreeNode* {
        if (pre_l > pre_r) return nullptr;
        
        int root_val = preorder[pre_l];
        int root_idx = in_map[root_val];
        int left_size = root_idx - in_l;
        
        TreeNode* node = new TreeNode(root_val);
        node->left = build(pre_l + 1, pre_l + left_size, in_l, root_idx - 1);
        node->right = build(pre_l + left_size + 1, pre_r, root_idx + 1, in_r);
        return node;
    };
    
    return build(0, preorder.size() - 1, 0, inorder.size() - 1);
}
```
</details>

---

## 6. 动态规划

### 题目 6.1：爬楼梯 ⭐

```cpp
int climb_stairs(int n) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
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
</details>

---

### 题目 6.2：打家劫舍 ⭐⭐

```cpp
int rob(const std::vector<int>& nums) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
int rob(const std::vector<int>& nums) {
    if (nums.empty()) return 0;
    if (nums.size() == 1) return nums[0];
    
    int prev2 = nums[0];
    int prev1 = std::max(nums[0], nums[1]);
    
    for (int i = 2; i < nums.size(); ++i) {
        int curr = std::max(prev1, prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```
</details>

---

### 题目 6.3：最长递增子序列 ⭐⭐⭐

```cpp
int length_of_lis(const std::vector<int>& nums) {
    // 你的代码（尝试 O(n log n) 解法）
}
```

<details>
<summary>参考解答</summary>

```cpp
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
```
</details>

---

### 题目 6.4：编辑距离 ⭐⭐⭐⭐

```cpp
int min_distance(const std::string& word1, const std::string& word2) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
int min_distance(const std::string& word1, const std::string& word2) {
    int m = word1.size(), n = word2.size();
    std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));
    
    for (int i = 0; i <= m; ++i) dp[i][0] = i;
    for (int j = 0; j <= n; ++j) dp[0][j] = j;
    
    for (int i = 1; i <= m; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (word1[i-1] == word2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + std::min({dp[i-1][j], dp[i][j-1], dp[i-1][j-1]});
            }
        }
    }
    return dp[m][n];
}
```
</details>

---

## 7. 排序与查找

### 题目 7.1：在排序数组中查找元素的第一个和最后一个位置 ⭐⭐

```cpp
std::vector<int> search_range(const std::vector<int>& nums, int target) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
std::vector<int> search_range(const std::vector<int>& nums, int target) {
    auto lower = std::lower_bound(nums.begin(), nums.end(), target);
    auto upper = std::upper_bound(nums.begin(), nums.end(), target);
    
    if (lower == nums.end() || *lower != target) {
        return {-1, -1};
    }
    return {(int)(lower - nums.begin()), (int)(upper - nums.begin() - 1)};
}
```
</details>

---

### 题目 7.2：搜索旋转排序数组 ⭐⭐⭐

> 在旋转过的有序数组中查找目标值。

```cpp
// 示例：
// 输入：nums = [4,5,6,7,0,1,2], target = 0
// 输出：4

int search(const std::vector<int>& nums, int target) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
int search(const std::vector<int>& nums, int target) {
    int left = 0, right = nums.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        
        if (nums[left] <= nums[mid]) {  // 左半有序
            if (nums[left] <= target && target < nums[mid]) {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {  // 右半有序
            if (nums[mid] < target && target <= nums[right]) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }
    return -1;
}
```
</details>

---

## 8. 综合挑战

### 题目 8.1：LRU 缓存 ⭐⭐⭐

> 设计 LRU（最近最少使用）缓存，支持 get 和 put 操作，均为 O(1)。

```cpp
class LRUCache {
public:
    LRUCache(int capacity);
    int get(int key);
    void put(int key, int value);
};
```

<details>
<summary>参考解答</summary>

```cpp
class LRUCache {
private:
    int capacity;
    std::list<std::pair<int, int>> cache;  // {key, value}
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> map;
    
public:
    LRUCache(int capacity) : capacity(capacity) {}
    
    int get(int key) {
        if (!map.count(key)) return -1;
        
        // 移到前面
        cache.splice(cache.begin(), cache, map[key]);
        return map[key]->second;
    }
    
    void put(int key, int value) {
        if (map.count(key)) {
            map[key]->second = value;
            cache.splice(cache.begin(), cache, map[key]);
            return;
        }
        
        if (cache.size() == capacity) {
            int old_key = cache.back().first;
            cache.pop_back();
            map.erase(old_key);
        }
        
        cache.emplace_front(key, value);
        map[key] = cache.begin();
    }
};
```
</details>

---

### 题目 8.2：接雨水 ⭐⭐⭐⭐

> 给定柱子高度数组，计算能接多少雨水。

```cpp
// 示例：
// 输入：[0,1,0,2,1,0,1,3,2,1,2,1]
// 输出：6

int trap(const std::vector<int>& height) {
    // 你的代码
}
```

<details>
<summary>参考解答</summary>

```cpp
int trap(const std::vector<int>& height) {
    if (height.empty()) return 0;
    
    int left = 0, right = height.size() - 1;
    int left_max = 0, right_max = 0;
    int result = 0;
    
    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= left_max) {
                left_max = height[left];
            } else {
                result += left_max - height[left];
            }
            ++left;
        } else {
            if (height[right] >= right_max) {
                right_max = height[right];
            } else {
                result += right_max - height[right];
            }
            --right;
        }
    }
    return result;
}
```
</details>

---

## 📝 学习建议

### 解题步骤

1. **理解题目**：确保完全理解输入输出和边界条件
2. **想出暴力解法**：先确保能解决问题
3. **分析复杂度**：思考是否可以优化
4. **寻找模式**：是否见过类似的问题？
5. **编写代码**：注意边界条件和特殊情况
6. **测试验证**：用示例和边界情况测试

### 常见思路

| 问题类型 | 常用技巧 |
|----------|----------|
| 数组重复/配对 | 哈希表 |
| 有序数组查找 | 二分查找 |
| 子数组/子串 | 滑动窗口 |
| 序列问题 | 动态规划 |
| 树的遍历 | 递归/BFS/DFS |
| 链表操作 | 双指针/虚拟头节点 |

### 推荐练习平台

- [LeetCode](https://leetcode.com/)
- [LeetCode 中文](https://leetcode.cn/)
- [Codeforces](https://codeforces.com/)
- [洛谷](https://www.luogu.com.cn/)

---

## 💡 总结

算法能力需要持续练习才能提升。建议：

1. **每天至少一题**：保持手感
2. **总结模式**：遇到新类型的题目要总结
3. **复习旧题**：隔一段时间重做
4. **理解而非背诵**：理解思路比记住代码重要
5. **学会分析**：每道题都分析时间和空间复杂度

祝你在算法学习之旅中取得进步！🚀

---

## ⏮️ 返回

[返回第三章目录](./README.md) | [返回教程首页](../README.md)

