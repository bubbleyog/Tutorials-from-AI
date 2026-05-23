#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
#include <iomanip>

// 矩阵大小 N x N
// N = 1024 时，矩阵约 8MB (double)，刚好放不下 L2 Cache，但能放下 L3 Cache (通常)
// 较大的 N 更能体现 Cache 优化的效果
const int N = 1024; 

using Matrix = std::vector<double>;

// 初始化矩阵
void init_matrix(Matrix& m) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0.0, 1.0);
    for(auto& val : m) val = dis(gen);
}

// 1. 朴素矩阵乘法 (Naive i-j-k)
// 这种实现对 Cache 极度不友好，特别是 B 矩阵的访问
void dgemm_naive(const Matrix& A, const Matrix& B, Matrix& C) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];
            }
            C[i * N + j] = sum;
        }
    }
}

// 2. 交换循环次序 (i-k-j)
// 这是一个极小的改动，但能带来巨大的提升
// 此时内层循环是对 C[i][j] 和 B[k][j] 的连续访问，符合空间局部性
void dgemm_ikj(const Matrix& A, const Matrix& B, Matrix& C) {
    // 确保 C 初始化为 0
    std::fill(C.begin(), C.end(), 0.0);
    
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            double r = A[i * N + k];
            // 编译器更容易对这个内层循环进行自动向量化 (Auto-Vectorization)
            for (int j = 0; j < N; ++j) {
                C[i * N + j] += r * B[k * N + j];
            }
        }
    }
}

// 3. 循环分块 (Tiling / Blocking)
// 将大矩阵切分成小块，使其能放入 L1/L2 Cache
// 这里展示最简单的 Blocked i-j-k
void dgemm_tiled(const Matrix& A, const Matrix& B, Matrix& C, int blockSize) {
    std::fill(C.begin(), C.end(), 0.0);
    
    for (int ii = 0; ii < N; ii += blockSize) {
        for (int jj = 0; jj < N; jj += blockSize) {
            for (int kk = 0; kk < N; kk += blockSize) {
                
                // 处理当前 Block
                // 使用 i-k-j 顺序处理 block 内部
                int imax = std::min(ii + blockSize, N);
                int jmax = std::min(jj + blockSize, N);
                int kmax = std::min(kk + blockSize, N);

                for (int i = ii; i < imax; ++i) {
                    for (int k = kk; k < kmax; ++k) {
                        double r = A[i * N + k];
                        for (int j = jj; j < jmax; ++j) {
                            C[i * N + j] += r * B[k * N + j];
                        }
                    }
                }
            }
        }
    }
}

int main() {
    Matrix A(N * N), B(N * N), C(N * N);
    init_matrix(A);
    init_matrix(B);

    std::cout << "Matrix size: " << N << "x" << N << std::endl;

    // Test Naive
    auto start = std::chrono::high_resolution_clock::now();
    dgemm_naive(A, B, C);
    auto end = std::chrono::high_resolution_clock::now();
    double time_naive = std::chrono::duration<double>(end - start).count();
    std::cout << "Naive (i-j-k): " << time_naive << " s" << std::endl;

    // Test IKJ
    start = std::chrono::high_resolution_clock::now();
    dgemm_ikj(A, B, C);
    end = std::chrono::high_resolution_clock::now();
    double time_ikj = std::chrono::duration<double>(end - start).count();
    std::cout << "Optimized (i-k-j): " << time_ikj << " s (Speedup: " << time_naive/time_ikj << "x)" << std::endl;

    // Test Tiled
    // 块大小的选择通常取决于 L1/L2 Cache 大小。32 或 64 是常见选择。
    int blockSize = 64; 
    start = std::chrono::high_resolution_clock::now();
    dgemm_tiled(A, B, C, blockSize);
    end = std::chrono::high_resolution_clock::now();
    double time_tiled = std::chrono::duration<double>(end - start).count();
    std::cout << "Tiled (Block=" << blockSize << "): " << time_tiled << " s (Speedup vs Naive: " << time_naive/time_tiled << "x)" << std::endl;

    return 0;
}
