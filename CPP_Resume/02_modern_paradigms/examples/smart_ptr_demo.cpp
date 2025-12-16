/**
 * @file smart_ptr_demo.cpp
 * @brief 智能指针详解示例
 * 
 * 编译：g++ -std=c++20 -Wall -o smart_ptr_demo smart_ptr_demo.cpp
 * 运行：./smart_ptr_demo
 */

#include <iostream>
#include <memory>
#include <vector>
#include <string>

// ============================================================
// 辅助类
// ============================================================

class Widget {
public:
    int id;
    std::string name;
    
    Widget(int id, const std::string& name) : id(id), name(name) {
        std::cout << "  [Widget] 创建: " << name << " (id=" << id << ")\n";
    }
    
    ~Widget() {
        std::cout << "  [Widget] 销毁: " << name << " (id=" << id << ")\n";
    }
    
    void use() const {
        std::cout << "  [Widget] 使用: " << name << "\n";
    }
};

// ============================================================
// 1. unique_ptr 基础
// ============================================================

void demo_unique_ptr_basics() {
    std::cout << "\n=== unique_ptr 基础 ===\n";
    
    // 创建
    auto p1 = std::make_unique<Widget>(1, "Widget-1");
    p1->use();
    
    // 获取裸指针
    Widget* raw = p1.get();
    std::cout << "  裸指针: " << raw << "\n";
    
    // 检查非空
    if (p1) {
        std::cout << "  p1 非空\n";
    }
    
    // reset
    p1.reset();  // 释放并置空
    if (!p1) {
        std::cout << "  p1 现在为空\n";
    }
    
    // reset 到新对象
    p1.reset(new Widget(2, "Widget-2"));
    
    // release：释放所有权
    Widget* released = p1.release();
    std::cout << "  release 后 p1 " << (p1 ? "非空" : "为空") << "\n";
    delete released;  // 需要手动删除
}

// ============================================================
// 2. unique_ptr 所有权转移
// ============================================================

std::unique_ptr<Widget> create_widget(int id) {
    return std::make_unique<Widget>(id, "Factory-Widget");
}

void take_widget(std::unique_ptr<Widget> w) {
    std::cout << "  接管 Widget\n";
    w->use();
    // 函数结束时 w 被销毁
}

void demo_unique_ptr_ownership() {
    std::cout << "\n=== unique_ptr 所有权转移 ===\n";
    
    // 从工厂函数获取
    auto w1 = create_widget(10);
    w1->use();
    
    // 转移到另一个变量
    auto w2 = std::move(w1);
    std::cout << "  move 后 w1 " << (w1 ? "非空" : "为空") << "\n";
    
    // 转移给函数
    take_widget(std::move(w2));
    std::cout << "  函数调用后 w2 " << (w2 ? "非空" : "为空") << "\n";
}

// ============================================================
// 3. unique_ptr 与数组
// ============================================================

void demo_unique_ptr_array() {
    std::cout << "\n=== unique_ptr 与数组 ===\n";
    
    auto arr = std::make_unique<int[]>(5);
    
    for (int i = 0; i < 5; ++i) {
        arr[i] = i * 10;
    }
    
    std::cout << "  数组内容: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << "\n";
}

// ============================================================
// 4. shared_ptr 基础
// ============================================================

void demo_shared_ptr_basics() {
    std::cout << "\n=== shared_ptr 基础 ===\n";
    
    auto p1 = std::make_shared<Widget>(100, "Shared-Widget");
    std::cout << "  use_count: " << p1.use_count() << "\n";
    
    {
        auto p2 = p1;  // 共享所有权
        std::cout << "  p2 = p1 后 use_count: " << p1.use_count() << "\n";
        
        auto p3 = p1;
        std::cout << "  p3 = p1 后 use_count: " << p1.use_count() << "\n";
    }
    
    std::cout << "  p2, p3 离开作用域后 use_count: " << p1.use_count() << "\n";
    
    p1.reset();
    std::cout << "  p1.reset() 后，Widget 被销毁\n";
}

// ============================================================
// 5. weak_ptr 避免循环引用
// ============================================================

class Node {
public:
    std::string name;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev;  // 使用 weak_ptr 避免循环
    
    Node(const std::string& n) : name(n) {
        std::cout << "  [Node] 创建: " << name << "\n";
    }
    
    ~Node() {
        std::cout << "  [Node] 销毁: " << name << "\n";
    }
};

void demo_weak_ptr() {
    std::cout << "\n=== weak_ptr 避免循环引用 ===\n";
    
    {
        auto node1 = std::make_shared<Node>("Node-1");
        auto node2 = std::make_shared<Node>("Node-2");
        
        node1->next = node2;
        node2->prev = node1;  // weak_ptr 不增加引用计数
        
        std::cout << "  node1 use_count: " << node1.use_count() << "\n";
        std::cout << "  node2 use_count: " << node2.use_count() << "\n";
        
        // 通过 weak_ptr 访问
        if (auto prev = node2->prev.lock()) {
            std::cout << "  node2 的前驱是: " << prev->name << "\n";
        }
    }
    
    std::cout << "  所有节点已正确销毁\n";
}

// ============================================================
// 6. enable_shared_from_this
// ============================================================

class Server : public std::enable_shared_from_this<Server> {
public:
    std::string name;
    
    Server(const std::string& n) : name(n) {
        std::cout << "  [Server] 创建: " << name << "\n";
    }
    
    ~Server() {
        std::cout << "  [Server] 销毁: " << name << "\n";
    }
    
    std::shared_ptr<Server> get_shared() {
        return shared_from_this();
    }
    
    void register_callback() {
        auto self = shared_from_this();
        std::cout << "  注册回调，引用计数: " << self.use_count() << "\n";
    }
};

void demo_enable_shared_from_this() {
    std::cout << "\n=== enable_shared_from_this ===\n";
    
    auto server = std::make_shared<Server>("MainServer");
    std::cout << "  初始引用计数: " << server.use_count() << "\n";
    
    auto another = server->get_shared();
    std::cout << "  get_shared() 后引用计数: " << server.use_count() << "\n";
    
    server->register_callback();
}

// ============================================================
// 7. 自定义删除器
// ============================================================

void demo_custom_deleter() {
    std::cout << "\n=== 自定义删除器 ===\n";
    
    // unique_ptr 自定义删除器
    auto deleter = [](int* p) {
        std::cout << "  自定义删除器: 删除 int* 值为 " << *p << "\n";
        delete p;
    };
    
    {
        std::unique_ptr<int, decltype(deleter)> p(new int(42), deleter);
        std::cout << "  值: " << *p << "\n";
    }
    
    // shared_ptr 自定义删除器（类型擦除）
    {
        std::shared_ptr<int> p(new int(100), [](int* p) {
            std::cout << "  shared_ptr 自定义删除器: " << *p << "\n";
            delete p;
        });
    }
}

// ============================================================
// 8. 在容器中使用
// ============================================================

void demo_smart_ptr_containers() {
    std::cout << "\n=== 智能指针与容器 ===\n";
    
    std::vector<std::unique_ptr<Widget>> vec;
    
    vec.push_back(std::make_unique<Widget>(1, "Vec-1"));
    vec.push_back(std::make_unique<Widget>(2, "Vec-2"));
    vec.push_back(std::make_unique<Widget>(3, "Vec-3"));
    
    std::cout << "  遍历容器:\n";
    for (const auto& w : vec) {
        std::cout << "    - " << w->name << "\n";
    }
    
    std::cout << "  清空容器...\n";
    vec.clear();
    std::cout << "  所有 Widget 已销毁\n";
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================\n";
    std::cout << "        智能指针详解示例\n";
    std::cout << "========================================\n";
    
    demo_unique_ptr_basics();
    demo_unique_ptr_ownership();
    demo_unique_ptr_array();
    demo_shared_ptr_basics();
    demo_weak_ptr();
    demo_enable_shared_from_this();
    demo_custom_deleter();
    demo_smart_ptr_containers();
    
    std::cout << "\n========================================\n";
    std::cout << "            示例结束\n";
    std::cout << "========================================\n";
    
    return 0;
}

