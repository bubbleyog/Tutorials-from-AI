cmake_minimum_required(VERSION 3.10)
project(NBody_Simulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 开启优化
if(MSVC)
    add_compile_options(/O2)
else()
    add_compile_options(-O3 -march=native -ffast-math)
endif()

# 查找依赖
find_package(OpenMP REQUIRED)
find_package(MPI) # MPI 是可选的，如果没找到就不编译 MPI 版本

include_directories(include)

# 1. 核心库 (包含数据结构和初始化逻辑)
add_library(nbody_core src/nbody_core.cpp)

# 2. OpenMP 版本
add_executable(nbody_omp src/nbody_omp.cpp)
target_link_libraries(nbody_omp PRIVATE nbody_core OpenMP::OpenMP_CXX)

# 3. MPI 版本 (如果存在 MPI)
if(MPI_FOUND)
    add_executable(nbody_mpi src/nbody_mpi.cpp)
    target_link_libraries(nbody_mpi PRIVATE nbody_core MPI::MPI_CXX)
else()
    message(WARNING "MPI not found. Skipping nbody_mpi build.")
endif()
