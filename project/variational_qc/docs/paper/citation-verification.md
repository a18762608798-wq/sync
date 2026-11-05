# 当前引用支撑索引

本文件维护文献与当前论文论述的支撑关系：cite key、Zotero key、已读位置、支持范围及正文绑定位置。按文献更新对应条目；正文范围改变时重新核对受影响的支撑关系。

下列内容整理自已有全文核验记录，本次整理未重新阅读文献。原记录缺少具体页、节或公式定位的条目明确标为“定位待补”，不补造已读位置；同作者扩展版与所引出版版也分别说明。章节文件名前缀同时指向 `sections/` 下英文及对应 `-zh.tex` 中文文件。

实验定义及结果以 [Exp 规范](../../specs/)、正式数据和 manifest 为准；本文献索引不重复维护实验参数、验收状态或数值结果。修订历史通过 Git 查看，编译及数值验证的详细输出保留在已有运行目录。本次整理前的完整记录保存在 [原始快照](../../data/validation/paper-record-scope-20261105-8olb9nnk/before/project/docs/paper/citation-verification.md)，供查阅尚未提交的历史证据，不继续追加。

## 模型、对称性与拓扑诊断

| cite key | Zotero key | 已读全文位置 | 支撑论述与适用条件 | 正文位置 |
| --- | --- | --- | --- | --- |
| `su1979solitons` | `P7R34NFU` | 原文 pp. 1--2 | SSH 交替键模型的来源；本文相互作用自旋链的分类另有依据。 | `01-model` |
| `ryu2010topological` | `5F4TT9SR` | arXiv:0912.2157，Sec. 2，p. 9，Table 1 及说明 | 十重分类针对单粒子哈密顿量，用于非相互作用参照；不直接分类本文自旋链。 | `01-model` |
| `gu2009tensor` | `UJYVQLZP` | arXiv:0903.1069，Sec. V F，p. 14 | 对称性约束下相的等价与区分；具体保护群和 MPS 分类结合后续文献。 | `01-model` |
| `chen2010local` | `FVM2XMZ8` | arXiv:1004.3835，Secs. V--VI，pp. 5--6 | 对称局域幺正等价与 SPT 定义；要求局域、保持对称且与恒等连通的路径。 | `01-model` |
| `chen2011classification` | `GCIB9LCZ` | arXiv:1008.3745，MPS 与现场对称分类段落；具体页/节定位待补 | 一维对称有能隙自旋相的虚拟投影表示和上同调分类；不是有限开链分类已收敛的证明。 | `00-introduction`、`01-model` |
| `schuch2011classifying` | `RME7WIRI` | arXiv:1010.3732，Sec. II C；已读 MPS 与母哈密顿量相关正文 | MPS 框架下的对称相分类及有能隙路径；保留一维、对称与有能隙假设。 | `00-introduction`、`01-model` |
| `schollwock2011density` | `3AJILFTW` | arXiv:1008.3477，Sec. 4.1.1，pp. 16--17，Eqs. (20)--(25)；另已读 pp. 65--66、71--72，Secs. 6.3--6.4 | 当前绑定用于 Schmidt 分解与 MPS；补充阅读支持局部张量变分优化及单/双站点 DMRG 方法背景，项目自己的扇区惩罚与参数不归为该综述方案。 | `01-model`；DMRG 方法阅读尚未单独绑定 |
| `cirac2021matrix` | `GS8923LS` | arXiv:2011.12127，Sec. III A，pp. 31--34，Eqs. (44)--(45) | 可注入 MPS 的现场、时间反演和反射分类；有限链猫态与破缺相不直接套唯一有能隙基态结论。 | `01-model` |
| `pollmann2012detection` | `WCRRQH9M` | arXiv:1204.0704，Sec. II B，Eqs. (7)--(9)；Sec. IV A，Eqs. (17)--(18) | 虚拟投影表示与 string 端点选择规则；对称、可注入 MPS 的长串规则不直接等同于有限开链首尾关联，允许非零也不保证非零。 | `00-introduction`、`01-model`、`04-heatmaps` |
| `verresen2017onedimensional` | `UG93KMJX` | arXiv:1707.05787，Sec. I，pp. 2--4 | 边缘对称性分数化，含交替 Heisenberg 链例子及晶胞表示条件。 | `01-model` |
| `pollmann2012symmetry` | `9X9X5TCX` | arXiv:0909.4059，Secs. II--III，pp. 2--5 | $D_2$、自旋时间反演及键反演的保护作用；有限链边缘劈裂不作为体相定义。 | `01-model` |
| `li2008entanglement` | `IZICB99P` | arXiv:0805.0332；具体页/节定位待补 | 纠缠谱作为拓扑序指纹的来源，原文语境为分数量子霍尔体系；一维 SPT 的保护简并由 Pollmann 等支撑。 | `01-model` |
| `pollmann2010entanglement` | `TXREEMXW` | arXiv:0910.1811，Secs. III--IV | 一维 Haldane 型相的纠缠谱简并及对称保护；不混同于内禀拓扑序。 | `01-model` |
| `elben2020manybody` | `MPE67Q6B` | 出版版 pp. 1--4，p. 2 “Partial reflection invariant”，Eqs. (2)--(4)；另已读 arXiv:1906.05011，pp. 1--3 | 玻色部分反射标记、归一化纯度与随机测量协议；镜像关联的局域旋转及多个设置不可省略，重叠与纯度可从同一随机测量数据估计。量子化要求区间大于关联长度；本文数值计算标记，实验另测计算基关联。 | `00-introduction`、`01-model`、`04-heatmaps` |
| `shiozaki2017manybody` | `URA4V7WK` | arXiv:1609.05970，Sec. I C，p. 5，Eqs. (1.6)--(1.8) | 部分空间变换用于费米 SPT 多体不变量；其费米相位不套入本文玻色算符。 | `01-model` |
| `elben2022toolbox` | `YTBCD6JR` | arXiv:2203.11374；多体不变量与随机测量相关段落，具体页/节定位待补 | 对称保护多体不变量及纯度等量的随机测量实现；不是本文已执行该协议的证据。cite key 沿用原名，正式出版年份见 BibTeX。 | `01-model` |

## 关联测量与实验背景

| cite key | Zotero key | 已读全文位置 | 支撑论述与适用条件 | 正文位置 |
| --- | --- | --- | --- | --- |
| `perezgarcia2008string` | `H69QSWUL` | arXiv:0802.0447，p. 2，Lemma 1 / Theorem 1 | MPS 框架下 string 序与局域对称性的关系；保留定理对象与假设，普通 string 不替代一般 SPT 分类。 | `04-heatmaps` |
| `dennijs1989preroughening` | `3EJ4I2TP` | Sec. IV C，原刊 p. 4723 / PDF p. 15，Eqs. (4.2)--(4.5) | 自旋链 string 序来源；本文晶胞端点、内部负号和倍数关系来自自身算符推导。 | `04-heatmaps` |
| `haegeman2012order` | `QIWCCNMC` | arXiv:1201.4174，pp. 1--3，MPS 固定点与交换测量构造 | 普通 string 的局限及对称性相关诊断；本文未实施该交换测量协议。 | `00-introduction`、`04-heatmaps` |
| `endres2011observation` | `AQY9KWUG` | arXiv:1108.3317；具体页/节定位待补 | 低维 Mott 绝缘体中关联粒子空穴对与非局域 string 序的实验背景；不等同于本文自旋链测量。 | `04-heatmaps` |
| `huang2020predicting` | `94QNC4QU` | arXiv:2002.08953，p. 2，classical shadow 数据获取与预测段落；附件 `4KL248JN` | 随机基测量与经典阴影的观测量预测；本文单一计算基采样不继承其普遍保证。 | `04-heatmaps` |
| `cong2019quantum` | `YBET8WFZ` | arXiv:1810.03787，p. 2，QCNN circuit model 与 phase recognition 段落 | 含测量和反馈的电路型相识别策略；不声称仅需本文相同的计算基数据。 | `04-heatmaps` |
| `kitaev2006topological` | `6FB8TCYP` | 原记录确认已读技术内容，未保存页/节定位，待补 | 拓扑纠缠熵作为内禀拓扑序诊断；与一维玻色 SPT 的区分保持清楚。 | `00-introduction` |
| `levin2006detecting` | `FYBSJVQI` | 原记录确认已读技术内容，未保存页/节定位，待补 | 从基态波函数识别内禀拓扑序及拓扑纠缠熵；不直接作为本文一维 SPT 分类。 | `00-introduction` |
| `satzinger2021realizing` | `8WC7LVIH` | arXiv:2104.01180；具体页/节定位待补 | 超导处理器上的 toric-code 态制备及拓扑纠缠熵测量；用于实验背景。 | `00-introduction` |
| `deleseleuc2019observation` | `SX4ARZEG` | arXiv:1810.13286，pp. 2--3，SSH model for hard-core bosons 与 experimental realization | 里德伯原子实现的玻色 SSH SPT 相与多体保护对称性；不混同于自由费米子的手征保护。 | `00-introduction`、`01-model` |
| `tan2023realizing` | `XWW5BLHC` | arXiv:2112.10333，Sec. II A--B，pp. 3--4，Eqs. (1)--(3) | 超导处理器上的次近邻 SPT 链与计算基 string 读出；该文的绝热制备及重编译不同于本文 VQE。 | `00-introduction`、`04-heatmaps` |

## 变分方法与拟设比较

| cite key | Zotero key | 已读全文位置 | 支撑论述与适用条件 | 正文位置 |
| --- | --- | --- | --- | --- |
| `peruzzo2014variational` | `K8NY4LJ9` | arXiv:1304.3061；具体页/节定位待补 | 参数化电路结合经典优化的变分本征求解器；本文具体优化预算由 Exp 定义。 | `00-introduction`、`06-ansatz` |
| `cerezo2021variational` | `NBV9FIIP` | arXiv:2012.09265；代价函数和拟设相关段落，具体页/节定位待补 | VQA 的电路、代价函数、测量与优化背景；不据综述保证本文算法性能。 | `00-introduction`、`06-ansatz` |
| `tilly2022variational` | `9VYJZQIJ` | arXiv:2111.05176；具体页/节定位待补 | VQE 方法与最佳实践综述；不为本项目未测性能背书。 | `00-introduction`、`06-ansatz` |
| `kandala2017hardware` | `6VE4TBI8` | 原文 p. 2，Fig. 1(c) 与 Eq. (2) | 超导 VQE 的分子及磁体演示、单比特 Euler 旋转与纠缠层交替；不同层定义下不直接比较同精度深度。 | `00-introduction`、`06-ansatz` |
| `wecker2015progress` | `PI73XDN2` | arXiv:1507.08969，p. 2，Eq. (1) 及其后对称性、经典优化段落 | HVA 的哈密顿量生成元与独立变分角；不等同于固定绝热时间表。 | `06-ansatz` |
| `wiersema2020exploring` | `FIN75BUI` | arXiv:2008.02941，pp. 1--4；Sec. II，p. 4 的 Eq. (7) 与 Fig. 2 | XXZ HVA、奇偶键与横纵向旋转共享，共 $4p$ 个角且 $XX$ 与 $YY$ 同角；原数值模型为周期边界，本文开放链比较须保持该区别。 | `06-ansatz` |
| `gard2020efficient` | `98HJVY8U` | arXiv:1904.10910，p. 2，Sec. II 的对称子空间讨论 | 对称电路缩减搜索空间；其化学问题全空间覆盖保证不转移到本文拟设。 | `06-ansatz` |
| `ho2019efficient` | `IFSMJ8F2` | arXiv:1803.00026，Sec. 2，p. 4，GHZ 与局域电路论证 | 非平庸初始纠缠作为态制备资源；不构成本文浅层电路的普遍效率保证。 | `06-ansatz` |
| `mcclean2018barren` | `INQIR6DI` | arXiv:1803.11173；具体页/节定位待补 | 接近相应随机设计条件的电路可有指数小梯度；不把结论扩展为所有结构化电路都不可训练。 | `06-ansatz` |
| `cerezo2021cost` | `KDP9R89P` | arXiv:2001.00550，p. 2，Fig. 1、Results 与局域/全局代价对比 | 梯度行为依赖代价函数和深度；不证明本文免于贫瘠高原。 | `06-ansatz` |
| `grant2019initialization` | `EC44PZN4` | arXiv:1903.05076，Sec. 3，p. 3，Eqs. (7)--(10) | 恒等块初始化及初始迭代的梯度动机；本文没有采用其完整初始化协议。 | `06-ansatz` |
| `campos2021abrupt` | `D6G65X4B` | arXiv:2010.09720；具体页/节定位待补 | 结构化变分电路训练随深度的突变与可训练性研究；不保证本文局域优化的收敛性。 | `06-ansatz` |
| `wang2021noise` | `KBE5KH5Y` | arXiv:2007.14384，pp. 3--4，local Pauli noise setting、Lemma 1 与 Theorem 1 | 特定局域 Pauli 噪声模型下梯度压低；不泛化到任意噪声。 | `06-ansatz` |
| `sun2023efficient` | `FPSUMAZF` | 库内 arXiv 全文 pp. 1--6；pp. 4--5 的 Eqs. (4)--(12) 与 Figs. 3--4，p. 6 反射约束讨论 | 初始纠缠结构加浅层 eSWAP 修饰、独立键角、两种子层顺序及镜像约束；本文分别参数化横纵向并增加 AFM 参考分支，不将相匹配初始化或反射约束本身写成首次提出。 | `00-introduction`、`06-ansatz` |
| `yu2023simulating` | `JFQRHJBC` | 出版版 pp. 1--6，pp. 5--6 的 Fig. 1 与 Eqs. (7)--(13) | 单态初态、奇偶键交替与同类键统一共享转角；XXZ 每层四角、各向同性两角，已有三 CNOT 键块分解。本文均匀共享基线是文献启发的受限结构，实测优势由本项目结果支撑。 | `00-introduction`、`06-ansatz` |

## 读出缓解

| cite key | Zotero key | 已读全文位置 | 支撑论述与适用条件 | 正文位置 |
| --- | --- | --- | --- | --- |
| `bravyi2021mitigating` | `X3WB23G3` | arXiv:2006.14044；具体页/节定位待补 | 张量积分配矩阵与含关联 CTMP 模型，支持独立误差近似和模型区别；两种全局基态制备不足以识别一般关联模型。 | `08-readout` |
| `cai2023quantum` | `YWVJ2CJ7` | arXiv:2210.00921，Sec. III C，p. 10，Eqs. (19)--(24) | 分配矩阵、张量积假设、关联误差与抽样代价；读出前分布是已制备态的分布，缓解不消除全部门与制备误差。 | `00-introduction`、`08-readout` |
| `maciejewski2020mitigation` | `8PUKRW3H` | arXiv:1907.08518，Sec. 4.3，p. 7，Eqs. (25)--(27) | 线性反演负概率及到概率单纯形的欧氏投影；当前正文采用该凸问题，排序阈值求解来自其最优性条件，有限采样偏差仍需区分。 | `08-readout` |
| `endo2021hybrid` | `L6HIIJG2` | arXiv:2011.01382，Sec. V G，p. 28，Eqs. (140)--(143) | 测量噪声矩阵与概率矫正的综述背景。 | `00-introduction` |

## 能隙、有限尺寸与簇态方法

| cite key | Zotero key | 已读全文位置 | 支撑论述与适用条件 | 正文位置 |
| --- | --- | --- | --- | --- |
| `sandvik2010computational` | `WCKVFLZP` | arXiv:1101.3281，Sec. 3.3，Sec. 4，尤其 Secs. 4.2--4.3 | 有限尺寸诊断、Lanczos/Krylov 与一维链基态和激发方法背景；实际尺寸、扇区、收敛判据和拟合结果由 Exp 定义。结构因子在正文的计算基单样本模平方表达是本项目推导。 | `03-sq`、`A-appendix` |
| `lukyanov1998lowenergy` | `TTYPYSFE` | arXiv:cond-mat/9712314，Sec. II，p. 3；Sec. IV，pp. 11--13 | 均匀 XXZ 高斯低能理论与有限尺寸修正；其符号及扭转周期边界系数不直接用于本文开链。 | `A-appendix` |
| `takayoshi2010coefficients` | `9V9PJCZM` | arXiv:1005.1704，Sec. II A--B，Eqs. (2)、(4)、(7)--(9)；Sec. III，Eqs. (19)--(20) | XXZ 玻色化、二聚化扰动、标度维数与扇区修正；弱耦合体理论和本项目经验拟合分别表述。 | `A-appendix` |
| `sirker2008thermodynamics` | `RH8NUY46` | arXiv:0801.1201，p. 6，Sec. 2 末段；pp. 8--9，Sec. 3，Eqs. (3.18)--(3.20)；Sec. 2 开链玻色谱 | 无破坏对称性的边界外场时，开边界 XXZ 的主导无关边界算符维数为 $2$，产生有效长度偏移；原文主要检验磁化率，不直接给出本项目固定多重对称扇区的能隙系数。 | `A-appendix`，`eq:gap-fit` 前 |
| `liu2024finitesize` | `X32BR5K2` | arXiv:2405.06891v2，Sec. 2.1.1，Eqs. (5)--(8)；p. 6，Sec. 2.1.2，Eqs. (14)--(16) | 维数为 $2$ 的边界应力张量带来低能能级的 $1/L^2$ 修正，可等价描述为非普适长度偏移；原文 Ising/Potts 例子不直接给出本文 XXZ 扇区系数，也不证明自由截距经验拟合已到渐近区。 | `A-appendix`，`eq:gap-fit` 前 |
| `raussendorf2001oneway` | `4AELG4TT` | 所引 PRL 原文未直读；已读同作者扩展版 arXiv:quant-ph/0108067，Eq. (2) 与簇态制备段落 | 簇态的稳定子本征方程，以及 $CZ$ 作用于全体 $\lvert+\rangle$ 的制备。技术支撑来自同作者扩展版，不能记为 PRL 全文已读。 | `A-appendix`，簇态基准定义 |
| `toth2005detecting` | `MPN89WLD` | arXiv:quant-ph/0405165，p. 3，Eqs. (8)--(9)，Theorem 2 | 二分簇态稳定子及两个局域测量设置；本项目加权评分不是该文的纠缠见证。 | `A-appendix`，簇态测量设置 |

## 已核验、当前未绑定的来源

保留可复用的文献证据，不将未采用方案或背景阅读写成当前实验方法。

| 来源 | Zotero key / 身份 | 已读位置与支撑范围 | 绑定状态 |
| --- | --- | --- | --- |
| Campostrini、Pelissetto、Vicari，*Finite-size scaling at quantum transitions* (2014) | `9PZENU2C`，PDF `MIZA2VYP`；DOI `10.1103/PhysRevB.89.094516` | arXiv:1401.0788，pp. 3--5，Secs. II A、II C，Eqs. (13)--(15)、(28)；Sec. III D，Eqs. (97)、(109)--(113)。非周期边界的逆长度标度场与有效长度偏移支持二阶修正动机；XY 例子的系数不转移给 XXZ。 | 已核验背景阅读；当前正文未引用 |
| Nation 等，*Scalable mitigation of measurement errors on quantum computers* (2021) | `3QSYME47`；DOI `10.1103/PRXQuantum.2.040326` | arXiv:2108.12518，pp. 1--2，Secs. I--II，Eqs. (1)--(5)。M3 的观测 bitstring 子空间、列归一化与无矩阵求解；模型含相关误差仍需相应标定信息，不保证本文观测量改善。 | 当前正文未采用或引用 |
| van den Berg 等，*Model-free readout-error mitigation for quantum expectation values* (2022) | `3Y6JUJKC`；DOI `10.1103/PhysRevA.105.032620` | 已读原文 pp. 2--4，Sec. II 的 AcquireData / Protocol 1、Sec. III 与 Sec. IV A--B。需要采样前随机 Pauli-$X$、翻转模式及随机化标定；不能靠事后翻转当前 bitstring 数据补做协议。 | 当前正文未采用或引用 |

## 现存证据缺口

- 上表标为“定位待补”的条目已有全文核验结论，但原记录的定位精度不足；后续涉及这些论述的实质修改时，补读并更新对应条目。本次整理不将缺少定位的历史结论升级为重新核验通过。
- `raussendorf2001oneway` 的所引 PRL 出版版仍缺直接阅读记录；当前技术支撑明确来自已读的同作者扩展版。
- `schollwock2011density` 的 DMRG 方法补充阅读已有依据，尚未在当前附录中单独绑定；这与其在模型节的现有引用范围分别维护。
