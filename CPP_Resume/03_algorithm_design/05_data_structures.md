# 3.5 常用数据结构

## 📖 本节概述

数据结构是组织和存储数据的方式，选择合适的数据结构对算法效率至关重要。本节将介绍链表、栈、队列、树等基础数据结构的原理和实现。

---

## 1. 数据结构概览

| 数据结构 | 特点 | 典型操作复杂度 |
|----------|------|----------------|
| 数组 | 连续内存，随机访问 | 访问 O(1)，插入 O(n) |
| 链表 | 非连续，灵活插删 | 访问 O(n)，插入 O(1) |
| 栈 | LIFO，后进先出 | push/pop O(1) |
| 队列 | FIFO，先进先出 | enqueue/dequeue O(1) |
| 哈希表 | 快速查找 | 增删查 O(1) 平均 |
| 二叉搜索树 | 有序，高效查找 | 增删查 O(log n) |
| 堆 | 快速获取最值 | 取最值 O(1)，插入 O(log n) |

---

## 2. 链表

### 2.1 单链表

```cpp
// 节点定义
template <typename T>
struct ListNode {
    T data;
    ListNode* next;
    
    ListNode(T val) : data(val), next(nullptr) {}
};

// 单链表类
template <typename T>
class SinglyLinkedList {
private:
    ListNode<T>* head;
    int size;
    
public:
    SinglyLinkedList() : head(nullptr), size(0) {}
    
    ~SinglyLinkedList() {
        while (head) {
            ListNode<T>* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    // 在头部插入
    void push_front(T val) {
        ListNode<T>* node = new ListNode<T>(val);
        node->next = head;
        head = node;
        ++size;
    }
    
    // 在尾部插入
    void push_back(T val) {
        ListNode<T>* node = new ListNode<T>(val);
        if (!head) {
            head = node;
        } else {
            ListNode<T>* curr = head;
            while (curr->next) {
                curr = curr->next;
            }
            curr->next = node;
        }
        ++size;
    }
    
    // 在指定位置插入
    void insert(int index, T val) {
        if (index <= 0) {
            push_front(val);
            return;
        }
        if (index >= size) {
            push_back(val);
            return;
        }
        
        ListNode<T>* node = new ListNode<T>(val);
        ListNode<T>* curr = head;
        for (int i = 0; i < index - 1; ++i) {
            curr = curr->next;
        }
        node->next = curr->next;
        curr->next = node;
        ++size;
    }
    
    // 删除头部
    void pop_front() {
        if (!head) return;
        ListNode<T>* temp = head;
        head = head->next;
        delete temp;
        --size;
    }
    
    // 删除指定值
    void remove(T val) {
        if (!head) return;
        
        if (head->data == val) {
            pop_front();
            return;
        }
        
        ListNode<T>* curr = head;
        while (curr->next && curr->next->data != val) {
            curr = curr->next;
        }
        
        if (curr->next) {
            ListNode<T>* temp = curr->next;
            curr->next = temp->next;
            delete temp;
            --size;
        }
    }
    
    // 查找
    ListNode<T>* find(T val) const {
        ListNode<T>* curr = head;
        while (curr) {
            if (curr->data == val) return curr;
            curr = curr->next;
        }
        return nullptr;
    }
    
    // 获取大小
    int get_size() const { return size; }
    
    // 打印链表
    void print() const {
        ListNode<T>* curr = head;
        while (curr) {
            std::cout << curr->data;
            if (curr->next) std::cout << " -> ";
            curr = curr->next;
        }
        std::cout << std::endl;
    }
};
```

### 2.2 双向链表

```cpp
template <typename T>
struct DoublyNode {
    T data;
    DoublyNode* prev;
    DoublyNode* next;
    
    DoublyNode(T val) : data(val), prev(nullptr), next(nullptr) {}
};

template <typename T>
class DoublyLinkedList {
private:
    DoublyNode<T>* head;
    DoublyNode<T>* tail;
    int size;
    
public:
    DoublyLinkedList() : head(nullptr), tail(nullptr), size(0) {}
    
    ~DoublyLinkedList() {
        while (head) {
            DoublyNode<T>* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    void push_front(T val) {
        DoublyNode<T>* node = new DoublyNode<T>(val);
        if (!head) {
            head = tail = node;
        } else {
            node->next = head;
            head->prev = node;
            head = node;
        }
        ++size;
    }
    
    void push_back(T val) {
        DoublyNode<T>* node = new DoublyNode<T>(val);
        if (!tail) {
            head = tail = node;
        } else {
            node->prev = tail;
            tail->next = node;
            tail = node;
        }
        ++size;
    }
    
    void pop_front() {
        if (!head) return;
        DoublyNode<T>* temp = head;
        head = head->next;
        if (head) head->prev = nullptr;
        else tail = nullptr;
        delete temp;
        --size;
    }
    
    void pop_back() {
        if (!tail) return;
        DoublyNode<T>* temp = tail;
        tail = tail->prev;
        if (tail) tail->next = nullptr;
        else head = nullptr;
        delete temp;
        --size;
    }
    
    int get_size() const { return size; }
};
```

### 2.3 链表常见操作

```cpp
// 反转链表
ListNode<int>* reverse(ListNode<int>* head) {
    ListNode<int>* prev = nullptr;
    ListNode<int>* curr = head;
    
    while (curr) {
        ListNode<int>* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    
    return prev;
}

// 检测环
bool has_cycle(ListNode<int>* head) {
    ListNode<int>* slow = head;
    ListNode<int>* fast = head;
    
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

// 找中间节点
ListNode<int>* find_middle(ListNode<int>* head) {
    ListNode<int>* slow = head;
    ListNode<int>* fast = head;
    
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

// 合并两个有序链表
ListNode<int>* merge_sorted(ListNode<int>* l1, ListNode<int>* l2) {
    ListNode<int> dummy(0);
    ListNode<int>* curr = &dummy;
    
    while (l1 && l2) {
        if (l1->data <= l2->data) {
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

---

## 3. 栈

### 3.1 栈的实现

```cpp
template <typename T>
class Stack {
private:
    std::vector<T> data;
    
public:
    void push(T val) {
        data.push_back(val);
    }
    
    void pop() {
        if (!empty()) {
            data.pop_back();
        }
    }
    
    T& top() {
        return data.back();
    }
    
    const T& top() const {
        return data.back();
    }
    
    bool empty() const {
        return data.empty();
    }
    
    size_t size() const {
        return data.size();
    }
};

// 使用 STL：std::stack<int> s;
```

### 3.2 栈的应用

```cpp
// 1. 括号匹配
bool is_valid_parentheses(const std::string& s) {
    std::stack<char> st;
    std::unordered_map<char, char> pairs = {
        {')', '('}, {']', '['}, {'}', '{'}
    };
    
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.empty() || st.top() != pairs[c]) {
                return false;
            }
            st.pop();
        }
    }
    return st.empty();
}

// 2. 逆波兰表达式求值
int eval_rpn(const std::vector<std::string>& tokens) {
    std::stack<int> st;
    
    for (const auto& token : tokens) {
        if (token == "+" || token == "-" || token == "*" || token == "/") {
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();
            if (token == "+") st.push(a + b);
            else if (token == "-") st.push(a - b);
            else if (token == "*") st.push(a * b);
            else st.push(a / b);
        } else {
            st.push(std::stoi(token));
        }
    }
    return st.top();
}

// 3. 单调栈：下一个更大元素
std::vector<int> next_greater(const std::vector<int>& nums) {
    int n = nums.size();
    std::vector<int> result(n, -1);
    std::stack<int> st;  // 存储索引
    
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && nums[st.top()] < nums[i]) {
            result[st.top()] = nums[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}
```

---

## 4. 队列

### 4.1 普通队列

```cpp
template <typename T>
class Queue {
private:
    std::deque<T> data;
    
public:
    void enqueue(T val) {
        data.push_back(val);
    }
    
    void dequeue() {
        if (!empty()) {
            data.pop_front();
        }
    }
    
    T& front() {
        return data.front();
    }
    
    bool empty() const {
        return data.empty();
    }
    
    size_t size() const {
        return data.size();
    }
};

// 使用 STL：std::queue<int> q;
```

### 4.2 循环队列

```cpp
template <typename T>
class CircularQueue {
private:
    std::vector<T> data;
    int front_idx;
    int rear_idx;
    int capacity;
    int count;
    
public:
    CircularQueue(int k) : data(k), front_idx(0), rear_idx(0), capacity(k), count(0) {}
    
    bool enqueue(T val) {
        if (is_full()) return false;
        data[rear_idx] = val;
        rear_idx = (rear_idx + 1) % capacity;
        ++count;
        return true;
    }
    
    bool dequeue() {
        if (is_empty()) return false;
        front_idx = (front_idx + 1) % capacity;
        --count;
        return true;
    }
    
    T front() const {
        return data[front_idx];
    }
    
    T rear() const {
        return data[(rear_idx - 1 + capacity) % capacity];
    }
    
    bool is_empty() const { return count == 0; }
    bool is_full() const { return count == capacity; }
};
```

### 4.3 双端队列

```cpp
// 使用 STL：std::deque<int>
#include <deque>

void demo_deque() {
    std::deque<int> dq;
    
    dq.push_back(1);    // 后端插入
    dq.push_front(0);   // 前端插入
    dq.pop_back();      // 后端删除
    dq.pop_front();     // 前端删除
    
    dq.front();         // 访问前端
    dq.back();          // 访问后端
}
```

### 4.4 优先队列（堆）

```cpp
#include <queue>

void demo_priority_queue() {
    // 默认最大堆
    std::priority_queue<int> max_heap;
    max_heap.push(3);
    max_heap.push(1);
    max_heap.push(4);
    std::cout << max_heap.top() << std::endl;  // 4
    
    // 最小堆
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
    min_heap.push(3);
    min_heap.push(1);
    min_heap.push(4);
    std::cout << min_heap.top() << std::endl;  // 1
    
    // 自定义比较
    auto cmp = [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return a.second > b.second;  // 按 second 最小
    };
    std::priority_queue<std::pair<int, int>, 
                        std::vector<std::pair<int, int>>, 
                        decltype(cmp)> pq(cmp);
}
```

---

## 5. 二叉树

### 5.1 二叉树结构

```cpp
template <typename T>
struct TreeNode {
    T data;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode(T val) : data(val), left(nullptr), right(nullptr) {}
};
```

### 5.2 遍历方式

```cpp
// 前序遍历：根 -> 左 -> 右
void preorder(TreeNode<int>* root) {
    if (!root) return;
    std::cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}

// 中序遍历：左 -> 根 -> 右
void inorder(TreeNode<int>* root) {
    if (!root) return;
    inorder(root->left);
    std::cout << root->data << " ";
    inorder(root->right);
}

// 后序遍历：左 -> 右 -> 根
void postorder(TreeNode<int>* root) {
    if (!root) return;
    postorder(root->left);
    postorder(root->right);
    std::cout << root->data << " ";
}

// 层序遍历（BFS）
void level_order(TreeNode<int>* root) {
    if (!root) return;
    
    std::queue<TreeNode<int>*> q;
    q.push(root);
    
    while (!q.empty()) {
        TreeNode<int>* node = q.front();
        q.pop();
        std::cout << node->data << " ";
        
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
    }
}
```

### 5.3 迭代遍历

```cpp
// 前序遍历（迭代）
std::vector<int> preorder_iterative(TreeNode<int>* root) {
    std::vector<int> result;
    if (!root) return result;
    
    std::stack<TreeNode<int>*> st;
    st.push(root);
    
    while (!st.empty()) {
        TreeNode<int>* node = st.top();
        st.pop();
        result.push_back(node->data);
        
        if (node->right) st.push(node->right);
        if (node->left) st.push(node->left);
    }
    return result;
}

// 中序遍历（迭代）
std::vector<int> inorder_iterative(TreeNode<int>* root) {
    std::vector<int> result;
    std::stack<TreeNode<int>*> st;
    TreeNode<int>* curr = root;
    
    while (curr || !st.empty()) {
        while (curr) {
            st.push(curr);
            curr = curr->left;
        }
        curr = st.top();
        st.pop();
        result.push_back(curr->data);
        curr = curr->right;
    }
    return result;
}
```

### 5.4 常见操作

```cpp
// 计算树的高度
int height(TreeNode<int>* root) {
    if (!root) return 0;
    return 1 + std::max(height(root->left), height(root->right));
}

// 计算节点数
int count_nodes(TreeNode<int>* root) {
    if (!root) return 0;
    return 1 + count_nodes(root->left) + count_nodes(root->right);
}

// 判断是否平衡
bool is_balanced(TreeNode<int>* root) {
    if (!root) return true;
    
    int left_h = height(root->left);
    int right_h = height(root->right);
    
    return std::abs(left_h - right_h) <= 1 
           && is_balanced(root->left) 
           && is_balanced(root->right);
}

// 查找最低公共祖先
TreeNode<int>* lowest_common_ancestor(TreeNode<int>* root, 
                                       TreeNode<int>* p, TreeNode<int>* q) {
    if (!root || root == p || root == q) return root;
    
    TreeNode<int>* left = lowest_common_ancestor(root->left, p, q);
    TreeNode<int>* right = lowest_common_ancestor(root->right, p, q);
    
    if (left && right) return root;
    return left ? left : right;
}
```

---

## 6. 二叉搜索树（BST）

### 6.1 BST 性质

- 左子树所有节点 < 根节点
- 右子树所有节点 > 根节点
- 中序遍历得到有序序列

### 6.2 BST 实现

```cpp
template <typename T>
class BST {
private:
    TreeNode<T>* root;
    
    TreeNode<T>* insert_helper(TreeNode<T>* node, T val) {
        if (!node) return new TreeNode<T>(val);
        
        if (val < node->data) {
            node->left = insert_helper(node->left, val);
        } else if (val > node->data) {
            node->right = insert_helper(node->right, val);
        }
        return node;
    }
    
    TreeNode<T>* find_min(TreeNode<T>* node) {
        while (node->left) node = node->left;
        return node;
    }
    
    TreeNode<T>* remove_helper(TreeNode<T>* node, T val) {
        if (!node) return nullptr;
        
        if (val < node->data) {
            node->left = remove_helper(node->left, val);
        } else if (val > node->data) {
            node->right = remove_helper(node->right, val);
        } else {
            // 找到要删除的节点
            if (!node->left) {
                TreeNode<T>* temp = node->right;
                delete node;
                return temp;
            }
            if (!node->right) {
                TreeNode<T>* temp = node->left;
                delete node;
                return temp;
            }
            // 有两个子节点：找右子树的最小值替换
            TreeNode<T>* min_node = find_min(node->right);
            node->data = min_node->data;
            node->right = remove_helper(node->right, min_node->data);
        }
        return node;
    }
    
public:
    BST() : root(nullptr) {}
    
    void insert(T val) {
        root = insert_helper(root, val);
    }
    
    bool search(T val) const {
        TreeNode<T>* curr = root;
        while (curr) {
            if (val == curr->data) return true;
            if (val < curr->data) curr = curr->left;
            else curr = curr->right;
        }
        return false;
    }
    
    void remove(T val) {
        root = remove_helper(root, val);
    }
    
    // 中序遍历输出有序序列
    void inorder() const {
        std::function<void(TreeNode<T>*)> traverse = [&](TreeNode<T>* node) {
            if (!node) return;
            traverse(node->left);
            std::cout << node->data << " ";
            traverse(node->right);
        };
        traverse(root);
        std::cout << std::endl;
    }
};
```

---

## 7. 哈希表

### 7.1 哈希表原理

- **哈希函数**：将键映射到数组索引
- **冲突处理**：链地址法、开放寻址法

### 7.2 简单实现（链地址法）

```cpp
template <typename K, typename V>
class HashTable {
private:
    static const int BUCKET_SIZE = 1000;
    std::vector<std::list<std::pair<K, V>>> buckets;
    
    int hash(const K& key) const {
        return std::hash<K>{}(key) % BUCKET_SIZE;
    }
    
public:
    HashTable() : buckets(BUCKET_SIZE) {}
    
    void put(const K& key, const V& value) {
        int idx = hash(key);
        for (auto& pair : buckets[idx]) {
            if (pair.first == key) {
                pair.second = value;
                return;
            }
        }
        buckets[idx].emplace_back(key, value);
    }
    
    V* get(const K& key) {
        int idx = hash(key);
        for (auto& pair : buckets[idx]) {
            if (pair.first == key) {
                return &pair.second;
            }
        }
        return nullptr;
    }
    
    void remove(const K& key) {
        int idx = hash(key);
        buckets[idx].remove_if([&key](const auto& pair) {
            return pair.first == key;
        });
    }
    
    bool contains(const K& key) const {
        int idx = hash(key);
        for (const auto& pair : buckets[idx]) {
            if (pair.first == key) return true;
        }
        return false;
    }
};
```

### 7.3 使用 STL

```cpp
#include <unordered_map>
#include <unordered_set>

void demo_hash() {
    // unordered_map
    std::unordered_map<std::string, int> ages;
    ages["Alice"] = 25;
    ages["Bob"] = 30;
    ages.insert({"Charlie", 35});
    
    if (ages.count("Alice")) {
        std::cout << "Alice: " << ages["Alice"] << std::endl;
    }
    
    for (const auto& [name, age] : ages) {
        std::cout << name << ": " << age << std::endl;
    }
    
    // unordered_set
    std::unordered_set<int> seen;
    seen.insert(1);
    seen.insert(2);
    if (seen.count(1)) {
        std::cout << "1 exists" << std::endl;
    }
}
```

---

## 8. 堆的实现

```cpp
template <typename T, typename Compare = std::less<T>>
class Heap {
private:
    std::vector<T> data;
    Compare comp;
    
    void sift_up(int idx) {
        while (idx > 0) {
            int parent = (idx - 1) / 2;
            if (comp(data[parent], data[idx])) {
                std::swap(data[parent], data[idx]);
                idx = parent;
            } else {
                break;
            }
        }
    }
    
    void sift_down(int idx) {
        int n = data.size();
        while (true) {
            int largest = idx;
            int left = 2 * idx + 1;
            int right = 2 * idx + 2;
            
            if (left < n && comp(data[largest], data[left])) {
                largest = left;
            }
            if (right < n && comp(data[largest], data[right])) {
                largest = right;
            }
            
            if (largest != idx) {
                std::swap(data[idx], data[largest]);
                idx = largest;
            } else {
                break;
            }
        }
    }
    
public:
    void push(T val) {
        data.push_back(val);
        sift_up(data.size() - 1);
    }
    
    void pop() {
        if (data.empty()) return;
        data[0] = data.back();
        data.pop_back();
        if (!data.empty()) {
            sift_down(0);
        }
    }
    
    const T& top() const {
        return data[0];
    }
    
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};
```

---

## 📝 练习题

### 练习1：LRU 缓存
实现一个 LRU（最近最少使用）缓存。

### 练习2：用栈实现队列
用两个栈实现队列的功能。

### 练习3：序列化二叉树
实现二叉树的序列化和反序列化。

### 练习4：设计哈希集合
不使用 STL 实现一个简单的哈希集合。

---

## 💡 要点总结

1. **链表**：灵活插删，但随机访问慢
2. **栈**：LIFO，用于括号匹配、表达式求值
3. **队列**：FIFO，用于 BFS、缓冲
4. **优先队列**：快速获取最值，基于堆实现
5. **BST**：有序存储，O(log n) 查找
6. **哈希表**：O(1) 平均查找，处理冲突是关键

---

## ⏭️ 下一节

[3.6 实战练习题](./06_practical_problems.md) - 综合练习

