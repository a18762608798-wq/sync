# 变分参数演化

SSH 模型基态拓扑 $Z_R$ 分类的数值实验。

## 模型

SSH 哈密顿量具有交替耦合结构：

$$
H = (1-s) \sum_{i\text{ odd}} (X_i X_{i+1} + \delta Z_i Z_{i+1}) + s \sum_{j\text{ even}} (X_j X_{j+1} + \delta Z_j Z_{j+1})
$$

反射算符 $Z_R$ 用于量化空间反演对称性：

$$
Z_R = \frac{\operatorname{tr}(\rho S)}{\sqrt{(\operatorname{tr}(\rho_1^2) + \operatorname{tr}(\rho_2^2))/2}}, \quad S = \bigotimes_{i=1}^{N/2} \mathrm{SWAP}_{i,\,N-i+1}
$$

## 流程

1. ~~数值相图绘制~~ ✅
2. 绝热演化模拟和对称性初态选择
3. 变分参数电路实验
