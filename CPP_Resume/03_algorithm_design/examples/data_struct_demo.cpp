/**
 * @file data_struct_demo.cpp
 * @brief 数据结构示例
 * 
 * 编译：g++ -std=c++20 -O2 -Wall -o data_struct_demo data_struct_demo.cpp
 * 运行：./data_struct_demo
 */

#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <list>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <functional>

//==============================================================================
// 1. 链表实现
//==============================================================================

template <typename T>
struct ListNode {
    T data;
    ListNode* next;
    ListNode(T val) : data(val), next(nullptr) {}
};

template <typename T>
class LinkedList {
private:
    ListNode<T>* head;
    int size;
    
public:
    LinkedList() : head(nullptr), size(0) {}
    
    ~LinkedList() {
        while (head) {
            ListNode<T>* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    void push_front(T val) {
        ListNode<T>* node = new ListNode<T>(val);
        node->next = head;
        head = node;
        ++size;
    }
    
    void push_back(T val) {
        ListNode<T>* node = new ListNode<T>(val);
        if (!head) {
            head = node;
        } else {
            ListNode<T>* curr = head;
            while (curr->next) curr = curr->next;
            curr->next = node;
        }
        ++size;
    }
    
    void pop_front() {
        if (!head) return;
        ListNode<T>* temp = head;
        head = head->next;
        delete temp;
        --size;
    }
    
    bool find(T val) const {
        ListNode<T>* curr = head;
        while (curr) {
            if (curr->data == val) return true;
            curr = curr->next;
        }
        return false;
    }
    
    void print() const {
        ListNode<T>* curr = head;
        std::cout << "[";
        while (curr) {
            std::cout << curr->data;
            if (curr->next) std::cout << " -> ";
            curr = curr->next;
        }
        std::cout << "]" << std::endl;
    }
    
    int get_size() const { return size; }
};

// 链表反转
ListNode<int>* reverse_list(ListNode<int>* head) {
    ListNode<int>* prev = nullptr;
    while (head) {
        ListNode<int>* next = head->next;
        head->next = prev;
        prev = head;
        head = next;
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

//==============================================================================
// 2. 栈实现
//==============================================================================

template <typename T>
class Stack {
private:
    std::vector<T> data;
    
public:
    void push(T val) { data.push_back(val); }
    void pop() { if (!empty()) data.pop_back(); }
    T& top() { return data.back(); }
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

// 括号匹配
bool is_valid_parentheses(const std::string& s) {
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

// 逆波兰表达式
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

//==============================================================================
// 3. 队列实现
//==============================================================================

template <typename T>
class Queue {
private:
    std::list<T> data;
    
public:
    void enqueue(T val) { data.push_back(val); }
    void dequeue() { if (!empty()) data.pop_front(); }
    T& front() { return data.front(); }
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

//==============================================================================
// 4. 二叉树
//==============================================================================

template <typename T>
struct TreeNode {
    T data;
    TreeNode* left;
    TreeNode* right;
    TreeNode(T val) : data(val), left(nullptr), right(nullptr) {}
};

// 遍历方式
void preorder(TreeNode<int>* root, std::vector<int>& result) {
    if (!root) return;
    result.push_back(root->data);
    preorder(root->left, result);
    preorder(root->right, result);
}

void inorder(TreeNode<int>* root, std::vector<int>& result) {
    if (!root) return;
    inorder(root->left, result);
    result.push_back(root->data);
    inorder(root->right, result);
}

void postorder(TreeNode<int>* root, std::vector<int>& result) {
    if (!root) return;
    postorder(root->left, result);
    postorder(root->right, result);
    result.push_back(root->data);
}

void levelorder(TreeNode<int>* root, std::vector<int>& result) {
    if (!root) return;
    std::queue<TreeNode<int>*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode<int>* node = q.front();
        q.pop();
        result.push_back(node->data);
        if (node->left) q.push(node->left);
        if (node->right) q.push(node->right);
    }
}

int tree_height(TreeNode<int>* root) {
    if (!root) return 0;
    return 1 + std::max(tree_height(root->left), tree_height(root->right));
}

//==============================================================================
// 5. 二叉搜索树
//==============================================================================

class BST {
private:
    TreeNode<int>* root;
    
    TreeNode<int>* insert_helper(TreeNode<int>* node, int val) {
        if (!node) return new TreeNode<int>(val);
        if (val < node->data) node->left = insert_helper(node->left, val);
        else if (val > node->data) node->right = insert_helper(node->right, val);
        return node;
    }
    
    TreeNode<int>* find_min(TreeNode<int>* node) {
        while (node->left) node = node->left;
        return node;
    }
    
    TreeNode<int>* remove_helper(TreeNode<int>* node, int val) {
        if (!node) return nullptr;
        if (val < node->data) {
            node->left = remove_helper(node->left, val);
        } else if (val > node->data) {
            node->right = remove_helper(node->right, val);
        } else {
            if (!node->left) {
                TreeNode<int>* temp = node->right;
                delete node;
                return temp;
            }
            if (!node->right) {
                TreeNode<int>* temp = node->left;
                delete node;
                return temp;
            }
            TreeNode<int>* min_node = find_min(node->right);
            node->data = min_node->data;
            node->right = remove_helper(node->right, min_node->data);
        }
        return node;
    }
    
    void inorder_helper(TreeNode<int>* node, std::vector<int>& result) {
        if (!node) return;
        inorder_helper(node->left, result);
        result.push_back(node->data);
        inorder_helper(node->right, result);
    }
    
public:
    BST() : root(nullptr) {}
    
    void insert(int val) { root = insert_helper(root, val); }
    
    bool search(int val) {
        TreeNode<int>* curr = root;
        while (curr) {
            if (val == curr->data) return true;
            if (val < curr->data) curr = curr->left;
            else curr = curr->right;
        }
        return false;
    }
    
    void remove(int val) { root = remove_helper(root, val); }
    
    std::vector<int> inorder() {
        std::vector<int> result;
        inorder_helper(root, result);
        return result;
    }
};

//==============================================================================
// 6. 简单哈希表
//==============================================================================

class HashSet {
private:
    static const int BUCKET_SIZE = 100;
    std::vector<std::list<int>> buckets;
    
    int hash(int key) const { return key % BUCKET_SIZE; }
    
public:
    HashSet() : buckets(BUCKET_SIZE) {}
    
    void add(int key) {
        int idx = hash(key);
        for (int x : buckets[idx]) {
            if (x == key) return;
        }
        buckets[idx].push_back(key);
    }
    
    void remove(int key) {
        int idx = hash(key);
        buckets[idx].remove(key);
    }
    
    bool contains(int key) const {
        int idx = hash(key);
        for (int x : buckets[idx]) {
            if (x == key) return true;
        }
        return false;
    }
};

//==============================================================================
// 7. 堆实现
//==============================================================================

class MaxHeap {
private:
    std::vector<int> data;
    
    void sift_up(int idx) {
        while (idx > 0) {
            int parent = (idx - 1) / 2;
            if (data[parent] < data[idx]) {
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
            
            if (left < n && data[left] > data[largest]) largest = left;
            if (right < n && data[right] > data[largest]) largest = right;
            
            if (largest != idx) {
                std::swap(data[idx], data[largest]);
                idx = largest;
            } else {
                break;
            }
        }
    }
    
public:
    void push(int val) {
        data.push_back(val);
        sift_up(data.size() - 1);
    }
    
    void pop() {
        if (data.empty()) return;
        data[0] = data.back();
        data.pop_back();
        if (!data.empty()) sift_down(0);
    }
    
    int top() const { return data[0]; }
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

//==============================================================================
// 辅助函数
//==============================================================================

template<typename Container>
void print_container(const std::string& label, const Container& c) {
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
// 主函数
//==============================================================================

int main() {
    std::cout << "===== 数据结构示例 =====" << std::endl;
    
    // ========== 1. 链表 ==========
    std::cout << "\n【1. 链表】" << std::endl;
    LinkedList<int> list;
    list.push_back(1);
    list.push_back(2);
    list.push_back(3);
    list.push_front(0);
    std::cout << "链表: ";
    list.print();
    std::cout << "查找 2: " << std::boolalpha << list.find(2) << std::endl;
    std::cout << "查找 5: " << list.find(5) << std::endl;
    
    // ========== 2. 栈 ==========
    std::cout << "\n【2. 栈】" << std::endl;
    Stack<int> st;
    st.push(1);
    st.push(2);
    st.push(3);
    std::cout << "栈顶: " << st.top() << std::endl;
    st.pop();
    std::cout << "弹出后栈顶: " << st.top() << std::endl;
    
    // 括号匹配
    std::cout << "\n【括号匹配】" << std::endl;
    std::vector<std::string> tests = {"()", "()[]{}", "(]", "([)]", "{[]}"};
    for (const auto& s : tests) {
        std::cout << "\"" << s << "\": " << is_valid_parentheses(s) << std::endl;
    }
    
    // 逆波兰表达式
    std::cout << "\n【逆波兰表达式】" << std::endl;
    std::vector<std::string> rpn = {"2", "1", "+", "3", "*"};
    std::cout << "表达式: [2, 1, +, 3, *] = " << eval_rpn(rpn) << std::endl;
    
    // ========== 3. 队列 ==========
    std::cout << "\n【3. 队列】" << std::endl;
    Queue<int> q;
    q.enqueue(1);
    q.enqueue(2);
    q.enqueue(3);
    std::cout << "队首: " << q.front() << std::endl;
    q.dequeue();
    std::cout << "出队后队首: " << q.front() << std::endl;
    
    // ========== 4. 二叉树 ==========
    std::cout << "\n【4. 二叉树】" << std::endl;
    
    //       1
    //      / \
    //     2   3
    //    / \   \
    //   4   5   6
    
    TreeNode<int>* tree_root = new TreeNode<int>(1);
    tree_root->left = new TreeNode<int>(2);
    tree_root->right = new TreeNode<int>(3);
    tree_root->left->left = new TreeNode<int>(4);
    tree_root->left->right = new TreeNode<int>(5);
    tree_root->right->right = new TreeNode<int>(6);
    
    std::vector<int> pre_result, in_result, post_result, level_result;
    preorder(tree_root, pre_result);
    inorder(tree_root, in_result);
    postorder(tree_root, post_result);
    levelorder(tree_root, level_result);
    
    print_container("前序遍历", pre_result);
    print_container("中序遍历", in_result);
    print_container("后序遍历", post_result);
    print_container("层序遍历", level_result);
    std::cout << "树高度: " << tree_height(tree_root) << std::endl;
    
    // ========== 5. 二叉搜索树 ==========
    std::cout << "\n【5. 二叉搜索树】" << std::endl;
    BST bst;
    for (int x : {5, 3, 7, 2, 4, 6, 8}) {
        bst.insert(x);
    }
    print_container("BST 中序遍历", bst.inorder());
    std::cout << "查找 4: " << bst.search(4) << std::endl;
    std::cout << "查找 9: " << bst.search(9) << std::endl;
    bst.remove(3);
    print_container("删除 3 后", bst.inorder());
    
    // ========== 6. 哈希集合 ==========
    std::cout << "\n【6. 哈希集合】" << std::endl;
    HashSet hs;
    hs.add(1);
    hs.add(2);
    hs.add(3);
    std::cout << "contains(2): " << hs.contains(2) << std::endl;
    hs.remove(2);
    std::cout << "删除后 contains(2): " << hs.contains(2) << std::endl;
    
    // ========== 7. 最大堆 ==========
    std::cout << "\n【7. 最大堆】" << std::endl;
    MaxHeap heap;
    for (int x : {3, 1, 4, 1, 5, 9, 2, 6}) {
        heap.push(x);
    }
    std::cout << "堆顶: " << heap.top() << std::endl;
    std::cout << "依次弹出: ";
    while (!heap.empty()) {
        std::cout << heap.top() << " ";
        heap.pop();
    }
    std::cout << std::endl;
    
    // ========== 8. 使用 STL 优先队列 ==========
    std::cout << "\n【8. STL 优先队列】" << std::endl;
    std::priority_queue<int> max_pq;
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_pq;
    
    for (int x : {3, 1, 4, 1, 5, 9, 2, 6}) {
        max_pq.push(x);
        min_pq.push(x);
    }
    
    std::cout << "最大堆顶: " << max_pq.top() << std::endl;
    std::cout << "最小堆顶: " << min_pq.top() << std::endl;
    
    std::cout << "\n===== 完成 =====" << std::endl;
    return 0;
}

