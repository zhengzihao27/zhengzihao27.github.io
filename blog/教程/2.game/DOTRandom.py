import numpy as np
import matplotlib.pyplot as plt

# --------- 输入数据 ---------
# 所有会刷新DOT的帧（无我无剑）
refresh_times = [
21,43,65,86,129,150,172,215,258,279,300,343,364,385,406,428,516,558,579,600,622,
643,664,707,749,814,857,880,901,922,964,985,1007,1049,1134,1156,1178,1199,1220,
1241,1306,1348,1369,1390,1411,1432,1454,1519,1562,1584,1605,1626,1647,1669,1690,
1753,1817,1859,1882,1903,1925,1967,1989,2010,2052,2138,2181,2202,2224,2246,2268,
2334,2377,2398,2419,2441,2462,2483,2547,2590,2611,2632,2653,2674,2695,2758,2824,
2867,2890,2911,2933,2975,2996,3018,3146,3168,3189,3210,3231,3252,3274,3339,3382,
3403,3424,3445,3466,3487,3552,3594,3616,3638,3660,3681,3702,3723,3787,3852,3894,
3917,3938,3960,4002,4023,4044,4175,4196,4217,4238,4259,4281,4302,4408,4429,4450,
4471,4492,4513,4576,4642,4684,4727,4748,4769,4790,4833,4855,4876,4897
]

# 真实DOT tick帧（用于对比）
dot_real = [
66,109,154,197,237,281,325,369,410,453,498,541,582,625,669,713,753,797,841,885,
926,969,1014,1058,1097,1142,1185,1229,1270,1314,1358,1401,1441,1485,1530,1574,1614,
1657,1701,1746,1786,1830,1874,1917,1957,2001,2045,2090,2129,2173,2218,2262,2301,
2345,2390,2433,2474,2517,2561,2606,2646,2690,2733,2778,2818,2862,2906,2949,2989,
3033,3078,3121,3161,3205,3249,3294,3333,3377,3421,3465,3505,3550,3593,3637,3677,
3722,3765,3810,3850,3893,3937,3981,4021,4065,4109,4154,4194,4238,4281,4326,4366,
4409,4454,4497,4537,4581,4625,4669,4709,4753,4798,4841,4881,4925,4970
]

# --------- 参数 ---------
P = 43
TICKS_TOTAL = 8
scan_pattern = [4,4,4,4]    # 可调，多放几个3更容易出39
reset_countdown_on_refresh = False
refill_ticks_on_refresh    = True

# --------- 模拟函数 ---------
def simulate(period, ticks_total, start_frame, refresh_list, pattern):
    refresh_list = sorted(refresh_list)
    refresh_idx  = 0
    countdown    = period
    ticks_left   = ticks_total
    frame        = start_frame
    tick_frames  = []
    pat_i        = 0

    def do_scan(step, now):
        nonlocal countdown, ticks_left, tick_frames
        if ticks_left <= 0: 
            return
        countdown -= step
        while countdown <= 0 and ticks_left > 0:
            tick_frames.append(now)
            ticks_left -= 1
            countdown += period

    while len(tick_frames) < len(dot_real):  # 模拟同样多的tick
        step = pattern[pat_i % len(pattern)]
        pat_i += 1
        prev = frame
        frame += step

        # —— 处理区间内的刷新 —— 
        # 找所有 prev < r <= frame 的刷新帧
        while refresh_idx < len(refresh_list) and refresh_list[refresh_idx] <= frame:
            r = refresh_list[refresh_idx]
            if r > prev:  # 在本区间内
                # 先推进到 r
                do_scan(r - prev, r)
                prev = r
                # 刷新：补发已到的tick后，再补满/重置
                if refill_ticks_on_refresh:
                    ticks_left = ticks_total
                if reset_countdown_on_refresh:
                    countdown = period
            refresh_idx += 1

        # 区间剩余再推进到 frame
        do_scan(frame - prev, frame)

        # 如果当前DOT耗尽，可以直接重新开始也行（看你逻辑）
        if ticks_left <= 0 and refresh_idx < len(refresh_list):
            # 等下一次刷新重开
            pass

    return np.array(tick_frames)



# --------- 运行 ---------
ticks_sim = simulate(P, TICKS_TOTAL, start_frame=min(dot_real)-1,
                     refresh_list=refresh_times,
                     pattern=scan_pattern)

# --------- 对比 ---------
real_iv = np.diff(dot_real)
sim_iv  = np.diff(ticks_sim[:len(dot_real)])

shift = 1
x_real = np.arange(len(real_iv))
x_sim  = np.arange(len(sim_iv)) + shift   # 整体右移

plt.figure(figsize=(12,4))
plt.plot(x_real, real_iv, 'o-', label='Real')
plt.plot(x_sim,  sim_iv,  'x--', label=f'Sim')
plt.axhline(P, ls='--', c='r', alpha=0.4)
plt.xlabel('tick index'); plt.ylabel('interval')
plt.title('DOT interval')
plt.legend(); plt.grid(True); plt.show()
