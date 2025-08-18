import matplotlib.pyplot as plt
import numpy as np

period = 43
total_frames = 1500
window = 4  # 每4帧结算一次
window2 = 3

dt_acc = 0.0
tick_frames = []
for frame in range(total_frames):
    dt_acc += 1
    # 只在每4帧时判定一次
    if frame % window == 0 :
        # 可能dt_acc已经跨过多个周期
        while dt_acc >= period:
            tick_frames.append(frame)
            dt_acc -= period
            epsilon = dt_acc
            window
            

tick_intervals = np.diff(tick_frames)

plt.figure(figsize=(10,4))
plt.plot(tick_intervals, marker='o', label='Tick Interval')
plt.axhline(period, color='r', linestyle='--', label='Theory Period')
plt.title(f'Batch Tick Simulation (period={period}, window={window})')
plt.xlabel('Tick Index')
plt.ylabel('Interval (frames)')
plt.legend()
plt.grid(True)
plt.show()

print("Tick间隔样本:", tick_intervals[:20])
print("最小间隔:", tick_intervals.min(), "最大间隔:", tick_intervals.max())
print("理论周期:", period)
