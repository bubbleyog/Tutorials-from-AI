/**
 * @file move_demo.cpp
 * @brief 移动语义与完美转发示例
 * 
 * 编译：g++ -std=c++20 -Wall -o move_demo move_demo.cpp
 * 运行：./move_demo
 */

#include <iostream>
#include <string>
#include <vector>
#include <utility>

// ============================================================
// 支持移动语义的类
// ============================================================

class Buffer {
private:
    int* data_;
    size_t size_;
    std::string name_;

public:
    // 构造函数
    Buffer(size_t size, const std::string& name)
        : data_(new int[size]), size_(size), name_(name) {
        std::fill(data_, data_ + size, 0);
        std::cout << "  [构造] " << name_ << " (size=" << size_ << ")\n";
    }
    
    // 析构函数
    ~Buffer() {
        if (data_) {
            std::cout << "  [析构] " << name_ << "\n";
            delete[] data_;
        }
    }
    
    // 拷贝构造函数
    Buffer(const Buffer& other)
        : data_(new int[other.size_]), size_(other.size_), name_(other.name_ + "_copy") {
        std::copy(other.data_, other.data_ + size_, data_);
        std::cout << "  [拷贝构造] " << name_ << " from " << other.name_ << "\n";
    }
    
    // 拷贝赋值运算符
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new int[size_];
            std::copy(other.data_, other.data_ + size_, data_);
            name_ = other.name_ + "_assigned";
            std::cout << "  [拷贝赋值] " << name_ << " from " << other.name_ << "\n";
        }
        return *this;
    }
    
    // 移动构造函数
    Buffer(Buffer&& other) noexcept
        : data_(other.data_), size_(other.size_), name_(std::move(other.name_)) {
        other.data_ = nullptr;
        other.size_ = 0;
        std::cout << "  [移动构造] " << name_ << "\n";
    }
    
    // 移动赋值运算符
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            name_ = std::move(other.name_);
            other.data_ = nullptr;
            other.size_ = 0;
            std::cout << "  [移动赋值] " << name_ << "\n";
        }
        return *this;
    }
    
    size_t size() const { return size_; }
    const std::string& name() const { return name_; }
    bool valid() const { return data_ != nullptr; }
};

// ============================================================
// 1. 移动构造 vs 拷贝构造
// ============================================================

void demo_move_vs_copy() {
    std::cout << "\n=== 移动 vs 拷贝 ===\n";
    
    std::cout << "\n-- 拷贝 --\n";
    Buffer b1(1000, "Original");
    Buffer b2 = b1;  // 拷贝构造
    std::cout << "  b1 有效: " << std::boolalpha << b1.valid() << "\n";
    std::cout << "  b2 有效: " << b2.valid() << "\n";
    
    std::cout << "\n-- 移动 --\n";
    Buffer b3(1000, "ToMove");
    Buffer b4 = std::move(b3);  // 移动构造
    std::cout << "  b3 有效: " << b3.valid() << " (资源已被移走)\n";
    std::cout << "  b4 有效: " << b4.valid() << "\n";
}

// ============================================================
// 2. std::move 的本质
// ============================================================

void demo_std_move() {
    std::cout << "\n=== std::move 的本质 ===\n";
    
    std::string s1 = "Hello, World!";
    std::cout << "  s1 = \"" << s1 << "\"\n";
    
    // std::move 只是类型转换，不会移动
    std::string&& rref = std::move(s1);
    std::cout << "  std::move(s1) 后，s1 = \"" << s1 << "\" (未改变!)\n";
    
    // 真正的移动发生在这里
    std::string s2 = std::move(s1);
    std::cout << "  s2 = std::move(s1) 后:\n";
    std::cout << "    s1 = \"" << s1 << "\" (可能为空)\n";
    std::cout << "    s2 = \"" << s2 << "\"\n";
}

// ============================================================
// 3. 函数参数传递
// ============================================================

void sink(Buffer buffer) {
    std::cout << "  sink() 收到: " << buffer.name() << "\n";
}

void demo_parameter_passing() {
    std::cout << "\n=== 函数参数传递 ===\n";
    
    std::cout << "\n-- 传递左值（拷贝） --\n";
    Buffer b1(100, "Buffer1");
    sink(b1);  // 拷贝
    
    std::cout << "\n-- 传递右值（移动） --\n";
    sink(Buffer(100, "Temporary"));  // 临时对象，移动
    
    std::cout << "\n-- 使用 std::move --\n";
    Buffer b2(100, "Buffer2");
    sink(std::move(b2));  // 显式移动
    std::cout << "  b2 有效: " << std::boolalpha << b2.valid() << "\n";
}

// ============================================================
// 4. 值类别
// ============================================================

void take_lvalue(int& x) { std::cout << "  左值: " << x << "\n"; }
void take_rvalue(int&& x) { std::cout << "  右值: " << x << "\n"; }

void demo_value_categories() {
    std::cout << "\n=== 值类别 ===\n";
    
    int x = 10;
    
    // 左值
    take_lvalue(x);           // x 是左值
    // take_lvalue(42);       // 错误：42 是右值
    
    // 右值
    take_rvalue(42);          // 42 是右值
    take_rvalue(x + 1);       // x + 1 是右值
    take_rvalue(std::move(x)); // std::move(x) 是右值
    // take_rvalue(x);        // 错误：x 是左值
}

// ============================================================
// 5. 完美转发
// ============================================================

void process(int& x) { std::cout << "  process(int&): " << x << "\n"; }
void process(int&& x) { std::cout << "  process(int&&): " << x << "\n"; }

// 不使用转发：总是调用左值版本
template<typename T>
void wrapper_bad(T&& arg) {
    process(arg);  // arg 总是左值！
}

// 使用完美转发
template<typename T>
void wrapper_good(T&& arg) {
    process(std::forward<T>(arg));
}

void demo_perfect_forwarding() {
    std::cout << "\n=== 完美转发 ===\n";
    
    int x = 10;
    
    std::cout << "\n-- 不使用转发 --\n";
    wrapper_bad(x);   // 左值，但内部调用左值版本
    wrapper_bad(20);  // 右值，但内部仍调用左值版本！
    
    std::cout << "\n-- 使用 std::forward --\n";
    wrapper_good(x);   // 左值 -> process(int&)
    wrapper_good(20);  // 右值 -> process(int&&)
}

// ============================================================
// 6. 在容器中使用移动
// ============================================================

void demo_move_in_containers() {
    std::cout << "\n=== 容器中的移动 ===\n";
    
    std::vector<std::string> vec;
    
    std::string s = "Hello";
    
    std::cout << "\n-- push_back 拷贝 --\n";
    vec.push_back(s);
    std::cout << "  s = \"" << s << "\"\n";
    
    std::cout << "\n-- push_back 移动 --\n";
    vec.push_back(std::move(s));
    std::cout << "  s = \"" << s << "\" (可能为空)\n";
    
    std::cout << "\n-- emplace_back --\n";
    vec.emplace_back("World");  // 原地构造
    
    std::cout << "\n  容器内容: ";
    for (const auto& item : vec) {
        std::cout << "\"" << item << "\" ";
    }
    std::cout << "\n";
}

// ============================================================
// 7. 返回值优化
// ============================================================

Buffer create_buffer() {
    Buffer b(500, "Created");
    return b;  // NRVO 或隐式移动
}

void demo_return_value() {
    std::cout << "\n=== 返回值优化 ===\n";
    
    std::cout << "\n-- 创建并返回 --\n";
    Buffer b = create_buffer();
    std::cout << "  收到: " << b.name() << "\n";
    
    // 注意：不要对返回的局部变量使用 std::move
    // return std::move(local);  // 反而会阻止 NRVO！
}

// ============================================================
// 8. 移动后的状态
// ============================================================

void demo_moved_from_state() {
    std::cout << "\n=== 移动后的状态 ===\n";
    
    std::string s = "Hello";
    std::string s2 = std::move(s);
    
    // 移动后对象处于有效但未指定状态
    std::cout << "  移动后:\n";
    std::cout << "    s 为空: " << s.empty() << "\n";
    std::cout << "    s.size(): " << s.size() << "\n";
    
    // 可以重新赋值
    s = "New Value";
    std::cout << "  重新赋值后: s = \"" << s << "\"\n";
    
    // 可以销毁
    // s 离开作用域时正常销毁
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================\n";
    std::cout << "     移动语义与完美转发示例\n";
    std::cout << "========================================\n";
    
    demo_move_vs_copy();
    demo_std_move();
    demo_parameter_passing();
    demo_value_categories();
    demo_perfect_forwarding();
    demo_move_in_containers();
    demo_return_value();
    demo_moved_from_state();
    
    std::cout << "\n========================================\n";
    std::cout << "            示例结束\n";
    std::cout << "========================================\n";
    
    return 0;
}

