/**
 * @file class_demo.cpp
 * @brief 类与对象示例
 * 
 * 演示内容：
 * - 类的定义和使用
 * - 构造函数与析构函数
 * - 继承与多态
 * - 运算符重载
 * - 现代 C++ 类特性
 * 
 * 编译：g++ -std=c++20 -Wall -o class_demo class_demo.cpp
 * 运行：./class_demo
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cmath>

// ============================================================
// 1. 基本类定义
// ============================================================

class Person {
private:
    std::string name_;
    int age_;

public:
    // 构造函数（使用成员初始化列表）
    Person(const std::string& name, int age) 
        : name_(name), age_(age) {
        std::cout << "  Person \"" << name_ << "\" 被创建" << std::endl;
    }
    
    // 析构函数
    ~Person() {
        std::cout << "  Person \"" << name_ << "\" 被销毁" << std::endl;
    }
    
    // 成员函数
    void introduce() const {
        std::cout << "  我是 " << name_ << ", " << age_ << " 岁" << std::endl;
    }
    
    // Getter
    std::string get_name() const { return name_; }
    int get_age() const { return age_; }
    
    // Setter
    void set_age(int age) { age_ = age; }
};

void demo_basic_class() {
    std::cout << "=== 基本类定义 ===" << std::endl;
    
    {
        Person alice("Alice", 25);
        alice.introduce();
        
        alice.set_age(26);
        std::cout << "  生日后年龄: " << alice.get_age() << std::endl;
    }
    std::cout << "离开作用域，析构函数被调用" << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 2. 现代类特性：default, delete, 类内初始化
// ============================================================

class ModernWidget {
private:
    int value_ = 0;                    // C++11 类内初始化
    std::string name_ = "unnamed";

public:
    // 显式使用默认构造函数
    ModernWidget() = default;
    
    // 自定义构造函数
    ModernWidget(int v, const std::string& n) 
        : value_(v), name_(n) {}
    
    // 禁止拷贝
    ModernWidget(const ModernWidget&) = delete;
    ModernWidget& operator=(const ModernWidget&) = delete;
    
    // 允许移动
    ModernWidget(ModernWidget&&) = default;
    ModernWidget& operator=(ModernWidget&&) = default;
    
    void print() const {
        std::cout << "  Widget: " << name_ << " = " << value_ << std::endl;
    }
};

void demo_modern_class() {
    std::cout << "=== 现代类特性 ===" << std::endl;
    
    ModernWidget w1;  // 使用默认值
    w1.print();
    
    ModernWidget w2(42, "answer");
    w2.print();
    
    // ModernWidget w3 = w2;  // 错误：拷贝被禁止
    ModernWidget w3 = std::move(w2);  // OK：移动允许
    w3.print();
    
    std::cout << std::endl;
}

// ============================================================
// 3. 继承与多态
// ============================================================

// 抽象基类
class Shape {
public:
    virtual ~Shape() = default;
    
    // 纯虚函数
    virtual double area() const = 0;
    virtual void draw() const = 0;
    
    // 普通虚函数
    virtual std::string type() const {
        return "Shape";
    }
};

class Circle : public Shape {
private:
    double radius_;

public:
    explicit Circle(double r) : radius_(r) {}
    
    double area() const override {
        return 3.14159265358979 * radius_ * radius_;
    }
    
    void draw() const override {
        std::cout << "  绘制圆形 (半径=" << radius_ << ")" << std::endl;
    }
    
    std::string type() const override {
        return "Circle";
    }
};

class Rectangle : public Shape {
private:
    double width_, height_;

public:
    Rectangle(double w, double h) : width_(w), height_(h) {}
    
    double area() const override {
        return width_ * height_;
    }
    
    void draw() const override {
        std::cout << "  绘制矩形 (" << width_ << " x " << height_ << ")" << std::endl;
    }
    
    std::string type() const override {
        return "Rectangle";
    }
};

void demo_inheritance() {
    std::cout << "=== 继承与多态 ===" << std::endl;
    
    // 使用智能指针和多态
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Rectangle>(4.0, 3.0));
    shapes.push_back(std::make_unique<Circle>(2.5));
    
    for (const auto& shape : shapes) {
        std::cout << "  类型: " << shape->type() << std::endl;
        shape->draw();
        std::cout << "  面积: " << shape->area() << std::endl;
        std::cout << std::endl;
    }
}

// ============================================================
// 4. 运算符重载
// ============================================================

class Complex {
private:
    double real_, imag_;

public:
    Complex(double r = 0, double i = 0) : real_(r), imag_(i) {}
    
    // 算术运算符
    Complex operator+(const Complex& other) const {
        return Complex(real_ + other.real_, imag_ + other.imag_);
    }
    
    Complex operator-(const Complex& other) const {
        return Complex(real_ - other.real_, imag_ - other.imag_);
    }
    
    Complex operator*(const Complex& other) const {
        return Complex(
            real_ * other.real_ - imag_ * other.imag_,
            real_ * other.imag_ + imag_ * other.real_
        );
    }
    
    // 复合赋值
    Complex& operator+=(const Complex& other) {
        real_ += other.real_;
        imag_ += other.imag_;
        return *this;
    }
    
    // 一元运算符
    Complex operator-() const {
        return Complex(-real_, -imag_);
    }
    
    // 比较运算符
    bool operator==(const Complex& other) const {
        return real_ == other.real_ && imag_ == other.imag_;
    }
    
    bool operator!=(const Complex& other) const {
        return !(*this == other);
    }
    
    // 模
    double magnitude() const {
        return std::sqrt(real_ * real_ + imag_ * imag_);
    }
    
    // 友元：输出流
    friend std::ostream& operator<<(std::ostream& os, const Complex& c) {
        os << c.real_;
        if (c.imag_ >= 0) os << "+";
        os << c.imag_ << "i";
        return os;
    }
};

void demo_operator_overloading() {
    std::cout << "=== 运算符重载 ===" << std::endl;
    
    Complex a(3, 4);
    Complex b(1, 2);
    
    std::cout << "  a = " << a << std::endl;
    std::cout << "  b = " << b << std::endl;
    std::cout << "  a + b = " << (a + b) << std::endl;
    std::cout << "  a - b = " << (a - b) << std::endl;
    std::cout << "  a * b = " << (a * b) << std::endl;
    std::cout << "  -a = " << (-a) << std::endl;
    std::cout << "  |a| = " << a.magnitude() << std::endl;
    std::cout << "  a == b: " << std::boolalpha << (a == b) << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 5. 静态成员
// ============================================================

class Counter {
private:
    static int count_;  // 静态成员变量
    int id_;

public:
    Counter() : id_(++count_) {
        std::cout << "  创建 Counter #" << id_ << std::endl;
    }
    
    ~Counter() {
        std::cout << "  销毁 Counter #" << id_ << std::endl;
        --count_;
    }
    
    // 静态成员函数
    static int get_count() { return count_; }
    
    int get_id() const { return id_; }
};

// 静态成员定义
int Counter::count_ = 0;

void demo_static_members() {
    std::cout << "=== 静态成员 ===" << std::endl;
    
    std::cout << "初始计数: " << Counter::get_count() << std::endl;
    
    {
        Counter c1;
        Counter c2;
        Counter c3;
        std::cout << "当前计数: " << Counter::get_count() << std::endl;
    }
    
    std::cout << "最终计数: " << Counter::get_count() << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 6. 链式调用（Builder 模式）
// ============================================================

class QueryBuilder {
private:
    std::string query_;

public:
    QueryBuilder& select(const std::string& columns) {
        query_ = "SELECT " + columns;
        return *this;
    }
    
    QueryBuilder& from(const std::string& table) {
        query_ += " FROM " + table;
        return *this;
    }
    
    QueryBuilder& where(const std::string& condition) {
        query_ += " WHERE " + condition;
        return *this;
    }
    
    QueryBuilder& order_by(const std::string& column) {
        query_ += " ORDER BY " + column;
        return *this;
    }
    
    std::string build() const {
        return query_ + ";";
    }
};

void demo_builder_pattern() {
    std::cout << "=== 链式调用 (Builder 模式) ===" << std::endl;
    
    QueryBuilder builder;
    std::string query = builder
        .select("name, age")
        .from("users")
        .where("age > 18")
        .order_by("name")
        .build();
    
    std::cout << "  生成的查询: " << query << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 7. explicit 关键字
// ============================================================

class ImplicitInt {
    int value_;
public:
    ImplicitInt(int v) : value_(v) {}  // 允许隐式转换
    int get() const { return value_; }
};

class ExplicitInt {
    int value_;
public:
    explicit ExplicitInt(int v) : value_(v) {}  // 禁止隐式转换
    int get() const { return value_; }
};

void take_implicit(ImplicitInt x) {
    std::cout << "  ImplicitInt: " << x.get() << std::endl;
}

void take_explicit(ExplicitInt x) {
    std::cout << "  ExplicitInt: " << x.get() << std::endl;
}

void demo_explicit() {
    std::cout << "=== explicit 关键字 ===" << std::endl;
    
    take_implicit(42);  // OK: 隐式转换
    // take_explicit(42);  // 错误: 需要显式转换
    take_explicit(ExplicitInt(42));  // OK: 显式构造
    
    ImplicitInt a = 100;   // OK: 隐式转换
    // ExplicitInt b = 100;  // 错误
    ExplicitInt b(100);    // OK
    ExplicitInt c{100};    // OK
    
    std::cout << "  a = " << a.get() << ", b = " << b.get() << std::endl;
    
    std::cout << std::endl;
}

// ============================================================
// 主函数
// ============================================================

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "       C++ 类与对象示例程序" << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << std::endl;
    
    demo_basic_class();
    demo_modern_class();
    demo_inheritance();
    demo_operator_overloading();
    demo_static_members();
    demo_builder_pattern();
    demo_explicit();
    
    std::cout << "========================================" << std::endl;
    std::cout << "            示例结束" << std::endl;
    std::cout << "========================================" << std::endl;
    
    return 0;
}

