cmake_minimum_required(VERSION 3.10)
project(Parallel_Shared_Memory)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 1. 查找 OpenMP
find_package(OpenMP REQUIRED)

# 2. 查找 Threads (pthread on Linux)
find_package(Threads REQUIRED)

# 开启通用优化
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native)
endif()

# 目标 1: OpenMP 示例
add_executable(omp_demo omp_demo.cpp)
# 链接 OpenMP 库
target_link_libraries(omp_demo PRIVATE OpenMP::OpenMP_CXX)

# 目标 2: std::thread 示例
add_executable(thread_demo thread_demo.cpp)
target_link_libraries(thread_demo PRIVATE Threads::Threads)
