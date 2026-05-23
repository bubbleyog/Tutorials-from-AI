#include "nbody_core.hpp"
#include <random>
#include <fstream>
#include <cmath>
#include <iostream>

namespace nbody {

void init_particles(std::vector<Particle>& particles, int n, double size) {
    particles.resize(n);
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> pos_dist(-size, size);
    std::uniform_real_distribution<> mass_dist(1.0, 10.0);

    for (int i = 0; i < n; ++i) {
        particles[i].x = pos_dist(gen);
        particles[i].y = pos_dist(gen);
        particles[i].z = pos_dist(gen);
        particles[i].vx = 0.0;
        particles[i].vy = 0.0;
        particles[i].vz = 0.0;
        particles[i].mass = mass_dist(gen);
    }
}

void save_particles(const std::vector<Particle>& particles, int step, const std::string& filename) {
    std::ofstream file(filename, std::ios::app); // Append mode
    if (!file.is_open()) return;

    // Format: step, id, x, y, z, mass
    for (size_t i = 0; i < particles.size(); ++i) {
        file << step << "," << i << ","
             << particles[i].x << "," << particles[i].y << "," << particles[i].z << ","
             << particles[i].mass << "\n";
    }
}

// 这是一个极其耗时的函数，也是我们并行化的重点
// 复杂度 O(N^2)
void compute_forces_and_update(std::vector<Particle>& particles, const SimulationParams& params) {
    size_t n = particles.size();
    
    // 存储这一步的加速度，避免直接修改速度影响后续计算
    // 更好的做法是直接累加力，然后统一更新
    struct Accel { double ax, ay, az; };
    std::vector<Accel> accelerations(n, {0.0, 0.0, 0.0});

    // 计算两两之间的引力
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            if (i == j) continue;

            double dx = particles[j].x - particles[i].x;
            double dy = particles[j].y - particles[i].y;
            double dz = particles[j].z - particles[i].z;

            // 添加一个软化因子 (softening factor) 避免距离为 0 时除以 0
            double dist_sq = dx*dx + dy*dy + dz*dz + 1e-9; 
            double dist = std::sqrt(dist_sq);
            double f = (params.G * particles[j].mass) / dist_sq; // F/m_i = G * m_j / r^2

            // a = F/m
            // 投影到 x, y, z 分量: ax = a * (dx/dist) = G * m_j * dx / r^3
            double a_common = f / dist;
            accelerations[i].ax += a_common * dx;
            accelerations[i].ay += a_common * dy;
            accelerations[i].az += a_common * dz;
        }
    }

    // 更新位置和速度 (Euler integration)
    for (size_t i = 0; i < n; ++i) {
        particles[i].vx += accelerations[i].ax * params.dt;
        particles[i].vy += accelerations[i].ay * params.dt;
        particles[i].vz += accelerations[i].az * params.dt;

        particles[i].x += particles[i].vx * params.dt;
        particles[i].y += particles[i].vy * params.dt;
        particles[i].z += particles[i].vz * params.dt;
    }
}

} // namespace nbody
