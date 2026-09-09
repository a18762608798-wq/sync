# HCE 误差缓解

目标：用 Hamming 距离公式估计纯度 $\mathrm{tr}(\rho^2)$，
同时缓解门误差和读出误差。思路仿照 robust classical shadow，
噪声处理抄 Vitale et al., PRX Quantum 5, 030338 (2024) 附录 C，
关键步骤见 [02_Robust-Estimation](../../02_Robust-Estimation.md)。

## 噪声假设

照搬 robust-shadow 推导的假设：

* 门无关（gate-independent）、Markovian 噪声 $\Lambda$，
  作用在随机幺正**之后**、理想计算基测量**之前**；
* 局域噪声 $\Lambda=\bigotimes_j\Lambda_j$，
  每个 $\Lambda_j$ 保迹（TP）；
* 在一次 calibration/实验窗口内平稳；
  慢漂移用交错 iteration 处理，和原文 Fig. 1 一样。

含噪 Born 分布记为：

$$
P_\Lambda(s|U)=\langle s|\Lambda(U\rho U^\dagger)|s\rangle
=\mathrm{tr}\bigr(\rho\,U^\dagger\Lambda^*(|s\rangle\langle s|)U\bigr).
$$

第二行是 Heisenberg 绘景：$\Lambda^*$ 把纯投影变成了
被噪声抹过的混合算符。你证明里的 $P(U,s)$ 在含噪时
就替换成 $U^\dagger\Lambda^*(|s\rangle\langle s|)U$ 的版本。

## 理想情况回顾：把你的证明翻译成 twirl 语言

你原来的证明（[Hamming_Core_Estimation](Hamming_Core_Estimation.md#purity)）
核心是算

$$
\mathbb E_{U}\big[\sum_{s,s'}(-2)^{-D[s,s']}(P(s)\otimes P(s'))\big],
$$

其中 $P(s)\equiv P(U,s)=U|s\rangle\langle s|U^\dagger$
（$U$ 含在投影算符里，平均时才积掉）。
下面是同一个计算，只换一套名字。符号对照：

| 本文符号 | 你证明里的东西 |
|---|---|
| $W$ | 把 $U$ 剥掉后剩下的部分：bare 投影配上核函数，即 $W=\sum_{s,s'}f(s,s')\vert s\rangle\langle s\vert\otimes\vert s'\rangle\langle s'\vert$ |
| $\tau^{(2)}$（two-copy twirl） | 你们逐比特算 $A_{same}$、$A_{diff}$ 时做的那个 $\mathbb E_{U_n}$ 平均；$\Pi$ 重排不用显写，因为 $(U^\dagger)^{\otimes2}WU^{\otimes2}$ 里两个 copy 的指标本来就是对齐的 |
| $S$、$S_j$ | 全局 SWAP 和单比特 SWAP；$S=\sum_RR\otimes R$ 就是 logic_gates 笔记里的恒等式 |
| $\tau_j(W_j)=S_j/2$ | 你们算出来的 $2A_{same}-A_{diff}=\frac12\sum_\mu R_\mu\otimes R_\mu$，同一个等式 |

具体对应：$P(s|U)P(s'|U)$ 求和就是 $\mathbb E_{s,s'}$；
把 $P(s)=UP_{bare}(s)U^\dagger$ 代入，
$\mathbb E_U$ 全部落到 $U$ 上，正好是
$\tau^{(2)}(W)=\mathbb E_U[(U^\dagger)^{\otimes2}WU^{\otimes2}]$。
于是你们的结论
$\mathbb E_U[\sum(-2)^{-D}P\otimes P']=\frac1{2^N}\sum_RR\otimes R$
翻译过来就是 $\tau^{(2)}(W)=2^{-N}S$，
两边和 $(\rho\otimes\rho)$ 缩并即得
$\mathbb E[f]=2^{-N}\mathrm{tr}(\rho^2)$。
估计量前面的 $2^N$ 前缀从这里来。

最直接的证据：你 Pair 一节对一般核
$\varepsilon_{s_ns_n'}$ 算出的结果

$$
\frac12(\varepsilon_{00}+\varepsilon_{01})I\otimes I
+\frac16(\varepsilon_{00}-\varepsilon_{01})\sum_{\mu=1}^3\sigma_\mu\otimes\sigma_\mu,
$$

把 $\sum_1^3\sigma\sigma=2S-I$ 代入，
恰等于 $\tau_j$ 作用在
$\mathrm{diag}(\varepsilon_{00},\varepsilon_{01},
\varepsilon_{01},\varepsilon_{00})$ 上的结果
（两边都等于 $\frac{\varepsilon_{00}+2\varepsilon_{01}}3I
+\frac{\varepsilon_{00}-\varepsilon_{01}}3S$，可验算）。
理想 Hamming 取值 $\varepsilon_{00}=1$、
$\varepsilon_{01}=-\frac12$ 正好杀掉 $I\otimes I$ 项、
留下 $\frac12S$。下面要求的 dressed 核
$(x_j,y_j)$ 就是含噪版的
$(\varepsilon_{00},\varepsilon_{01})$，
即 $x_j\equiv\varepsilon_{00}$，$y_j\equiv\varepsilon_{01}$。

## Dressed 核的假设形式

有噪声时，同一个 $U$ 下的一对 shots 给出
$\mathrm{tr}[\tilde W\,(U\rho U^\dagger)^{\otimes2}]$，其中

$$
\tilde W=\sum_{s,s'}g(s,s')\,
\Lambda^*(|s\rangle\langle s|)\otimes\Lambda^*(|s'\rangle\langle s'|),
$$

对 $U$ 平均后
$\mathbb E=\mathrm{tr}[\tau^{(2)}(\tilde W)\rho^{\otimes2}]$。
取因子化对称假设

$$
g(s,s')=\prod_{j=1}^Ng_j(s_j,s'_j),\quad
g_j(a,a)=x_j,\quad g_j(a\ne b)=y_j,
$$

于是 $\tilde W=\bigotimes_jQ_j$，

$$
Q_j=\sum_{a,b}g_j(a,b)\,
\Lambda_j^*(|a\rangle\langle a|)\otimes\Lambda_j^*(|b\rangle\langle b|).
$$

对一切 $\rho$ 无偏，当且仅当
$\tau^{(2)}(\tilde W)=2^{-N}S$，
即逐比特 $\tau_j(Q_j)=S_j/2$。
记 $t_j=\mathrm{tr}Q_j$，$u_j=\mathrm{Tr}S_jQ_j$，条件是
（对照你 Pair 一节的展开式：$t_j$ 管 $I\otimes I$ 项的系数，
$u_j$ 管 SWAP 项的系数）

$$
t_j=1,\qquad u_j=2.
$$

## $t_j$ 方程：与噪声无关的求和规则

保迹给出
$\mathrm{tr}\,\Lambda^*(|a\rangle\langle a|)
=\mathrm{tr}(|a\rangle\langle a|\Lambda(I))=1$，所以

$$
t_j=\sum_{a,b}g_j(a,b)=2x_j+2y_j=1.
$$

即

$$
x_j+y_j=\frac12,
$$

跟噪声完全无关。还剩一个方程定核函数。

## $u_j$ 方程：每比特只需一个噪声参数

用 $\mathrm{tr}(S(A\otimes B))=\mathrm{tr}(AB)$，

$$
u_j=\sum_{a,b}g_j(a,b)M^{(j)}_{ab}
=A_jx_j+B_jy_j=2,
$$

其中
$M^{(j)}_{ab}=\mathrm{tr}(\Lambda_j^*(|a\rangle\langle a|)
\Lambda_j^*(|b\rangle\langle b|))$，
$A_j=M_{00}+M_{11}$，$B_j=M_{01}+M_{10}$，
即被抹过的投影两两之间的 Hilbert-Schmidt 内积之和。
因为 $\Lambda^*$ 保单位元（$\Lambda$ 保迹），

$$
A_j+B_j
=\mathrm{tr}\big[(\sum_a\Lambda^*(|a\rangle\langle a|))^2\big]
=\mathrm{tr}[\Lambda^*(I)^2]=\mathrm{tr}(I)=2.
$$

即恒有 $B_j=2-A_j$。联立解得

$$
x_j=\frac{A_j+2}{4(A_j-1)},\qquad
y_j=\frac{A_j-4}{4(A_j-1)}.
$$

检验：无噪（$A_j=2$）回到 $(1,-\frac12)$；
完全退极化（$A_j=1$）发散，
和 $\alpha_j,\beta_j$ 在 $G_j=1/2$ 处的
"无信息"奇点是同一回事。

## 算例：退极化噪声

$\Lambda(\rho)=(1-p)\rho+pI/2$，自伴随。
$X:=\Lambda^*(|0\rangle\langle0|)
=\mathrm{diag}(1-p/2,p/2)$，
$\mathrm{tr}X^2=1-p+p^2/2$，
$A=2\mathrm{tr}X^2=2-2p+p^2$。
比如 $p=0.04$：$A=1.9216$，
$x\approx1.063$，$y\approx-0.563$，
只是对 $(1,-0.5)$ 的轻微修正。

计算基退相位给出 $A_j=2$，
即理想核保持无偏——理应如此：
这种噪声根本不改变测量统计。

## Calibration：怎么测 $A_j$

$A_j$ 的操作定义：$A_j=\mathrm{tr}(X^2)+\mathrm{tr}((I-X)^2)$，
$X=\Lambda_j^*(|0\rangle\langle0|)$。
在 $|0\rangle^{\otimes N}$ 上跑
**同样的 same-$U$ pair 结构**
（直积态，所以逐比特 marginal 精确成立，
不需要任何近似），数每比特 pair 一致率：

$$
E_j^{(=)}:=\mathbb E_{U_j}\mathbb E_{s,s'}[\delta_{s_js'_j}].
$$

固定 $U$ 时
$\sum_aP_j(a|U)^2
=\mathrm{tr}[D_j\,(U|0\rangle\langle0|U^\dagger)^{\otimes2}]$，
$D_j=\sum_a\Lambda^*(|a\rangle\langle a|)^{\otimes2}$。
$\mathrm{tr}D_j=2$，
$\mathrm{tr}(S_jD_j)=A_j$；twirl 后和
$|00\rangle\langle00|$ 缩并
（$I$ 和 $S$ 的期望都是 1）：

$$
E_j^{(=)}=\frac13\big(1+A_j/2\big),\qquad
A_j=6E_j^{(=)}-2.
$$

Calibration 数据上的估计器
（$N_U$ 个 $U$，每个 $N_M$ shots）：

$$
\hat E_j^{(=)}=\frac{1}{N_U}\sum_r
\frac{1}{N_M(N_M-1)}\sum_{m\ne m'}
\delta_{s_j^{(r,m)},\,s_j^{(r,m')}},\qquad
\hat A_j=6\hat E_j^{(=)}-2.
$$

$m\ne m'$ 排除自配对，和主估计量的
$k\ne k'$ 同理，这是无偏的 U-statistic。
自检：无噪时 $E_j^{(=)}=2/3$
（Bloch 球平均 $\cos^4+\sin^4$）；
完全退极化时 $1/2$；
恒有 $1\le A_j\le2$
（$X\succeq0$，$\mathrm{tr}X=1$）。
实验值跑出界就说明假设被违反。
无噪值 $2/3$ 解析已知，
可以照原文 III.D 做 control variate 降方差。

## 完整流程

1. **Calibration**：制备 $|0\rangle^{\otimes N}$，
   同样的幺正系综，估计每比特 $\hat A_j$。
   只需要"哪些 shots 属同一个 $U$"的分组信息，
   连 $U$ 的具体值都不用记。
2. **解 kernel**：按上式算每比特 $(x_j,y_j)$，
   检查 $x_j+y_j=1/2$。
3. **缓解后的估计量**，在目标态数据上算：

$$
\hat P_2^{\mathrm{mit}}=\frac{2^N}{MK(K-1)}
\sum_m\sum_{k\ne k'}\prod_{j=1}^N
g_j(s_j^{(m,k)},s_j^{(m,k')}).
$$

   经典后处理成本不变。
4. **漂移**：calibration 和正式测量按 iteration 交错，
   每个 iteration 一套 $\hat A_j^{(i)}$。
5. **交叉检验**：$|0\rangle$ 本身必须返回 1；
   和同一批数据的 robust-shadow U-statistic 纯度
   （原文式 16）在误差棒内一致；
   否则走原文附录 E 的局域性检验。

## $A_j$ 和 $G_j$ 的关系

$$
G_j=\tfrac12\sum_a
\mathrm{tr}(\Lambda_j^*(|a\rangle\langle a|)|a\rangle\langle a|),
\qquad
A_j=\sum_a\mathrm{tr}([\Lambda_j^*(|a\rangle\langle a|)]^2).
$$

$G_j$ 是对角保真度，$A_j$ 是范数平方和。
单参数退极化下 $G=1-p/2$，
$A=4G^2-4G+2$；
但一般噪声下两者没有固定关系，
所以 $A_j$ 必须独立标定。
好消息是不增加量子开销：
同一批 $|0\rangle$ calibration 数据，
算 $G$ 用"含噪频率×理想概率"互相关，
算 $A$ 用 pair 一致率，
只是经典后处理不同。

## 非 unital 扩展（比如 $T_1$）

上面用了
$c_a:=\mathrm{tr}\,\Lambda^*(|a\rangle\langle a|)=1$。
对 amplitude damping 这类非 unital 信道，
$c_0=1+\delta$、$c_1=1-\delta$，
$t_j=1$ 的条件变成
$x(c_0^2+c_1^2)+2yc_0c_1=1$。
$c_a/2$ 可直接从 calibration 单 shots 频率
的 Haar 平均读出（单拷贝 twirl），
所以每比特至多需要两个标定量
$(A_j,\delta_j)$，框架不塌。

## 注意事项

* **Pair 内平稳**：一对 shots 的前后两次必须看到
  同样的噪声，比原文 iteration 内平稳更严。
* **读出误差**：形式上可吸收进 $\Lambda$，
  但 $D=0$ 项权重最大，
  读出翻转对方差的放大比单拷贝 shadow 更狠；
  值得数值验证，对照
  [Error_Bounds](../Error_Bounds.md)。
* $A_j\to1$ 时方差发散，和 $\alpha_j,\beta_j$
  在 $G_j\to1/2$ 处一样。
* 这只修正噪声 bias；Hamming core 的结构性局限还在，
  见 [HCE_Limit_of_Hamming_Core](HCE_Limit_of_Hamming_Core.md)。
