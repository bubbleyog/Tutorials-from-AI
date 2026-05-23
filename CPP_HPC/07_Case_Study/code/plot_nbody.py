import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import sys
import os

# 使用方法: python plot_nbody.py <csv_file>

if len(sys.argv) < 2:
    print("Usage: python plot_nbody.py <csv_file>")
    sys.exit(1)

filename = sys.argv[1]
if not os.path.exists(filename):
    print(f"Error: {filename} not found.")
    sys.exit(1)

# 读取数据
# 格式: step, id, x, y, z, mass
try:
    df = pd.read_csv(filename, header=None, names=['step', 'id', 'x', 'y', 'z', 'mass'])
except Exception as e:
    print(f"Error reading CSV: {e}")
    sys.exit(1)

# 获取唯一的步数
steps = df['step'].unique()
print(f"Found {len(steps)} steps in the data.")

# 只绘制第一步和最后一步的对比
fig = plt.figure(figsize=(12, 5))

# Plot Start
ax1 = fig.add_subplot(121, projection='3d')
step_start = steps[0]
data_start = df[df['step'] == step_start]
ax1.scatter(data_start['x'], data_start['y'], data_start['z'], s=1, c='blue', alpha=0.5)
ax1.set_title(f"Step {step_start}")

# Plot End
ax2 = fig.add_subplot(122, projection='3d')
step_end = steps[-1]
data_end = df[df['step'] == step_end]
ax2.scatter(data_end['x'], data_end['y'], data_end['z'], s=1, c='red', alpha=0.5)
ax2.set_title(f"Step {step_end}")

plt.tight_layout()
plt.show()
