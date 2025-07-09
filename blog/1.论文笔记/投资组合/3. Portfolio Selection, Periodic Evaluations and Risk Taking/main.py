import numpy as np
import matplotlib.pyplot as plt

# 参数设置（来自 Tversky and Kahneman 1992 的典型估计）
alpha = 0.88  # 风险敏感度
k = 2.25      # 损失厌恶因子

# 构造 x 值：从负值到正值（表示收益或损失）
x = np.linspace(-1, 1, 400)

# 定义效用函数
def U(x):
    u = np.zeros_like(x)
    u[x >= 0] = x[x >= 0]**alpha
    u[x < 0] = -k * np.abs(x[x < 0])**alpha
    return u

# 计算效用值
u = U(x)

# 作图
plt.figure(figsize=(8, 5))
plt.plot(x, u, label=f"$U(x)$, α={alpha}, k={k}", color='blue')
plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')
plt.axvline(0, color='gray', linewidth=0.5, linestyle='--')
plt.title("S-shaped Utility Function (Prospect Theory)")
plt.xlabel("Gain / Loss $x$")
plt.ylabel("Utility $U(x)$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
