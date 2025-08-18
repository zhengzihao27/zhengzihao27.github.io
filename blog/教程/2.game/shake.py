from scipy.interpolate import UnivariateSpline
import numpy as np
import matplotlib.pyplot as plt

data = [1,0,2,0,-3,1,1,1,-2,0,2,0,-2,0,1,1,-3,1,1,1,-2,0,2,1,-4,2,0,1,-2,1,1,0,-3,1,2,1,-3]
x = np.arange(1, len(data)+1)

spline = UnivariateSpline(x, data, s=8)
x_pred = np.linspace(1, len(data), 200)
y_pred = spline(x_pred)

mean_val = np.mean(data)

plt.figure(figsize=(10, 4))
plt.scatter(x, data, color='blue', s=25)
plt.plot(x_pred, y_pred, color='orange', linewidth=2, label='Offset')
plt.axhline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean = {mean_val:.2f}')
plt.xlabel('Frame')
plt.ylabel('Offset')
plt.title('Offset Swing Curve')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


data2 = [1,0,2,0,-3,1,1,1,-2,0,2,0,-2,0,1,1,-3,1,1,1,-2,0,2,1,-4,2,0,1,-2,1,1,0,
        -3,1,2,1,-3,0,1,2,-3,1,1,0,-3,1,1,2,-4,1,2,1,-4,1,2,0,-2,0,1,2,-3,1,0,2,
        -3,1,1,0,-3,1,2,0,-3,1,1,2,-4,1,1,1,-3,2,0,1,-3,2,0,2,-3,0,1,1,-3,1,1,2,
        -3,1,0,2,-3,0,2,0,-3,1,1,1,-3,1,2,0,-3,1,2]
x = np.arange(1, len(data2)+1)

spline = UnivariateSpline(x, data2, s=8)
x_pred = np.linspace(1, len(data2), 200)
y_pred = spline(x_pred)

mean_val = np.mean(data2)


plt.figure(figsize=(10,4))
plt.plot(x, data2, '-o', ms=4, label='Offset')       # 折线图
plt.axhline(mean_val, color='red', ls='--', lw=2,
            label=f'Mean = {mean_val:.2f}')

plt.xlabel('Frame')
plt.ylabel('Offset')
plt.title('Offset Swing Curve (Line)')
plt.legend()
plt.grid(True, ls='--', alpha=0.5)
plt.tight_layout()
plt.show()

