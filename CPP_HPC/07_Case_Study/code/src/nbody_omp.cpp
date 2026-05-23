#include "nbody_core.hpp"
#include <iostream>
#include <chrono>
#include <omp.h>
#include <cmath>

// OpenMP 优化版本的力计算
// 注意：这里我们重写了 compute_forces_and_update 以便插入 OpenMP 指令
void compute_forces_omp(std::vector<nbody::Particle>& particles, const nbody::SimulationParams& params) {
    size_t n = particles.size();
    
    // 临时存储加速度，避免竞争条件
    // 使用 SOA 风格存储加速度可能更好，但为了简单，我们用 vector<Accel>
    struct Accel { double ax, ay, az; };
    std::vector<Accel> accelerations(n);

    // 1. 并行计算加速度
    // schedule(dynamic) 有助于负载均衡，因为不同粒子可能的计算开销略有不同（尽管这里是对称的）
    // 但对于 N-Body O(N^2) 来说，static 往往足够且开销更小
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < n; ++i) {
        double ax = 0, ay = 0, az = 0;
        double xi = particles[i].x;
        double yi = particles[i].y;
        double zi = particles[i].z;

        // 这里可以进一步优化：利用牛顿第三定律 F_ij = -F_ji，减少一半计算量
        // 但这会引入写冲突，需要复杂的锁或原子操作，通常得不偿失
        // 除非使用分块算法
        for (size_t j = 0; j < n; ++j) {
            if (i == j) continue;

            double dx = particles[j].x - xi;
            double dy = particles[j].y - yi;
            double dz = particles[j].z - zi;

            double dist_sq = dx*dx + dy*dy + dz*dz + 1e-9;
            double dist = std::sqrt(dist_sq);
            double f_over_dist = (params.G * particles[j].mass) / (dist_sq * dist);

            ax += f_over_dist * dx;
            ay += f_over_dist * dy;
            az += f_over_dist * dz;
        }
        accelerations[i] = {ax, ay, az};
    }

    // 2. 并行更新位置和速度
    #pragma omp parallel for schedule(static)
    for (size_t i = 0; i < n; ++i) {
        particles[i].vx += accelerations[i].ax * params.dt;
        particles[i].vy += accelerations[i].ay * params.dt;
        particles[i].vz += accelerations[i].az * params.dt;

        particles[i].x += particles[i].vx * params.dt;
        particles[i].y += particles[i].vy * params.dt;
        particles[i].z += particles[i].vz * params.dt;
    }
}

int main(int argc, char** argv) {
    nbody::SimulationParams params;
    params.num_particles = 2000; // 2000个粒子，O(N^2) = 4,000,000 次相互作用
    params.num_steps = 100;
    params.dt = 0.01;
    params.G = 1.0;

    // 允许通过命令行参数覆盖粒子数
    if (argc > 1) params.num_particles = std::stoi(argv[1]);

    std::vector<nbody::Particle> particles;
    nbody::init_particles(particles, params.num_particles, 100.0);

    std::cout << "N-Body Simulation (OpenMP)" << std::endl;
    std::cout << "Particles: " << params.num_particles << std::endl;
    std::cout << "Steps: " << params.num_steps << std::endl;
    std::cout << "Max Threads: " << omp_get_max_threads() << std::endl;

    auto start = std::chrono::high_resolution_clock::now();

    for (int step = 0; step < params.num_steps; ++step) {
        compute_forces_omp(particles, params);
        // if (step % 10 == 0) std::cout << "Step " << step << " done." << std::endl;
    }

    auto end = std::chrono::high_resolution_clock::now();
    double duration = std::chrono::duration<double>(end - start).count();

    std::cout << "Total Time: " << duration << " s" << std::endl;
    // 计算每秒相互作用次数 (Interactions Per Second)
    double interactions = (double)params.num_particles * params.num_particles * params.num_steps;
    std::cout << "Performance: " << (interactions / duration) / 1e6 << " MOp/s" << std::endl;

    return 0;
}
