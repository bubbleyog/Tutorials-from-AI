#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <cstring>
#include <iomanip>

// 一个简单的矩阵类，用于演示 RAII 和移动语义
class Matrix {
public:
    // 构造函数
    Matrix(size_t rows, size_t cols) : rows_(rows), cols_(cols), data_(new double[rows * cols]) {
        // 初始化为 0 (或者其他值，这里为了性能演示仅分配)
        // std::fill(data_, data_ + rows * cols, 0.0); 
        // 实际上 new double[] 不会初始化，为了避免随机值影响（虽然这里只测内存操作），我们简单初始化一下
        // 但为了模拟“大计算量”或“大内存搬运”，我们主要关注构造和析构的开销
    }

    // 析构函数 (RAII: 资源在对象销毁时释放)
    ~Matrix() {
        if (data_) {
            delete[] data_;
        }
    }

    // 1. 拷贝构造函数 (Deep Copy)
    // 当我们执行 Matrix B = A; 时调用
    Matrix(const Matrix& other) : rows_(other.rows_), cols_(other.cols_), data_(new double[other.rows_ * other.cols_]) {
        std::copy(other.data_, other.data_ + rows_ * cols_, data_);
        // std::cout << "Copy Constructor called" << std::endl;
    }

    // 2. 拷贝赋值运算符
    // 当我们执行 B = A; (B已存在) 时调用
    Matrix& operator=(const Matrix& other) {
        if (this != &other) {
            delete[] data_; // 释放旧资源
            rows_ = other.rows_;
            cols_ = other.cols_;
            data_ = new double[rows_ * cols_]; // 分配新资源
            std::copy(other.data_, other.data_ + rows_ * cols_, data_); // 拷贝数据
        }
        // std::cout << "Copy Assignment called" << std::endl;
        return *this;
    }

    // 3. 移动构造函数 (Move Semantics)
    // 当我们执行 Matrix B = std::move(A); 或返回临时对象时调用
    // noexcept 很重要，它允许标准库容器（如 vector）在扩容时安全地使用移动构造
    Matrix(Matrix&& other) noexcept : rows_(other.rows_), cols_(other.cols_), data_(other.data_) {
        // “窃取”资源
        other.data_ = nullptr;
        other.rows_ = 0;
        other.cols_ = 0;
        // std::cout << "Move Constructor called" << std::endl;
    }

    // 4. 移动赋值运算符
    Matrix& operator=(Matrix&& other) noexcept {
        if (this != &other) {
            delete[] data_; // 释放自己的旧资源
            
            // 窃取资源
            data_ = other.data_;
            rows_ = other.rows_;
            cols_ = other.cols_;

            // 置空源对象
            other.data_ = nullptr;
            other.rows_ = 0;
            other.cols_ = 0;
        }
        // std::cout << "Move Assignment called" << std::endl;
        return *this;
    }

    size_t size() const { return rows_ * cols_; }

    // 用于阻止编译器优化掉某些操作
    double sum() const {
        double s = 0;
        for (size_t i = 0; i < rows_ * cols_; ++i) s += data_[i];
        return s;
    }

private:
    size_t rows_;
    size_t cols_;
    double* data_;
};

// 一个产生矩阵的工厂函数
Matrix createMatrix(size_t N) {
    Matrix m(N, N);
    // do some initialization...
    return m; // 在 C++11 之前这里可能触发拷贝，C++11 后会触发移动或 RVO (返回值优化)
}

int main() {
    const size_t N = 2000; // 2000x2000 矩阵，约 400万个 double，32MB 数据
    const int ITERATIONS = 100;

    std::cout << "Matrix size: " << N << "x" << N << " (" << (N*N*8)/(1024.0*1024.0) << " MB)" << std::endl;
    std::cout << "Iterations: " << ITERATIONS << std::endl;

    // 测试 1: 拷贝性能
    auto start_copy = std::chrono::high_resolution_clock::now();
    double dummy_sum_copy = 0;
    for (int i = 0; i < ITERATIONS; ++i) {
        Matrix A(N, N);
        Matrix B = A; // 触发拷贝构造
        dummy_sum_copy += B.sum(); 
    }
    auto end_copy = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff_copy = end_copy - start_copy;
    std::cout << "Copy Test Time: " << std::fixed << std::setprecision(4) << diff_copy.count() << " s" << std::endl;

    // 测试 2: 移动性能
    auto start_move = std::chrono::high_resolution_clock::now();
    double dummy_sum_move = 0;
    for (int i = 0; i < ITERATIONS; ++i) {
        Matrix A(N, N);
        Matrix B = std::move(A); // 触发移动构造
        dummy_sum_move += B.sum();
    }
    auto end_move = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff_move = end_move - start_move;
    std::cout << "Move Test Time: " << std::fixed << std::setprecision(4) << diff_move.count() << " s" << std::endl;

    std::cout << "Speedup (Copy / Move): " << diff_copy.count() / diff_move.count() << "x" << std::endl;

    // 测试 3: std::vector<Matrix> 的扩容
    // 这展示了为什么 noexcept 对移动构造很重要
    std::cout << "\nTesting std::vector<Matrix> resize performance..." << std::endl;
    
    std::vector<Matrix> vec_copy;
    // 预留空间可以避免重分配，但为了演示性能差异，我们故意不预留
    // vec_copy.reserve(100); 

    auto start_vec = std::chrono::high_resolution_clock::now();
    for(int i=0; i<50; ++i) {
        vec_copy.push_back(Matrix(N, N)); // 这里虽然 push_back 临时对象会移动，但 vector 扩容时会移动旧元素
    }
    auto end_vec = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff_vec = end_vec - start_vec;
    std::cout << "Vector Push Back Time: " << diff_vec.count() << " s" << std::endl;

    return 0;
}
