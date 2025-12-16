/**
 * @file basic_demo.cpp
 * @brief 基础语法示例
 * 
 * 演示内容：
 * - 数据类型和变量
 * - 运算符
 * - 控制流
 * - 函数
 * - 输入输出
 * 
 * 编译：g++ -std=c++20 -Wall -o basic_demo basic_demo.cpp
 * 运行：./basic_demo
 */

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

// ============================================================
// 1. 数据类型演示
// ============================================================

void demo_data_types() {
    std::cout << "=== 数据类型演示 ===" << std::endl;
    
    // 基本类型
    bool flag = true;
    char ch = 'A';
    int num = 42;
    double pi = 3.14159265358979;
    
    // auto 类型推断 (C++11)
    auto x = 100;           // int
    auto y = 3.14;          // double
    auto s = "Hello";       // const char*
    
    // 输出类型信息
    std::cout << "bool: " << std::boolalpha << flag << std::endl;
    std::cout << "char: " << ch << std::endl;
    std::cout << "int: " << num << std::endl;
    std::cout << "double: " << std::fixed << std::setprecision(10) << pi << std::endl;
    std::cout << "auto推断的int: " << x << std::endl;
    std::cout << std::endl;
}

// ============================================================
// 2. 常量演示
// ============================================================

// const 常量
const int MAX_VALUE = 100;

// constexpr 编译期常量 (C++11)
constexpr int ARRAY_SIZE = 10;
constexpr double PI = 3.14159265358979;

// constexpr 函数 (C++11)
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

void demo_constants() {
    std::cout << "=== 常量演示 ===" << std::endl;
    
    std::cout << "MAX_VALUE: " << MAX_VALUE << std::endl;
    std::cout << "ARRAY_SIZE: " << ARRAY_SIZE << std::endl;
    std::cout << "PI: " << PI << std::endl;
    
    // 编译期计算
    constexpr int fact5 = factorial(5);
    std::cout << "5! = " << fact5 << " (编译期计算)" << std::endl;
    std::cout << std::endl;
}

// ============================================================
// 3. 运算符演示
// ============================================================

void demo_operators() {
    std::cout << "=== 运算符演示 ===" << std::endl;
    
    int a = 10, b = 3;
    
    // 算术运算符
    std::cout << "算术运算符:" << std::endl;
    std::cout << "  " << a << " + " << b << " = " << (a + b) << std::endl;
    std::cout << "  " << a << " - " << b << " = " << (a - b) << std::endl;
    std::cout << "  " << a << " * " << b << " = " << (a * b) << std::endl;
    std::cout << "  " << a << " / " << b << " = " << (a / b) << std::endl;
    std::cout << "  " << a << " % " << b << " = " << (a % b) << std::endl;
    
    // 位运算符
    std::cout << "位运算符:" << std::endl;
    int x = 0b1010;  // 10 (C++14 二进制字面量)
    int y = 0b1100;  // 12
    std::cout << "  0b1010 & 0b1100 = " << (x & y) << " (AND)" << std::endl;
    std::cout << "  0b1010 | 0b1100 = " << (x | y) << " (OR)" << std::endl;
    std::cout << "  0b1010 ^ 0b1100 = " << (x ^ y) << " (XOR)" << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 4. 控制流演示
// ============================================================

void demo_control_flow() {
    std::cout << "=== 控制流演示 ===" << std::endl;
    
    // if-else
    int score = 85;
    char grade;
    if (score >= 90) {
        grade = 'A';
    } else if (score >= 80) {
        grade = 'B';
    } else if (score >= 70) {
        grade = 'C';
    } else {
        grade = 'D';
    }
    std::cout << "分数 " << score << " 对应等级: " << grade << std::endl;
    
    // 范围 for 循环 (C++11)
    std::vector<int> nums = {1, 2, 3, 4, 5};
    std::cout << "范围for循环遍历: ";
    for (const auto& n : nums) {
        std::cout << n << " ";
    }
    std::cout << std::endl;
    
    // C++17 if 语句中的初始化
    std::vector<int> data = {10, 20, 30};
    if (auto size = data.size(); size > 0) {
        std::cout << "C++17 if初始化: 容器大小为 " << size << std::endl;
    }
    
    std::cout << std::endl;
}

// ============================================================
// 5. 函数演示
// ============================================================

// 普通函数
int add(int a, int b) {
    return a + b;
}

// 默认参数
void greet(const std::string& name, const std::string& greeting = "Hello") {
    std::cout << greeting << ", " << name << "!" << std::endl;
}

// 函数重载
double add(double a, double b) {
    return a + b;
}

std::string add(const std::string& a, const std::string& b) {
    return a + b;
}

// C++14 auto 返回类型
auto multiply(int a, int b) {
    return a * b;
}

// Lambda 表达式 (C++11)
void demo_functions() {
    std::cout << "=== 函数演示 ===" << std::endl;
    
    // 普通函数调用
    std::cout << "add(3, 5) = " << add(3, 5) << std::endl;
    std::cout << "add(3.14, 2.86) = " << add(3.14, 2.86) << std::endl;
    std::cout << "add(\"Hello, \", \"World\") = " << add("Hello, ", "World") << std::endl;
    
    // 默认参数
    greet("Alice");
    greet("Bob", "Hi");
    
    // auto 返回类型
    std::cout << "multiply(6, 7) = " << multiply(6, 7) << std::endl;
    
    // Lambda 表达式
    auto square = [](int x) { return x * x; };
    std::cout << "Lambda square(5) = " << square(5) << std::endl;
    
    // 带捕获的 Lambda
    int factor = 3;
    auto times = [factor](int x) { return x * factor; };
    std::cout << "Lambda times(5) = " << times(5) << std::endl;
    
    // 泛型 Lambda (C++14)
    auto generic_add = [](auto a, auto b) { return a + b; };
    std::cout << "泛型Lambda generic_add(1, 2) = " << generic_add(1, 2) << std::endl;
    std::cout << "泛型Lambda generic_add(1.5, 2.5) = " << generic_add(1.5, 2.5) << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 6. 命名空间演示
// ============================================================

namespace MyMath {
    constexpr double PI = 3.14159265358979;
    
    double circle_area(double radius) {
        return PI * radius * radius;
    }
    
    namespace Geometry {  // 嵌套命名空间
        double square_area(double side) {
            return side * side;
        }
    }
}

// C++17 嵌套命名空间简写
namespace Physics::Mechanics {
    double kinetic_energy(double mass, double velocity) {
        return 0.5 * mass * velocity * velocity;
    }
}

void demo_namespaces() {
    std::cout << "=== 命名空间演示 ===" << std::endl;
    
    std::cout << "MyMath::PI = " << MyMath::PI << std::endl;
    std::cout << "MyMath::circle_area(5) = " << MyMath::circle_area(5) << std::endl;
    std::cout << "MyMath::Geometry::square_area(4) = " << MyMath::Geometry::square_area(4) << std::endl;
    std::cout << "Physics::Mechanics::kinetic_energy(10, 5) = " 
              << Physics::Mechanics::kinetic_energy(10, 5) << std::endl;
    
    // using 声明
    using MyMath::circle_area;
    std::cout << "使用using后: circle_area(3) = " << circle_area(3) << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "      C++ 基础语法示例程序" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << std::endl;
    
    demo_data_types();
    demo_constants();
    demo_operators();
    demo_control_flow();
    demo_functions();
    demo_namespaces();
    
    std::cout << "========================================" << std::endl;
    std::cout << "            示例结束" << std::endl;
    std::cout << "========================================" << std::endl;
    
    return 0;
}

