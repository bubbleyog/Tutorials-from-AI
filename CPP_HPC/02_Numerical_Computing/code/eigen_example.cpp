#include <iostream>
#include <Eigen/Dense>
#include <chrono>

// 使用 Eigen 进行基本的线性代数运算
// Eigen 是一个 header-only 的库，非常方便集成

void basic_operations() {
    std::cout << "\n=== Eigen Basic Operations ===" << std::endl;
    
    // 定义 3x3 矩阵，元素类型为 double
    Eigen::Matrix3d A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 10; // 注意：如果是 7,8,9 则行列式为0，不可逆
         
    std::cout << "Matrix A:\n" << A << std::endl;
    
    // 定义向量
    Eigen::Vector3d v(1, 2, 3);
    std::cout << "Vector v:\n" << v << std::endl;
    
    // 矩阵向量乘法
    Eigen::Vector3d y = A * v;
    std::cout << "A * v =\n" << y << std::endl;
    
    // 矩阵乘法
    Eigen::Matrix3d B = A * A.transpose();
    std::cout << "A * A^T =\n" << B << std::endl;
}

void solve_linear_system() {
    std::cout << "\n=== Solving Ax = b ===" << std::endl;
    
    const int N = 100;
    // 动态大小矩阵 MatrixXd
    Eigen::MatrixXd A = Eigen::MatrixXd::Random(N, N);
    Eigen::VectorXd b = Eigen::VectorXd::Random(N);
    
    // 确保 A 可逆，通常加一个单位矩阵或者使其对角占优
    A = A * A.transpose() + Eigen::MatrixXd::Identity(N, N); 
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // 1. 使用 LLT 分解 (Cholesky) 求解，适用于正定矩阵（最快）
    // A 已经是正定的了 (A*A^T + I)
    Eigen::VectorXd x1 = A.llt().solve(b);
    
    auto end_llt = std::chrono::high_resolution_clock::now();
    
    // 2. 使用 Householder QR 分解求解，适用于任意矩阵（较慢但稳定）
    Eigen::VectorXd x2 = A.colPivHouseholderQr().solve(b);
    
    auto end_qr = std::chrono::high_resolution_clock::now();
    
    // 3. 使用 LU 分解
    Eigen::VectorXd x3 = A.partialPivLu().solve(b);
    
    auto end_lu = std::chrono::high_resolution_clock::now();
    
    std::cout << "Problem size: " << N << "x" << N << std::endl;
    std::cout << "LLT Time: " << std::chrono::duration<double>(end_llt - start).count() << "s" << std::endl;
    std::cout << "QR Time:  " << std::chrono::duration<double>(end_qr - end_llt).count() << "s" << std::endl;
    std::cout << "LU Time:  " << std::chrono::duration<double>(end_lu - end_qr).count() << "s" << std::endl;
    
    // 验证解的准确性
    double error = (A * x1 - b).norm() / b.norm();
    std::cout << "Relative Error (LLT): " << error << std::endl;
}

int main() {
    basic_operations();
    solve_linear_system();
    return 0;
}
