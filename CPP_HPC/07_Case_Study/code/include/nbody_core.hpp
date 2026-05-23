#pragma once
#include <vector>
#include <string>

namespace nbody {

// 使用 AOS (Array of Structures) 结构，虽然 SOA (Structure of Arrays) 可能对 SIMD 更友好
// 但 AOS 更直观，且对于简单的 N-Body 来说足够
struct Particle {
    double x, y, z;    // 位置
    double vx, vy, vz; // 速度
    double mass;       // 质量
};

// 模拟参数
struct SimulationParams {
    int num_particles; // 粒子总数
    int num_steps;     // 模拟步数
    double dt;         // 时间步长
    double G;          // 引力常数
};

// 随机初始化粒子
void init_particles(std::vector<Particle>& particles, int n, double size);

// 保存粒子状态到 CSV 文件（用于可视化）
void save_particles(const std::vector<Particle>& particles, int step, const std::string& filename);

// 计算两个粒子之间的引力相互作用
// 这是一个 O(N^2) 的算法核心
void compute_forces_and_update(std::vector<Particle>& particles, const SimulationParams& params);

} // namespace nbody
