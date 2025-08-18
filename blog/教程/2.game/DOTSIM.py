import numpy as np
import matplotlib.pyplot as plt

# --------- 真实数据 ---------
dot_real = np.array([
    66,109,154,197,237,281,325,369,410,453,498,541,582,625,669,713,753,797,841,885,
    926,969,1014,1058,1097,1142,1185,1229,1270,1314,1358,1401,1441,1485,1530,1574,1614,
    1657,1701,1746,1786,1830,1874,1917,1957,2001,2045,2090,2129,2173,2218,2262,2301,
    2345,2390,2433,2474,2517,2561,2606,2646,2690,2733,2778,2818,2862,2906,2949,2989,
    3033,3078,3121,3161,3205,3249,3294,3333,3377,3421,3465,3505,3550,3593,3637,3677,
    3722,3765,3810,3850,3893,3937,3981,4021,4065,4109,4154,4194,4238,4281,4326,4366,
    4409,4454,4497,4537,4581,4625,4669,4709,4753,4798,4841,4881,4925,4970
])
real_iv = np.diff(dot_real)

# --------- 模拟参数 ---------
period = 43
step   = 4            # 每4帧检查一次
total_frames = max(dot_real)+4  # 大一点，保证 tick 足够多

def batch_sim(period, step, total_frames):
    """每 step 帧检查一次，把这 step 帧一起加进 dt_acc"""
    dt_acc = 0.0
    tick_frames = []
    frame = 0
    while frame < total_frames:
        prev = frame
        frame += step
        dt_acc += step

        # 可能跨多个周期
        while dt_acc >= period:
            # tick 的真实发生时间在这一批次末尾 frame
            #（如果你需要更精确，可用线性插值：frame - (dt_acc - period)）
            tick_frames.append(frame)
            dt_acc -= period

    return np.array(tick_frames)

ticks_sim = batch_sim(period, step, total_frames)
sim_iv = np.diff(ticks_sim)

# --------- 对齐长度（用真实数据长度）---------
L = len(real_iv)
sim_iv = sim_iv[:L]

# --------- 画图比较 ---------
shift = 1  # 把模拟线整体右移一点，方便看
x_real = np.arange(L)
x_sim  = x_real + shift

plt.figure(figsize=(12,4))
plt.plot(x_real, real_iv, 'o-', label='Real')
plt.plot(x_sim,  sim_iv,  'x--', label='Sim')
plt.axhline(period, ls='--', c='r', alpha=0.4)
plt.xlabel('tick index'); plt.ylabel('interval')
plt.title(f'DOT (period={period}, step={step})')
plt.legend(); plt.grid(True); plt.show()

