/**
 * @file pointer_demo.cpp
 * @brief 指针与引用示例
 * 
 * 演示内容：
 * - 指针基础
 * - 引用
 * - const 与指针/引用
 * - 动态内存分配
 * - 智能指针预览
 * 
 * 编译：g++ -std=c++20 -Wall -o pointer_demo pointer_demo.cpp
 * 运行：./pointer_demo
 */

#include <iostream>
#include <memory>
#include <vector>

// ============================================================
// 1. 指针基础
// ============================================================

void demo_pointer_basics() {
    std::cout << "=== 指针基础 ===" << std::endl;
    
    int value = 42;
    int* ptr = &value;  // ptr 指向 value
    
    std::cout << "value 的值: " << value << std::endl;
    std::cout << "value 的地址: " << &value << std::endl;
    std::cout << "ptr 的值 (地址): " << ptr << std::endl;
    std::cout << "ptr 指向的值 (*ptr): " << *ptr << std::endl;
    
    // 通过指针修改值
    *ptr = 100;
    std::cout << "修改后 value 的值: " << value << std::endl;
    
    // 空指针
    int* null_ptr = nullptr;  // C++11 推荐使用 nullptr
    if (null_ptr == nullptr) {
        std::cout << "null_ptr 是空指针" << std::endl;
    }
    
    std::cout << std::endl;
}

// ============================================================
// 2. 指针与数组
// ============================================================

void demo_pointer_array() {
    std::cout << "=== 指针与数组 ===" << std::endl;
    
    int arr[] = {10, 20, 30, 40, 50};
    int* p = arr;  // 数组名退化为指针
    
    std::cout << "使用指针遍历数组: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << *(p + i) << " ";
    }
    std::cout << std::endl;
    
    // 指针算术
    std::cout << "p[0] = " << p[0] << std::endl;
    std::cout << "*(p+2) = " << *(p + 2) << std::endl;
    
    // 指针遍历
    std::cout << "使用指针迭代: ";
    for (int* ptr = arr; ptr < arr + 5; ++ptr) {
        std::cout << *ptr << " ";
    }
    std::cout << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 3. 引用
// ============================================================

void demo_references() {
    std::cout << "=== 引用 ===" << std::endl;
    
    int original = 42;
    int& ref = original;  // ref 是 original 的引用
    
    std::cout << "original: " << original << std::endl;
    std::cout << "ref: " << ref << std::endl;
    std::cout << "original 地址: " << &original << std::endl;
    std::cout << "ref 地址: " << &ref << " (相同!)" << std::endl;
    
    // 通过引用修改
    ref = 100;
    std::cout << "修改 ref 后, original: " << original << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 4. 指针 vs 引用在函数参数中的使用
// ============================================================

// 值传递
void by_value(int x) {
    x = 999;
    std::cout << "  by_value 内部 x = " << x << std::endl;
}

// 引用传递
void by_reference(int& x) {
    x = 999;
    std::cout << "  by_reference 内部 x = " << x << std::endl;
}

// 指针传递
void by_pointer(int* x) {
    if (x != nullptr) {
        *x = 999;
        std::cout << "  by_pointer 内部 *x = " << *x << std::endl;
    }
}

// const 引用（避免拷贝，不修改）
void print_vector(const std::vector<int>& v) {
    std::cout << "  向量内容: ";
    for (const auto& x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;
}

void demo_parameter_passing() {
    std::cout << "=== 参数传递方式 ===" << std::endl;
    
    int a = 10;
    std::cout << "初始值 a = " << a << std::endl;
    
    by_value(a);
    std::cout << "by_value 后 a = " << a << std::endl;
    
    a = 10;  // 重置
    by_reference(a);
    std::cout << "by_reference 后 a = " << a << std::endl;
    
    a = 10;  // 重置
    by_pointer(&a);
    std::cout << "by_pointer 后 a = " << a << std::endl;
    
    std::vector<int> vec = {1, 2, 3, 4, 5};
    print_vector(vec);
    
    std::cout << std::endl;
}

// ============================================================
// 5. const 与指针
// ============================================================

void demo_const_pointer() {
    std::cout << "=== const 与指针 ===" << std::endl;
    
    int x = 10, y = 20;
    
    // 指向 const 的指针（不能通过指针修改值）
    const int* ptr1 = &x;
    std::cout << "const int* ptr1 指向 x: " << *ptr1 << std::endl;
    // *ptr1 = 100;  // 错误：不能修改
    ptr1 = &y;  // OK：可以重新指向
    std::cout << "ptr1 重新指向 y: " << *ptr1 << std::endl;
    
    // const 指针（指针本身不能改）
    int* const ptr2 = &x;
    *ptr2 = 100;  // OK：可以修改值
    // ptr2 = &y;  // 错误：不能重新指向
    std::cout << "int* const ptr2 修改 x 为: " << x << std::endl;
    
    // 指向 const 的 const 指针
    const int* const ptr3 = &y;
    std::cout << "const int* const ptr3: " << *ptr3 << std::endl;
    // 两者都不能改
    
    std::cout << std::endl;
}

// ============================================================
// 6. 动态内存分配
// ============================================================

void demo_dynamic_memory() {
    std::cout << "=== 动态内存分配 ===" << std::endl;
    
    // 分配单个对象
    int* p = new int(42);
    std::cout << "new int(42): " << *p << std::endl;
    delete p;
    p = nullptr;  // 好习惯
    
    // 分配数组
    int* arr = new int[5]{1, 2, 3, 4, 5};
    std::cout << "new int[5]: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    delete[] arr;  // 注意使用 delete[]
    arr = nullptr;
    
    std::cout << std::endl;
}

// ============================================================
// 7. 智能指针预览
// ============================================================

class Resource {
public:
    Resource(const std::string& name) : name_(name) {
        std::cout << "  Resource \"" << name_ << "\" 被创建" << std::endl;
    }
    
    ~Resource() {
        std::cout << "  Resource \"" << name_ << "\" 被销毁" << std::endl;
    }
    
    void use() const {
        std::cout << "  使用 Resource \"" << name_ << "\"" << std::endl;
    }

private:
    std::string name_;
};

void demo_smart_pointers() {
    std::cout << "=== 智能指针预览 ===" << std::endl;
    
    std::cout << "\n--- unique_ptr (独占所有权) ---" << std::endl;
    {
        auto p1 = std::make_unique<Resource>("UniqueResource");
        p1->use();
        // 离开作用域自动释放
    }
    std::cout << "离开作用域后资源已自动释放" << std::endl;
    
    std::cout << "\n--- shared_ptr (共享所有权) ---" << std::endl;
    {
        auto p2 = std::make_shared<Resource>("SharedResource");
        std::cout << "  引用计数: " << p2.use_count() << std::endl;
        
        {
            auto p3 = p2;  // 共享所有权
            std::cout << "  共享后引用计数: " << p2.use_count() << std::endl;
            p3->use();
        }
        
        std::cout << "  p3 离开作用域后引用计数: " << p2.use_count() << std::endl;
    }
    std::cout << "所有 shared_ptr 离开作用域后资源被释放" << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 8. 函数指针
// ============================================================

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }
int multiply(int a, int b) { return a * b; }

void demo_function_pointers() {
    std::cout << "=== 函数指针 ===" << std::endl;
    
    // 函数指针类型
    int (*operation)(int, int);
    
    operation = add;
    std::cout << "add(5, 3) = " << operation(5, 3) << std::endl;
    
    operation = subtract;
    std::cout << "subtract(5, 3) = " << operation(5, 3) << std::endl;
    
    operation = multiply;
    std::cout << "multiply(5, 3) = " << operation(5, 3) << std::endl;
    
    // 使用类型别名简化
    using BinaryOp = int(*)(int, int);
    BinaryOp op = add;
    std::cout << "使用类型别名: add(10, 20) = " << op(10, 20) << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      C++ 指针与引用示例程序" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << std::endl;
    
    demo_pointer_basics();
    demo_pointer_array();
    demo_references();
    demo_parameter_passing();
    demo_const_pointer();
    demo_dynamic_memory();
    demo_smart_pointers();
    demo_function_pointers();
    
    std::cout << "========================================" << std::endl;
    std::cout << "            示例结束" << std::endl;
    std::cout << "========================================" << std::endl;
    
    return 0;
}

