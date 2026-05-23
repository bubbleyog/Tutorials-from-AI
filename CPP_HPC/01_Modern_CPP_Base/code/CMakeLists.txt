cmake_minimum_required(VERSION 3.10)
project(ModernCPP_HPC_Base)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 开启优化选项
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native)
endif()

add_executable(matrix_performance matrix_performance.cpp)
