import collections
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def pmf_convolve(f, d0, d1, p, f_next):
    for s, f in f.items():
        f_next[s + d0] += f * (1 - p)
        f_next[s + d1] += f * p
    return f_next


# 技能伤害数据
skill1 = [
    (163558, 278080),
    (59723, 101540),
    (42957, 73035),
    (170292, 289529),
    (73207, 124466),
    (73207, 124466),
    (67824, 115314),
    (182707, 310637),
    (67824, 115314),
    (73207, 124466),
    (67824, 115314),
    (67824, 115314),
    (417604, 710008),
    (73207, 124466),
    (317934, 540549),
    (192014, 326461),
    (122462, 208141),
    (73207, 124466),
]



skill2 = [
    (170490, 289866),
    (62255, 105845),
    (44778, 76131),
    (177509, 301799),
    (76310, 129741),
    (76310, 129741),
    (70699, 120202),
    (190451, 323803),
    (70699, 120202),
    (76310, 129741),
    (70699, 120202),
    (70699, 120202),
    (435305, 740103),
    (76310, 129741),
    (331409, 563460),
    (200153, 340299),
    (127615, 216970),
    (76310, 129741),
]

p1 = 0.342
p2 = 0.2743

p = p2
skills = skill2

HP = 2287216

#print(sum(a for a, b in skills))

# 累计伤害分布
f = collections.Counter()
f[0] = 1.0

pmf_history = []

first_kill_probs = []
cumulative_kill_probs = []

for i, (d0, d1) in enumerate(skills):
    f_next = collections.Counter()
    pmf_convolve(f, d0, d1, p, f_next)
    # 计算首次击杀概率
    kill_prob = 0
    for s, prob in f.items():
        if s < HP:
            # 不会心
            if s + d0 >= HP:
                kill_prob += prob * (1 - p)
            # 会心
            if s + d1 >= HP:
                kill_prob += prob * p
    first_kill_probs.append(kill_prob)
    if i == 0:
        cumulative_kill_probs.append(kill_prob)
    else:
        cumulative_kill_probs.append(cumulative_kill_probs[-1] + kill_prob)
    f = f_next
    pmf_history.append(f.copy())

exp_tau=0
# 输出每步概率
print("\nprob of n to kill：")
for idx, prob in enumerate(first_kill_probs):
    print(f"prob of {idx+1} to kill: {prob:.4%}")
    exp_tau+=(idx+1)*prob
    print(exp_tau)

print("\ncumulative n to kill：")
for idx, prob in enumerate(cumulative_kill_probs):
    print(f"第{idx+1}步累计击杀概率: {prob:.4%}")



print(f"\n总击杀概率: {cumulative_kill_probs[-1]:.4%}")

# 绘制概率分布图
plt.figure(figsize=(8,5))
plt.bar(range(1, len(first_kill_probs)+1), first_kill_probs, label='n-th skill can kill',color='orange')
plt.plot(range(1, len(cumulative_kill_probs)+1), cumulative_kill_probs, marker='o', label='probs of cumulative n to kill',color='red')
plt.xlabel('number of skill')
plt.ylabel('probs')
plt.title('The distribution of n to kill')
plt.legend()
plt.grid(True)

plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))

plt.show()




x_min, x_max, BIN_WIDTH = 500000, 3500000, 20000
x_bins = np.arange(x_min, x_max + BIN_WIDTH, BIN_WIDTH)
x_centers = 0.5 * (x_bins[:-1] + x_bins[1:])

plt.figure(figsize=(15, 6))
for i, pmf in enumerate(pmf_history):
    # 只画部分步数（比如每3步），太密会浑浊
    if i < 5 : continue
    if i % 3 == 0 or i == len(pmf_history) - 1:
        bin_probs = np.zeros(len(x_centers))
        for s, p in pmf.items():
            if x_min <= s < x_max:
                idx = int((s - x_min) // BIN_WIDTH)
                if 0 <= idx < len(bin_probs):
                    bin_probs[idx] += p
        # 透明度渐变，步数越大越深色
        color = plt.cm.viridis((len(pmf_history)-i)/(len(pmf_history)-1))
        plt.bar(x_centers, bin_probs, width=BIN_WIDTH*0.8, 
                alpha=0.18 + 0.6 * i/(len(pmf_history)-1), 
                color=color, 
                label=f'n={i+1}')


plt.axvline(HP, color='red', linestyle='--', lw=2, label='target HP')
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x/10000)}'))
plt.xlabel('cumulative damage')
plt.ylabel('prob')
plt.title('The distribution of n step cumulative damage')
plt.xlim(x_min, x_max)
plt.ylim(0, None)
plt.legend()
plt.tight_layout()
plt.show()
