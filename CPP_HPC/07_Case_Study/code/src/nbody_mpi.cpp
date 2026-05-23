#include "nbody_core.hpp"
#include <mpi.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <cstring>

// MPI 版本 N-Body
// 策略：Replicated Data (复制数据)
// 每个进程拥有所有粒子的位置副本 (因为计算力需要知道所有粒子的位置)
// 但每个进程只负责更新它自己那一小部分粒子的位置和速度

// 定义 MPI 数据类型以便传输 Particle 结构体
void create_mpi_particle_type(MPI_Datatype* mpi_particle_type) {
    // 结构体: x, y, z, vx, vy, vz, mass (全是 double)
    int blocklengths[1] = {7};
    MPI_Aint displacements[1] = {0};
    MPI_Datatype types[1] = {MPI_DOUBLE};
    MPI_Type_create_struct(1, blocklengths, displacements, types, mpi_particle_type);
    MPI_Type_commit(mpi_particle_type);
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // 创建自定义 MPI 类型
    MPI_Datatype mpi_particle_type;
    create_mpi_particle_type(&mpi_particle_type);

    nbody::SimulationParams params;
    params.num_particles = 2000;
    params.num_steps = 100;
    params.dt = 0.01;
    params.G = 1.0;

    // 1. 初始化
    // 所有进程都初始化相同的粒子（这里用固定种子，保证初始状态一致）
    // 或者只由 Rank 0 初始化然后广播
    std::vector<nbody::Particle> all_particles;
    nbody::init_particles(all_particles, params.num_particles, 100.0);

    // 2. 任务分配
    // 假设 num_particles 能被 size 整除
    int particles_per_proc = params.num_particles / size;
    int start_idx = rank * particles_per_proc;
    int end_idx = start_idx + particles_per_proc;

    // 本地负责的粒子
    // 注意：我们需要所有粒子的位置来计算力，但只需要更新本地粒子的速度和位置
    // 因此 all_particles 保存了所有粒子的信息

    if (rank == 0) {
        std::cout << "N-Body MPI Simulation" << std::endl;
        std::cout << "Particles: " << params.num_particles << std::endl;
        std::cout << "Processes: " << size << std::endl;
    }

    double start_time = MPI_Wtime();

    for (int step = 0; step < params.num_steps; ++step) {
        
        // --- 步骤 A: 计算本地负责粒子的新状态 ---
        // 只需要计算 [start_idx, end_idx) 范围内的粒子受到的力
        for (int i = start_idx; i < end_idx; ++i) {
            double ax = 0, ay = 0, az = 0;
            for (int j = 0; j < params.num_particles; ++j) {
                if (i == j) continue;
                
                double dx = all_particles[j].x - all_particles[i].x;
                double dy = all_particles[j].y - all_particles[i].y;
                double dz = all_particles[j].z - all_particles[i].z;
                
                double dist_sq = dx*dx + dy*dy + dz*dz + 1e-9;
                double dist = std::sqrt(dist_sq);
                double f = (params.G * all_particles[j].mass) / dist_sq;
                double a_common = f / dist;
                
                ax += a_common * dx;
                ay += a_common * dy;
                az += a_common * dz;
            }

            // 更新本地粒子的速度和位置
            all_particles[i].vx += ax * params.dt;
            all_particles[i].vy += ay * params.dt;
            all_particles[i].vz += az * params.dt;

            all_particles[i].x += all_particles[i].vx * params.dt;
            all_particles[i].y += all_particles[i].vy * params.dt;
            all_particles[i].z += all_particles[i].vz * params.dt;
        }

        // --- 步骤 B: 通信 (Allgather) ---
        // 每个进程都更新了自己那一部分粒子，现在需要把这些更新后的位置同步给所有人
        // 因为下一步计算力需要所有人的新位置
        
        // 注意：MPI_Allgather 需要发送缓冲区和接收缓冲区不同
        // 这里我们可以用 MPI_IN_PLACE (如果在 MPI-2 标准以上)，或者开辟临时 buffer
        // 为了简单和兼容性，我们直接对整个数组操作
        
        // 实际上，因为 all_particles 在各个进程中只有 [start_idx, end_idx) 是新的
        // 我们需要把这部分 gather 起来覆盖所有人的 all_particles
        
        // 为了避免复杂的指针操作，我们创建一个临时 buffer 存放本地更新后的粒子
        std::vector<nbody::Particle> local_updates(particles_per_proc);
        for(int i=0; i<particles_per_proc; ++i) {
            local_updates[i] = all_particles[start_idx + i];
        }

        MPI_Allgather(local_updates.data(), particles_per_proc, mpi_particle_type,
                      all_particles.data(), particles_per_proc, mpi_particle_type,
                      MPI_COMM_WORLD);
    }

    double end_time = MPI_Wtime();

    if (rank == 0) {
        std::cout << "Total Time: " << end_time - start_time << " s" << std::endl;
        double interactions = (double)params.num_particles * params.num_particles * params.num_steps;
        std::cout << "Performance: " << (interactions / (end_time - start_time)) / 1e6 << " MOp/s" << std::endl;
    }

    MPI_Type_free(&mpi_particle_type);
    MPI_Finalize();
    return 0;
}
