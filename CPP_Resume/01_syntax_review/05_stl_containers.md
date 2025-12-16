# 1.5 STL 容器

## 📖 本节概述

STL（Standard Template Library，标准模板库）是C++标准库的核心部分，提供了一系列通用的容器、算法和迭代器。本节将回顾最常用的STL容器，帮助你快速掌握它们的使用方法和适用场景。

---

## 1. STL 容器概览

### 1.1 容器分类

| 类别 | 容器 | 特点 |
|------|------|------|
| **序列容器** | `vector`, `deque`, `list`, `array`, `forward_list` | 按顺序存储元素 |
| **关联容器** | `set`, `map`, `multiset`, `multimap` | 按键排序，基于红黑树 |
| **无序容器** | `unordered_set`, `unordered_map`, `unordered_multiset`, `unordered_multimap` | 基于哈希表 |
| **容器适配器** | `stack`, `queue`, `priority_queue` | 基于其他容器的封装 |

### 1.2 如何选择容器

```
需要随机访问？
├─ 是 → 需要在中间插入删除？
│       ├─ 是 → deque
│       └─ 否 → vector（默认选择）
└─ 否 → 需要在中间插入删除？
        ├─ 是 → list
        └─ 否 → 需要按键查找？
                ├─ 是 → 需要有序？
                │       ├─ 是 → map/set
                │       └─ 否 → unordered_map/unordered_set
                └─ 否 → vector
```

---

## 2. vector - 动态数组

### 2.1 基本操作

```cpp
#include <vector>
#include <iostream>

int main() {
    // 创建 vector
    std::vector<int> v1;                    // 空 vector
    std::vector<int> v2(5);                 // 5个元素，默认值0
    std::vector<int> v3(5, 10);             // 5个元素，每个值为10
    std::vector<int> v4 = {1, 2, 3, 4, 5};  // 初始化列表
    std::vector<int> v5{1, 2, 3, 4, 5};     // C++11 统一初始化
    
    // 添加元素
    v1.push_back(1);       // 在末尾添加
    v1.push_back(2);
    v1.emplace_back(3);    // C++11：原地构造，更高效
    
    // 访问元素
    int first = v1[0];           // 不检查边界
    int second = v1.at(1);       // 检查边界，越界抛出异常
    int front = v1.front();      // 第一个元素
    int back = v1.back();        // 最后一个元素
    int* data = v1.data();       // 底层数组指针
    
    // 大小和容量
    size_t size = v1.size();       // 元素个数
    size_t capacity = v1.capacity(); // 已分配空间
    bool empty = v1.empty();       // 是否为空
    
    v1.resize(10);        // 改变大小
    v1.reserve(100);      // 预分配空间（不改变size）
    v1.shrink_to_fit();   // 释放多余空间
    
    // 删除元素
    v1.pop_back();        // 删除最后一个
    v1.erase(v1.begin()); // 删除第一个
    v1.erase(v1.begin(), v1.begin() + 2);  // 删除范围
    v1.clear();           // 清空所有元素
    
    return 0;
}
```

### 2.2 遍历 vector

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// 方法1：范围 for 循环（推荐）
for (int x : v) {
    std::cout << x << " ";
}

// 方法2：引用避免拷贝
for (const auto& x : v) {
    std::cout << x << " ";
}

// 方法3：迭代器
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";
}

// 方法4：索引
for (size_t i = 0; i < v.size(); ++i) {
    std::cout << v[i] << " ";
}

// 反向遍历
for (auto it = v.rbegin(); it != v.rend(); ++it) {
    std::cout << *it << " ";
}
```

### 2.3 vector 的注意事项

```cpp
// 1. 迭代器失效
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.push_back(4);  // 可能导致重新分配，it 失效！

// 2. 删除元素时的正确做法
std::vector<int> v = {1, 2, 3, 4, 5};
// 删除所有偶数
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) {
        it = v.erase(it);  // erase 返回下一个有效迭代器
    } else {
        ++it;
    }
}

// 更好的方式：erase-remove idiom
v.erase(std::remove_if(v.begin(), v.end(), 
        [](int x) { return x % 2 == 0; }), 
        v.end());

// C++20：std::erase_if
std::erase_if(v, [](int x) { return x % 2 == 0; });
```

---

## 3. array - 固定大小数组（C++11）

```cpp
#include <array>

int main() {
    // 创建 array
    std::array<int, 5> arr1;                     // 未初始化
    std::array<int, 5> arr2 = {1, 2, 3, 4, 5};   // 初始化
    std::array<int, 5> arr3{};                   // 零初始化
    
    // 访问元素
    arr2[0] = 10;
    arr2.at(1) = 20;  // 带边界检查
    
    // 大小
    constexpr size_t size = arr2.size();  // 编译期常量
    
    // 遍历
    for (const auto& x : arr2) {
        std::cout << x << " ";
    }
    
    // 与 C 数组互操作
    int* ptr = arr2.data();
    
    // 填充
    arr1.fill(0);
    
    // 交换
    arr1.swap(arr2);
    
    return 0;
}

// 优点：比原生数组安全，支持 STL 算法，知道自己的大小
// 缺点：大小固定，必须在编译期确定
```

---

## 4. deque - 双端队列

```cpp
#include <deque>

int main() {
    std::deque<int> dq = {2, 3, 4};
    
    // 两端操作（与 vector 不同的地方）
    dq.push_front(1);    // 在前端添加
    dq.push_back(5);     // 在后端添加
    dq.pop_front();      // 删除前端
    dq.pop_back();       // 删除后端
    
    // 支持随机访问
    dq[0] = 10;
    
    // 遍历方式与 vector 相同
    for (const auto& x : dq) {
        std::cout << x << " ";
    }
    
    return 0;
}

// 优点：两端 O(1) 插入删除
// 缺点：内存不连续，缓存不友好
```

---

## 5. list - 双向链表

```cpp
#include <list>

int main() {
    std::list<int> lst = {3, 1, 4, 1, 5};
    
    // 两端操作
    lst.push_front(0);
    lst.push_back(9);
    lst.pop_front();
    lst.pop_back();
    
    // 中间插入（高效，O(1)）
    auto it = lst.begin();
    std::advance(it, 2);      // 移动到第3个位置
    lst.insert(it, 100);      // 在该位置插入
    
    // list 特有操作
    lst.sort();               // 排序（不能用 std::sort）
    lst.reverse();            // 反转
    lst.unique();             // 删除相邻重复元素
    
    // 合并两个有序 list
    std::list<int> lst2 = {2, 4, 6};
    lst.merge(lst2);          // lst2 变为空
    
    // 移动元素到另一个位置
    lst.splice(lst.begin(), lst, --lst.end());  // 把最后一个移到开头
    
    // 删除满足条件的元素
    lst.remove(1);            // 删除所有值为1的元素
    lst.remove_if([](int x) { return x % 2 == 0; });  // 删除偶数
    
    return 0;
}

// 优点：任意位置 O(1) 插入删除
// 缺点：不支持随机访问，内存开销大
```

---

## 6. map - 有序键值对

### 6.1 基本操作

```cpp
#include <map>
#include <string>

int main() {
    // 创建 map
    std::map<std::string, int> scores;
    
    // 插入元素
    scores["Alice"] = 95;
    scores["Bob"] = 87;
    scores.insert({"Charlie", 92});
    scores.insert(std::make_pair("David", 88));
    scores.emplace("Eve", 91);  // C++11：原地构造
    
    // 访问元素
    int alice_score = scores["Alice"];     // 95
    int frank_score = scores["Frank"];     // ⚠️ 不存在则创建，值为0
    
    // 安全访问（推荐）
    if (scores.count("Alice") > 0) {
        std::cout << scores["Alice"] << std::endl;
    }
    
    // C++11：使用 at()
    try {
        int score = scores.at("Unknown");  // 抛出 std::out_of_range
    } catch (const std::out_of_range& e) {
        std::cout << "Not found!" << std::endl;
    }
    
    // 查找
    auto it = scores.find("Bob");
    if (it != scores.end()) {
        std::cout << it->first << ": " << it->second << std::endl;
    }
    
    // C++20：contains
    if (scores.contains("Alice")) {
        std::cout << "Alice exists!" << std::endl;
    }
    
    return 0;
}
```

### 6.2 遍历 map

```cpp
std::map<std::string, int> scores = {
    {"Alice", 95}, {"Bob", 87}, {"Charlie", 92}
};

// 方法1：范围 for（推荐）
for (const auto& [name, score] : scores) {  // C++17 结构化绑定
    std::cout << name << ": " << score << std::endl;
}

// C++11 方式
for (const auto& pair : scores) {
    std::cout << pair.first << ": " << pair.second << std::endl;
}

// 方法2：迭代器
for (auto it = scores.begin(); it != scores.end(); ++it) {
    std::cout << it->first << ": " << it->second << std::endl;
}
```

### 6.3 map 的其他操作

```cpp
std::map<int, std::string> m = {{1, "one"}, {2, "two"}, {3, "three"}};

// 删除
m.erase(2);                    // 按键删除
m.erase(m.begin());            // 按迭代器删除
m.erase(m.find(3), m.end());   // 删除范围

// 大小
size_t size = m.size();
bool empty = m.empty();

// 清空
m.clear();

// 边界查询
auto lower = m.lower_bound(2);  // 第一个 >= 2 的位置
auto upper = m.upper_bound(2);  // 第一个 > 2 的位置
auto range = m.equal_range(2);  // 返回 {lower, upper}
```

---

## 7. set - 有序集合

```cpp
#include <set>

int main() {
    // 创建 set
    std::set<int> s1;
    std::set<int> s2 = {3, 1, 4, 1, 5, 9};  // 自动去重排序
    
    // 插入
    s1.insert(10);
    s1.insert(20);
    auto [it, success] = s1.insert(10);  // C++17：返回迭代器和是否成功
    s1.emplace(30);
    
    // 查找
    auto it2 = s1.find(10);
    if (it2 != s1.end()) {
        std::cout << "Found: " << *it2 << std::endl;
    }
    
    // count（对于 set，只能是0或1）
    if (s1.count(10) > 0) {
        std::cout << "10 exists" << std::endl;
    }
    
    // C++20
    if (s1.contains(10)) {
        std::cout << "10 exists" << std::endl;
    }
    
    // 删除
    s1.erase(10);
    
    // 遍历（元素有序）
    for (int x : s2) {
        std::cout << x << " ";  // 1 3 4 5 9
    }
    
    return 0;
}
```

---

## 8. unordered_map 和 unordered_set

### 8.1 unordered_map

```cpp
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, int> umap;
    
    // 操作与 map 类似
    umap["Alice"] = 95;
    umap["Bob"] = 87;
    umap.insert({"Charlie", 92});
    
    // 查找 O(1) 平均
    if (umap.find("Alice") != umap.end()) {
        std::cout << umap["Alice"] << std::endl;
    }
    
    // 遍历（无序！）
    for (const auto& [name, score] : umap) {
        std::cout << name << ": " << score << std::endl;
    }
    
    // 哈希相关
    size_t buckets = umap.bucket_count();
    float load = umap.load_factor();
    umap.rehash(100);  // 重新哈希
    
    return 0;
}
```

### 8.2 自定义类型作为键

```cpp
#include <unordered_map>
#include <functional>

struct Point {
    int x, y;
    
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

// 自定义哈希函数
struct PointHash {
    size_t operator()(const Point& p) const {
        return std::hash<int>{}(p.x) ^ (std::hash<int>{}(p.y) << 1);
    }
};

int main() {
    std::unordered_map<Point, std::string, PointHash> points;
    points[{1, 2}] = "Point A";
    points[{3, 4}] = "Point B";
    
    return 0;
}
```

---

## 9. 容器适配器

### 9.1 stack - 栈

```cpp
#include <stack>

int main() {
    std::stack<int> s;
    
    s.push(1);
    s.push(2);
    s.push(3);
    
    while (!s.empty()) {
        std::cout << s.top() << " ";  // 3 2 1
        s.pop();
    }
    
    return 0;
}
```

### 9.2 queue - 队列

```cpp
#include <queue>

int main() {
    std::queue<int> q;
    
    q.push(1);
    q.push(2);
    q.push(3);
    
    while (!q.empty()) {
        std::cout << q.front() << " ";  // 1 2 3
        q.pop();
    }
    
    return 0;
}
```

### 9.3 priority_queue - 优先队列

```cpp
#include <queue>
#include <vector>

int main() {
    // 默认：最大堆
    std::priority_queue<int> pq;
    pq.push(3);
    pq.push(1);
    pq.push(4);
    
    while (!pq.empty()) {
        std::cout << pq.top() << " ";  // 4 3 1
        pq.pop();
    }
    
    // 最小堆
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_pq;
    min_pq.push(3);
    min_pq.push(1);
    min_pq.push(4);
    
    while (!min_pq.empty()) {
        std::cout << min_pq.top() << " ";  // 1 3 4
        min_pq.pop();
    }
    
    return 0;
}
```

---

## 10. 容器性能对比

| 操作 | vector | deque | list | map | unordered_map |
|------|--------|-------|------|-----|---------------|
| 随机访问 | O(1) | O(1) | O(n) | O(log n) | O(1) avg |
| 头部插入 | O(n) | O(1) | O(1) | - | - |
| 尾部插入 | O(1)* | O(1) | O(1) | - | - |
| 中间插入 | O(n) | O(n) | O(1) | - | - |
| 查找 | O(n) | O(n) | O(n) | O(log n) | O(1) avg |
| 删除 | O(n) | O(n) | O(1) | O(log n) | O(1) avg |

*amortized（均摊）

---

## 📝 练习题

### 练习1：词频统计
使用 `unordered_map` 统计一段文本中每个单词出现的次数。

### 练习2：成绩管理
使用 `map` 实现一个简单的学生成绩管理系统，支持添加、删除、查询、按成绩排序。

### 练习3：任务调度
使用 `priority_queue` 模拟一个简单的任务调度器，按优先级执行任务。

### 练习4：LRU 缓存
使用 `list` 和 `unordered_map` 实现一个 LRU（最近最少使用）缓存。

---

## 💡 要点总结

1. **默认使用 vector**：除非有特殊需求
2. **使用范围 for 循环**：更安全、更清晰
3. **使用 emplace 系列**：避免不必要的拷贝
4. **使用 C++17 结构化绑定**：简化 map 遍历
5. **使用 contains（C++20）**：比 count 更直观
6. **注意迭代器失效**：插入/删除后迭代器可能失效
7. **根据场景选择容器**：查找多用 map/unordered_map，顺序重要用 map

---

## ⏭️ 下一节

[1.6 现代C++新特性总览](./06_modern_features.md) - 快速了解C++11/14/17/20的关键特性

