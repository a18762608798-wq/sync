# Fitting

- **`pcov`**（parameter covariance）：参数的协方差矩阵，形状 `(3, 3)`。
  - 对角线元素是各参数的**方差**，取平方根就是标准误，可据此估计参数的不确定度；
  - 非对角元素反映参数间的相关性。

```python
import numpy as np
from scipy.optimize import curve_fit

# 定义多变量拟合函数
def func(X, a, b, c):
    x1, x2 = X # 也可以写成一元, 不必非用list
    return a * x1 + b * x2 + c

# 生成数据
x1 = np.linspace(0, 1, 10)
x2 = np.linspace(0, 2, 10)
X = [x1, x2]
y = func(X, 1, 2, 3) + 0.1 * np.random.normal(size=x1.size)

# 使用 curve_fit 进行拟合
popt, pcov = curve_fit(func, X, y)

print("Optimal parameters:", popt)
```
