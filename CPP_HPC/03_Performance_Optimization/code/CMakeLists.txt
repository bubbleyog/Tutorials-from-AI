cmake_minimum_required(VERSION 3.10)
project(Performance_Optimization)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 默认开启多线程支持
find_package(Threads REQUIRED)

# 1. 矩阵乘法示例
# 我们创建两个版本，一个开启优化，一个不开启，以便对比编译器优化的威力

# 基础版本 (-O0)
add_executable(gemm_O0 matrix_multiply_opt.cpp)
if(MSVC)
    target_compile_options(gemm_O0 PRIVATE /Od)
else()
    target_compile_options(gemm_O0 PRIVATE -O0)
endif()

# 优化版本 (-O3 + Native Arch)
add_executable(gemm_O3 matrix_multiply_opt.cpp)
if(MSVC)
    target_compile_options(gemm_O3 PRIVATE /O2)
else()
    # -march=native 允许编译器使用当前 CPU 支持的所有指令集 (AVX2, AVX-512 等)
    # -ffast-math 允许激进的浮点优化（可能会改变精度，但在 GEMM 中通常可接受）
    target_compile_options(gemm_O3 PRIVATE -O3 -march=native -ffast-math)
endif()


# 2. False Sharing 示例
add_executable(false_sharing false_sharing.cpp)
target_link_libraries(false_sharing PRIVATE Threads::Threads)
# 开启优化以确保循环不会被意外优化掉，同时让内存访问模式更纯粹
if(NOT MSVC)
    target_compile_options(false_sharing PRIVATE -O3)
endif()
