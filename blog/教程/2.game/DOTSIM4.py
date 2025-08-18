import numpy as np
import matplotlib.pyplot as plt

# --------- 真实数据 ---------
dot_real = np.array([
    63, 103, 147, 187, 227, 267, 312, 351, 392, 432, 475, 515, 555, 595, 639, 680, 719, 759,
    803, 844, 883, 923, 968, 1008, 1047, 1087, 1131, 1171, 1211, 1251, 1295, 1335, 1375, 1415,
    1459, 1499, 1539, 1580, 1623, 1664, 1703, 1744, 1788, 1828, 1867, 1907, 1951, 1991, 2032,
    2072, 2115, 2155, 2195, 2236, 2279, 2319, 2359, 2399, 2443, 2483, 2523, 2563, 2607, 2648,
    2687, 2727, 2771, 2812, 2852, 2891, 2936, 2975, 3015, 3055, 3099, 3139, 3179, 3219, 3263,
    3303, 3343, 3383, 3428, 3467, 3507, 3547, 3591, 3632, 3671, 3711, 3755, 3796, 3835, 3876,
    3919, 3959, 3999, 4039, 4083, 4123, 4163, 4204, 4248, 4287, 4327, 4368, 4411, 4451, 4492,
    4531, 4575, 4615, 4655, 4695, 4739, 4779, 4819, 4859, 4904
])
real_iv = np.diff(dot_real)

# --------- 模拟参数 ---------
period = 41
step   = 4            # 每4帧检查一次
total_frames = max(dot_real)+period  # 大一点，保证 tick 足够多

def batch_sim(period, step, total_frames):
    """每 step 帧检查一次，把这 step 帧一起加进 dt_acc"""
    dt_acc = 0.0
    tick_frames = []
    frame = 0
    while len(tick_frames) < len(dot_real):
        prev = frame
        frame += step
        dt_acc += step

        while dt_acc >= period:
            tick_frames.append(frame)
            dt_acc -= period

    return np.array(tick_frames)

ticks_sim = batch_sim(period, step, total_frames)
sim_iv = np.diff(ticks_sim)

# --------- 对齐长度（用真实数据长度）---------
L = len(real_iv)
sim_iv = sim_iv[:L]

# --------- 画图比较 ---------
shift = -2  # 把模拟线整体右移一点，方便看
x_real = np.arange(L)
x_sim  = x_real + shift

plt.figure(figsize=(12,4))
plt.plot(x_real, real_iv, 'o-', label='Real')
plt.plot(x_sim,  sim_iv,  'x--', label='Sim')
plt.axhline(period, ls='--', c='r', alpha=0.4)
plt.xlabel('tick index'); plt.ylabel('interval')
plt.title(f'DOT (period={period}, step={step})')
plt.legend(); plt.grid(True); plt.show()

