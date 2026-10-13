# 推导与证明规范（Structured Mathematical Proof）

目标：数学、物理、算法推导共用一套关键词，做到逻辑清楚、可追溯、可穿插解释、不冗余。

核心公式：

$$
\text{Proof} = \text{Context} + \text{Goal} + \text{Derivation Blocks} + \text{Conclusion}
$$

$$
\text{Derivation Block} = \text{HAVE} + \text{Formula Chain} + \text{BY}
$$

解释层（`INTERPRET` / `NOTE` / `MOTIVATION` 等）附着在推导块周围，不自动成为证明依据。

---

## 1. 标准结构

### 1.1 Context — 建立上下文（可选/视问题而定）

```text
GIVEN:
    已知事实、初始条件

LET:
    引入变量或对象

DEFINE:
    定义函数、物理量或辅助对象

REQUIRE:
    必须满足的前置条件
```

### 1.2 Goal — 声明目标（核心）

```text
GOAL:
    需要证明的命题

MOTIVATION:
    为什么选择这种证明方法（可选）
```

### 1.3 Proof — 主体推导（可反复出现）

```text
SUFFICES:
    化归为更简单的命题（可选）

CLAIM:
    需要证明的中间结论（可选）

HAVE:
    已建立的结论
BY:
    推导依据

INTERPRET:
    解释含义（可选）

HAVE / BY:
    下一个结论（可重复）

NOTE:
    补充说明（可选）

THEREFORE:
    阶段性或最终结论
```

### 1.4 Verification — 检查与结束（视需要而定）

```text
CHECK:
    量纲、边界或特殊情况检查

QED

IMPLICATION:
    结果的进一步意义（可选）

CAVEAT:
    适用范围与局限（可选）
```

这只是组织模板，不是强制顺序。`CHECK` 可出现在推导中间，`INTERPRET` 可紧跟任意重要公式，`MOTIVATION` 也可出现在新的中间步骤之前。

---

## 2. 关键词使用频率

| 关键词 | 使用规律 | 典型位置 |
|---|---|---|
| `GIVEN`, `DEFINE`, `LET` | 通常集中出现，需要时可再次引入 | 开头或新子问题 |
| `GOAL` | 通常一次，子证明可再次出现 | 开始或子证明开始 |
| `CLAIM`, `SUFFICES` | 按证明结构使用 | 证明过程中 |
| `HAVE`, `BY` | 可高频重复 | 具体推导 |
| `THEREFORE` | 每个关键阶段使用 | 阶段性结论 |
| `INTERPRET`, `NOTE` | 任意重要步骤后穿插 | 解释层 |
| `CHECK`, `CAVEAT` | 按需出现 | 中途或结尾 |
| `CASE`, `ASSUME`, `WLOG` | 特定策略时使用 | 局部证明块 |
| `QED` | 每个完整证明结束时 | 结尾 |

理解方式：`HAVE` / `BY` 构成可重复的推导单元，semantic layer 插在推导单元之间。

---

## 3. 公式链规范（Derivation Chain）

### 3.1 不推荐：每一步都用独立关键词

```text
HAVE:
    A = B
BY:
    Rule 1

HAVE:
    B = C
BY:
    Rule 2
```

几十行推导时会极度啰嗦。

### 3.2 推荐：一个 `HAVE` 包含整条推导链

```text
HAVE:
    A
    = B        [BY Rule 1]
    = C        [BY Rule 2]
    = D        [BY Rule 3]
    = E        [BY Rule 4]
```

规定：行尾方括号内的 `[BY ...]` 只解释该行的变换。这是一种轻量注释语法，不意味着可被证明器验证。

### 3.3 数学例子

```text
GIVEN:
    n ∈ N, n ≥ 1

GOAL:
    sum_{k=1}^{n} (2k-1) = n^2

HAVE:
    sum(2k - 1)
    = 2 sum k - sum 1           [BY linearity]
    = 2·n(n+1)/2 - n            [BY sum formulas]
    = n(n+1) - n                [BY simplification]
    = n^2                       [BY algebra]

THEREFORE:
    sum_{k=1}^{n} (2k-1) = n^2

QED
```

排版对应：

$$
\begin{aligned}
\sum_{k=1}^{n}(2k-1) &= 2\sum_{k=1}^{n}k - \sum_{k=1}^{n}1 && \text{(linearity)} \\
&= 2\cdot\frac{n(n+1)}{2} - n && \text{(sum formulas)} \\
&= n(n+1) - n && \text{(simplification)} \\
&= n^2 && \text{(algebra)}
\end{aligned}
$$

---

## 4. 长推导分块

按数学目的分块，不按公式数量分块。

- 同一种操作连续进行：保持在同一条公式链中。
- 出现新的数学思路：开始新的 `HAVE` 块。
- 得到可独立引用的结果：用 `HAVE` 或 `THEREFORE`，必要时编号 `(1)`、`（2)`。
- 需解释为什么选某种变换：插 `MOTIVATION`。
- 需解释结果意义：插 `INTERPRET`。

编号示例：

```text
HAVE:
    A = B = C              (1)

HAVE:
    D = E = F              (2)

THEREFORE:
    A = F
BY:
    (1), (2), and Rule 3.
```

编号的意义是引用前面结果而不重写公式。最后一步只有在 `(1)`、`(2)` 和 `Rule 3` 确实能推出结论时才成立。

---

## 5. 完整示例：带线性阻尼的弹簧振子

目标：证明机械能不随时间增加。运动方程为：

$$
m x''(t) + b x'(t) + k x(t) = 0
$$

```text
GIVEN:
    m > 0, b ≥ 0, k > 0, x ∈ C^2(I)
    FORALL t ∈ I:
        m x''(t) + b x'(t) + k x(t) = 0.    (1)

DEFINE:
    E(t) := (1/2)m[x'(t)]^2 + (1/2)k[x(t)]^2

INTERPRET PHYSICALLY:
    第一项为动能，第二项为弹性势能。

GOAL:
    FORALL t ∈ I: E'(t) ≤ 0

MOTIVATION:
    对总机械能求导，再用运动方程消去二阶导数。

HAVE:
    E'(t)
    = m x'(t)x''(t) + k x(t)x'(t)   [BY differentiation]
    = x'(t)[m x''(t) + k x(t)]      [BY factoring]
    = x'(t)[-b x'(t)]               [BY equation (1)]
    = -b[x'(t)]^2                   [BY algebra]       (2)

INTERPRET PHYSICALLY:
    机械能流失速率由阻尼系数和速度平方决定。

HAVE:
    b[x'(t)]^2 ≥ 0
BY:
    b ≥ 0 and [x'(t)]^2 ≥ 0.

THEREFORE:
    E'(t) = -b[x'(t)]^2 ≤ 0
BY:
    equation (2).

CHECK DIMENSIONALLY:
    [E'] = M L^2 T^-3
    [b(x')^2] = M L^2 T^-3

THEREFORE:
    E(t) is non-increasing on I.
BY:
    derivative criterion for monotonicity.

QED

IMPLICATION:
    b > 0 时，只要速度非零，阻尼就耗散机械能。

CAVEAT:
    假设 m, b, k 为常数，且为线性粘性阻尼。
```

三点说明：

1. 推导中穿插解释：先得中间结论，`INTERPRET` 后再继续。
2. 连续公式链不重复 `HAVE`：只要推导连续，一个 `HAVE` 足够。
3. 检查不等于证明：`CHECK DIMENSIONALLY` 是合理性检查，不能替代动力学方程和微分计算。

能量导数链的排版对应：

$$
\begin{aligned}
E'(t) &= m x'(t) x''(t) + k x(t) x'(t) && \text{(differentiation)} \\
&= x'(t)[m x''(t) + k x(t)] && \text{(factoring)} \\
&= x'(t)[-b x'(t)] && \text{(equation (1))} \\
&= -b[x'(t)]^2 && \text{(algebra)}
\end{aligned}
$$

---

## 6. 六条硬规则

| 规则 | 内容 |
|---|---|
| 1. 一个 `HAVE` 可含多行公式 | 不必每个等号都引入新关键词 |
| 2. 每个非显然变换必须有依据 | 优先行尾 `[BY ...]`，也可对整块统一说明 |
| 3. 重要中间结果单独成块 | 必要时编号 `(1)`、`（2)` |
| 4. 解释层可自由穿插 | 但 `INTERPRET` / `NOTE` 不自动成为证明依据 |
| 5. 局部假设必须有明确作用域 | `ASSUME` 下的结论不自动成为无条件结论 |
| 6. `QED` 只在目标完成后使用 | 不因公式推导结束就写 `QED` |

第 5 条示例：

```text
GOAL:
    IF P THEN Q

ASSUME:
    P

HAVE:
    Q
BY:
    ...

THEREFORE:
    IF P THEN Q

QED
```

从 `ASSUME P` 推出 `Q`，最终才建立 `P ⇒ Q`。未解除局部假设前，不得把 `Q` 当无条件事实。同理：`SUFFICES B` 须说明为何证 `B` 即得目标；`WLOG` 须解释其余情形可归约。

---

## 7. 关键词补充修正

- `IFF`：充要条件 / 逻辑等价，不是"重要条件"。
- `WHERE`：局部约束或定义，不仅是限定范围；可写 `x = f(a), WHERE a := g(t)`。
- `ASSUME` / `CLAIM` / `SUFFICES` / `CASE` / `CONTRADICTION` / `WLOG`：按需插入的证明结构操作，不必每证必现。

---

## 8. 速查模板

```text
GIVEN / LET / DEFINE:
    建立上下文

GOAL:
    声明当前证明目标

MOTIVATION:
    解释为什么采用这种方法（可选）

HAVE:
    Expression 1
    = Expression 2        [BY ...]
    = Expression 3        [BY ...]
    = Expression 4        [BY ...]

INTERPRET / NOTE:
    解释或补充说明（可选）

HAVE:
    Expression 5
    = Expression 6        [BY ...]
    ⇒ Proposition A       [BY ...]

THEREFORE:
    Intermediate Result

HAVE:
    ...

CHECK:
    ...（可选）

THEREFORE:
    Final Result

QED
```
