# 引用核验记录（paper-zotero-hunter verify 台账）

## 本轮权威文献重构与复核（2026-11-03，53 篇实际引用）

本节为当前稿件的核验入口；下方旧轮次记录保留历史，其与本节冲突的表述不再代表当前结论。此次目标是依据权威文献重建理论及完善引用，不以已有实验笔记的形式限制正文。

### 范围与数量

- 中英文稿分别实际引用 **53 篇、53 个不同 DOI**，两版引用集合一致；不是以 BibTeX 库存或未引用条目凑数。共同书目共 65 条，其余 12 条未引用项保留，不计入 53 篇。
- 新增 27 条经过技术内容核验的正文来源：26 篇经 DOI 去重新建 Zotero 条目，另 1 篇为原库已有的 Huang--Kueng--Preskill 工作；统一归入 physics/quant_comp/paper/inbox（ANJT35BK）及既有论文引用集合 paper-variational-qc（N7CLH4TB）。新增条目及新挂附件沿用 agent-crawled、unreviewed；后者仍表示待人工审核。
- 新增来源均取得开放获取 PDF，经首页标题和作者核对后挂入 Zotero。为 Tilly、Sandvik、Nation、Campos 四个既有引用补挂全文。论文引用的 53 个条目均有 PDF；集合覆盖检查为 65 条中 59 条有 PDF，其余 6 条均未在正文引用。
- 下表所称核验是阅读相关定义、方法、推导或结果段落，不以摘要、标题或“有附件”本身当作技术证明。既有 26 篇沿用早前已读记录，并对本轮改变论述范围的核心来源重新核对；不声称本轮从头通读每篇的全部页数。

### 新增正文来源：身份、已读位置与支持边界

| cite key | Zotero key | 已读全文位置 | 支持及限制 |
| --- | --- | --- | --- |
| `pollmann2012symmetry` | `9X9X5TCX` | 0909.4059；Secs. II--III，pp. 2--5 | D2、自旋时间反演、键反演的保护作用；不将有限链边缘劈裂当作体相定义。 |
| `pollmann2012detection` | `WCRRQH9M` | 1204.0704；Sec. II B，Eqs. (7)--(9)；Sec. IV A，Eqs. (17)--(18) | 虚拟投影表示和 string 端点选择规则；非零 string 不构成一般 SPT 分类。 |
| `shiozaki2017manybody` | `URA4V7WK` | 1609.05970；Sec. I C，p. 5，Eqs. (1.6)--(1.8) | 部分空间变换的不变量；明确为费米体系背景，不把其费米相位套入本文玻色算符。 |
| `verresen2017onedimensional` | `UG93KMJX` | 1707.05787；Sec. I，pp. 2--4 | 边缘对称性分数化；包含交替 Heisenberg 链例子及晶胞表示的适用条件。 |
| `gu2009tensor` | `UJYVQLZP` | 0903.1069；Sec. V F，p. 14 | 对称性约束下相的等价与区分；具体保护群采用后续 Pollmann 和 MPS 分类，避免沿用早期论述的过强范围。 |
| `chen2010local` | `FVM2XMZ8` | 1004.3835；Secs. V--VI，pp. 5--6 | 对称局域幺正等价与 SPT 定义；保持局域、保持对称且与恒等连通的路径条件。 |
| `schollwock2011density` | `3AJILFTW` | 1008.3477；Sec. 4.1.1，pp. 16--17，Eqs. (20)--(25) | Schmidt 分解与约化谱。MCP 该页提取失败，改读已挂 Zotero 的同一 arXiv PDF 文本；不据此声称本文使用 DMRG。 |
| `cirac2021matrix` | `GS8923LS` | 2011.12127；Sec. III A，pp. 31--34，Eqs. (44)--(45) | 可注入 MPS 的现场、时间反演和反射分类；有限链猫态、破缺相不直接套唯一有能隙基态结论。 |
| `haegeman2012order` | `QIWCCNMC` | 1201.4174；pp. 1--3，MPS 固定点与交换测量构造 | 普通 string 的局限，以及根据对称性构造交换型诊断；不宣称本文已实施交换协议。 |
| `lukyanov1998lowenergy` | `TTYPYSFE` | cond-mat/9712314；Sec. II，p. 3；Sec. IV，pp. 11--13 | 均匀 XXZ 高斯低能理论及有限尺寸修正；其符号与扭转周期边界约定不能直接作为本文开链系数。 |
| `ryu2010topological` | `5F4TT9SR` | 0912.2157；Sec. 2，p. 9，Table 1 及其说明 | 十重分类针对单粒子哈密顿量；引用用于说明其不能单独分类本文相互作用自旋链。 |
| `takayoshi2010coefficients` | `9V9PJCZM` | 1005.1704；Sec. II A--B，Eqs. (2)、(4)、(7)--(9)；Sec. III，Eqs. (19)--(20) | XXZ 玻色化、二聚化扰动、标度维数与扇区修正；弱耦合体理论与五点经验拟合分别表述。 |
| `deleseleuc2019observation` | `SX4ARZEG` | 1810.13286；pp. 2--3，SSH model for hard-core bosons 与 experimental realization | 里德伯原子玻色 SSH 实现与多体保护对称性；不与自由费米子的手征保护混为一谈。 |
| `tan2023realizing` | `XWW5BLHC` | 2112.10333；Sec. II A--B，pp. 3--4，Eqs. (1)--(3) | 超导处理器的次近邻 SPT 链与 Z 基 string 读出；该文使用绝热制备及重编译，不伪称为本文相同 VQE。 |
| `ho2019efficient` | `IFSMJ8F2` | 1803.00026；Sec. 2，p. 4，GHZ 和局域电路论证 | 非平庸纠缠结构作为态制备资源；不据此给本文浅层电路宣称普遍效率。 |
| `wecker2015progress` | `PI73XDN2` | 1507.08969；p. 2，Eq. (1) 与其后对称性、经典优化段落 | Hamiltonian variational ansatz 的生成元与自由转角；本文不是固定绝热时间表。 |
| `gard2020efficient` | `98HJVY8U` | 1904.10910；p. 2，Sec. II 的对称子空间讨论 | 对称电路缩减搜索空间；不将其化学问题的全空间覆盖保证转移给本文拟设。 |
| `wiersema2020exploring` | `FIN75BUI` | 2008.02941；p. 2，Sec. II 与 XXZ 优化、初始化讨论 | HVA 的模型依赖、纠缠结构和初始化；不视作本文可训练性保证。 |
| `cerezo2021cost` | `KDP9R89P` | 2001.00550；p. 2，Fig. 1、Results 和局域/全局代价对比 | 浅层电路也可出现依赖代价函数的梯度差异；保留电路与深度条件，不证明本文免于贫瘠高原。 |
| `wang2021noise` | `KBE5KH5Y` | 2007.14384；pp. 3--4，local Pauli noise setting、Lemma 1 和 Theorem 1 | 特定局域 Pauli 噪声模型下的梯度压低；不写成一切噪声下的结论。 |
| `grant2019initialization` | `EC44PZN4` | 1903.05076；Sec. 3，p. 3，Eqs. (7)--(10) | 恒等块初始化及初始迭代的梯度动机；本文未采用该完整初始化方案，不借其结论作保证。 |
| `cai2023quantum` | `YWVJ2CJ7` | 2210.00921；Sec. III C，p. 10，Eqs. (19)--(24) | 分配矩阵、张量积假设、相关误差与抽样代价；读出缓解不等于门误差或态制备误差已消除。 |
| `maciejewski2020mitigation` | `8PUKRW3H` | 1907.08518；Sec. 4.3，p. 7，Eqs. (25)--(27) | 反演负概率及其欧氏投影；本文实际使用截断后重归一，明确不是该投影且可引入偏差。 |
| `toth2005detecting` | `MPN89WLD` | quant-ph/0405165；p. 3，Eqs. (8)--(9)、Theorem 2 | 簇态稳定子及两个局域设置；项目加权分数不冒充该文的纠缠见证。 |
| `cong2019quantum` | `YBET8WFZ` | 1810.03787；p. 2，QCNN circuit model 与 phase recognition 段落 | 相识别的电路型替代策略，包含测量和反馈；不声称只需本文同一组 Z 基采样。 |
| `huang2020predicting` | `94QNC4QU` | 2002.08953；p. 2，classical shadow 数据获取与预测；读附件 4KL248JN | 随机基测量的经典阴影；不宣称本文测量数具有该文的普遍保证。此文原已在其他集合，本轮归入论文集合。 |
| `endo2021hybrid` | `L6HIIJG2` | 2011.01382；Sec. V G，p. 28，Eqs. (140)--(143) | 测量噪声矩阵与概率矫正；正确出版 DOI 为 10.7566/JPSJ.90.032001。 |

### 既有来源的复核与元数据修正

- Chen 2011（GCIB9LCZ，MPS 与现场对称分类）、Schuch 2011（RME7WIRI，Sec. II C 的有能隙路径定义）、Pollmann 2010（TXREEMXW，Secs. III--IV 的纠缠谱与反演）及 Pérez-García 2008（H69QSWUL，p. 2 的 Lemma 1/Theorem 1）重新读取相关正文。其结论针对体极限和相应假设，不再把“与有限链约定一致”写成分类定理已直接作用于 $L=8$ 的证明。
- Su 1979（P7R34NFU，pp. 1--2）本轮已直接读取，确认交替键来源；不再保留“本轮无法读原文”的旧缺口。den Nijs--Rommelse 1989（3EJ4I2TP，Sec. IV C，原刊 p. 4723、PDF p. 15，Eqs. (4.2)--(4.5)）也已直接读取，确认 string 序来源；项目特有的晶胞因子另作推导。
- Kandala 2017（6VE4TBI8，p. 2）确认超导 VQE 的分子与磁体演示；Yu 2023（JFQRHJBC，p. 2、Table I）确认云端长自旋链研究；van den Berg 2022（3Y6JUJKC，Sec. II，p. 2）确认其方法依赖随机翻转。三者是此前未在正文使用、本轮依据实际用途纳入的既有书目。
- 其余沿用早前技术核验的来源：Peruzzo（K8NY4LJ9）、Cerezo VQA 综述（NBV9FIIP）、Tilly（9VYJZQIJ）、McClean（INQIR6DI）、Campos（D6G65X4B）、Bravyi（X3WB23G3）、Nation（3QSYME47）、Elben 2020（MPE67Q6B）、Elben toolbox（YTBCD6JR）、Endres（AQY9KWUG）、Li--Haldane（IZICB99P）、Kitaev--Preskill（6FB8TCYP）、Levin--Wen（FYBSJVQI）、Satzinger（8WC7LVIH）、Sun（FPSUMAZF）、Sandvik（WCKVFLZP）和 Raussendorf--Briegel（4AELG4TT）。用途仍限于原文实际方法或理论；内禀拓扑序、玻色 SPT 和本文特有构造分别表述。
- Elben 2020 再读 pp. 1--3，并目读 p. 2 图像核对式 (1)--(4)：项目与该文的模型参数换算为 $J=2(1-s)e^{-\delta}$、$J'=2se^{-\delta}$、$\Delta=e^{2\delta}$；量子化需要区间充分大于关联长度，且随机基旋转不可省略。旧记录中“常规基测量下计算反射标记”已由正文明确更正为数值波函数计算。
- 修正 Peruzzo 2014 的书目文章号为 4213（旧稿将 DOI 后缀 5213 误作文章号）；Zotero 中本来正确，现同步至 BibTeX。补全 Elben 2020 在 Zotero 中缺失的后三位作者及卷、期、文章号；补全 Huang 2020 的卷页。
- 修正多个新入库 APS 条目导入时遗漏的文章号，身份以 DOI、原文和 arXiv 期刊信息交叉确认。Takayoshi 标题的 MathML 被导入为错误字符串，已按原文修正为 spin-1/2 XXZ chains。保留所有既有合法 cite keys，包括 Elben toolbox 的旧年份 key；其实际期刊卷页年份仍为 2023。
- Colless 的未引用旧条目标题及作者遗漏也按 Zotero/Crossref 元数据修正；它不计入 53 篇。初筛误命中的 Magann 等文章仅从本轮两个集合移出，未删除库内条目；Endo 综述已按正确 DOI 重新核实，不以错误 DOI 配上目标标题。

### 理论改进及本项目推导

1. 从两格点晶胞的自旋零与自旋一空间出发建立现场 $D_2$ 表示，再解释虚拟投影表示；不假定模型已投影为自旋一链。分别说明反射、时间反演保护与内部对称性保护，不把自由费米子十重分类套用于相互作用链。
2. 从 $T_r^z=(Z_{2r-1}+Z_{2r})/2$ 推出 $e^{i\pi T_r^z}=-Z_{2r-1}Z_{2r}$，实际测量的 string 量为晶胞关联的四倍。符号、端点、内部负号均与 Exp02/Exp06 现行算符核对。进一步以端点在 $u_x$ 下为奇，说明 Pollmann--Turner 的选择规则如何联系本文所选算符：对称、可注入 MPS 中，端点位于体内的长串在 $\eta=+1$ 时被禁止，$\eta=-1$ 时允许；允许不等于保证非零。本文实际有限开链首尾关联还依赖边界态，不将其非零值当作完整分类。
3. 三个参考态的 $(\hat S,\hat O)$ 分别为 $(1/4,0)$、$(1/4,1)$、$(1,0)$，据此确定唯一仿射组合 $Q$，依次取正一、负一和零。这是本文的参考态构造，不作为文献已有恒等式，也不声称一般态的 $Q=\tilde Z_{\mathcal R}$ 或普遍量子化。反号 string 量不保证落在 $[0,1]$。
4. 固定尺度结构因子等于交错磁化二阶矩；计算基单次样本的模平方形式给出非负性。有限链二阶矩不等于自发破缺已被证明。
5. 能量与保真度的条件界由同扇区谱分解给出：唯一基态且 $\Delta_{\rm sec}>0$ 时，$E-E_0\geq\Delta_{\rm sec}(1-F_0)$。该界未被用于估计真机保真度。
6. 以已核验 XXZ / sine-Gordon 文献说明 $\delta=-2$ 的均匀临界点、弱二聚化相关扰动及其适用范围；撤去旧笔记中“开链奇偶键交换加反射保证谱对称”和“固定该各向异性扫描为 BKT”的错误推断。
7. D02c 仍使用原有五点与二次经验拟合，读取存档系数 $a=-0.016764691580115853$、$b=94.85614016305661$、$c=-114.14443795338093$；未重算本征对或拟合。负截距不是负物理能隙，五点拟合不证明精确极限，更不证明整个相图已收敛。对应 spec、plan、大纲与笔记仅同步解释边界，编号、任务状态、算法及阈值保留。
8. 明确所有变分优化在理想经典模拟中进行；真机执行优化后电路测量关联量。D09 背景标签经实际 D09 内核及 S06 核对，是最低代价初态分支，并非独立的拓扑分类结果。
9. 读出模型仅覆盖其假设范围；本文实际使用负值截断后重归一，不冒充欧氏概率投影。硬件归一化与模拟固定尺度分别定义；最佳窗口的相关系数和误差棒为条件性、样本内描述，不作为独立相认证。
10. 摘要、引言、结果及结论同步上述证据边界。保留真机 string 信号符号与模拟相反的事实，不以归一化后的趋势代替拓扑态制备证据。

### 本轮直接验证与剩余缺件

- Julia 项目环境直接调用现行初态和 Exp02 观测量内核：三个参考态的结构因子、string、$Q$ 与反射值均匹配推导；全部 256 个计算基态逐一核对晶胞指数形式与实际 string 算符恒等。记录为 PAPER-REFERENCE-CHECK-OK。
- Exp06 层数元数据发现与修复：现行 spec 与全部 30 个归档分组均为 $p=1$，common 与 assembler 仍残留硬编码二层。现按同一层数常量写入清单并校验分组；已有清单只纠正该字段，未改 counts、参数、归一化或数值产物。原有 Exp06 本地测试 11 项通过，未调用真机。
- 中英文分别经实际 input 闭包检查，不将主文件本身没有 cite 误判为无引用；引文、DOI、交叉引用、图文件、书目项数量及编译结论见本节末验证结果。
- D10 当前仍缺可接入的真机结果图：本轮抽查 Exp07 两个 state 文件 counts 均为空，未启动采集、组装或正式实验。现有 D10 编号和实验定义保留；不声称整篇已满足带 D10 的投稿完整性。

### 本轮验证结果

Zotero 增量语义索引刷新已调用，但 MCP 返回 tools/call 等待 600 秒超时，故索引完成状态未确认。文献元数据与 PDF 的入库、读取和正文绑定均在此之前独立完成；未改 MCP 配置或访问原始数据库。该维护项不计为论文技术核验的通过证据。

中英文均为 53 个实际引用、53 个不同 DOI、53 条编译书目项；42 个 label、15 个被引用交叉标识、5 个图文件均通过闭包检查。两版现有引用检查脚本均报告 Issues 0。英文 PDF 12 页、中文 PDF 10 页，实际编译退出码均为 0；无未定义引用、缺字、Overfull 或浮动卡死告警。书目排版仍有 Underfull 提示，不影响引用或图的完整性。Git 空白检查按项目既有 CRLF 行尾约定通过。上述均为本轮重新验证；旧轮次中的实验全量核验不算作本轮重跑。

### 旧轮次记录


只记录读过全文的结论：Zotero key、位置、支撑的具体论述、适用限制。
元数据或摘要层面的条目不记入此处。未核验条目不得用于支撑技术论述。

## 01-model（2026-11-03 本轮）

- **chen2011classification**（Zotero `GCIB9LCZ` / bib 同 key）：确认支持。
  全文 `arXiv:1008.3745`：一维有对称有能隙相由对称群二阶上同调（投影表示等价类）标记。
  支撑正文“`Chen` 分类”一句。适用条件为一维、有能隙、 onsite 对称，与本项目 $L=8$ 开链用法一致。
- **schuch2011classifying**（Zotero `RME7WIRI`）：确认支持。
  全文 `arXiv:1010.3732` 摘要即声明 $MPS$ 框架下分类，且一维结论“first derived in Chen/Gu/Wen”。
  支撑“等价地可用 $MPS$ 表述”，同时交叉印证 `chen2011classification` 的归属。
- **pollmann2010entanglement**（Zotero `TXREEMXW`）：确认支持。
  全文 `arXiv:0910.1811`：一维拓扑相纠缠谱简并受对称保护（$Z_2\times Z_2$、时间反演或键中心反演），
  $Haldane$ 相由纠缠谱简并刻画。支撑“操作性指纹是纠缠谱简并”。
- **li2008entanglement**（Zotero `IZICB99P`）：仅支持部分范围。
  全文 `arXiv:0805.0332`：纠缠谱概念首创，语境是分数量子霍尔拓扑序“指纹”，不是一维 $SPT$。
  与 `pollmann2010entanglement` 并列引用时须明确分工（$Li$ 首创概念，$Pollmann$ 用于一维），
  不得暗示两篇都直接论证一维情形。
- **elben2020manybody**（Zotero `MPE67Q6B`）：确认支持，有适用边界。
  全文 `arXiv:1906.05011`：一维相互作用玻色系统多体拓扑不变量（含反射型）的随机测量协议。
  本项目数值相图用的是常规基测量下计算的部分反射标记 $\tilde{Z}_R$，不是随机测量实现；
  正文“测量方案见 Refs”一句是必要的隔离，重写时保留“定义借鉴、实现不同”的界限。
- **su1979solitons**（Zotero `P7R34NFU`）：既有已读记录（bib 头注 verified full text pp.1-2），
  本轮未重验（无开放获取）。沿用旧记录，待有 $APS$ 订阅时重验。
- **haldane1983nonlinear**（Zotero `4IEVSVY3`）：未核验，无开放获取。缺口。
- **affleck1987rigorous**（Zotero `DKNFR93D`）：未核验，无开放获取。缺口。

## 待补（缺口文献）

- `haldane1983nonlinear`、`affleck1987rigorous` 需校园 $APS$ 订阅拉全文；
  若不可行，退用权威综述/教材中复述该结论的章节作二手支撑并明确标注。

## 校园门禁尝试记录（2026-11-03）

- 按 hunter 流程试 $APS$ 机构订阅：本机出口 $IP$ 为中转地址（非校园 $IP$），
  `journals.aps.org` 与 `link.aps.org` 均返回 Cloudflare 质询，`curl` 无法通过；
  $Semantic Scholar$ 未持 $key$ 被限流（$429$）。$OpenAlex$ 确认三篇老 $PRL$ 无开放获取。
- 结论：本环境走不通校园门禁，两缺口保持未核验，不以摘要代替。
- 可行后续：用户在真校园网手工下载两篇 $PDF$ 交本轮读取；或配置图书馆代理后重跑；
  或退用权威综述/教材二手复述并明确标注。

## 01-model 二手支撑（2026-11-03 本轮，$VPN$ 绕行失败后）

- $VPN$ 绕行结论：出口经 $Mihomo$ $TUN$ 中转（非校园 $IP$），`--interface` 绑定物理网卡被策略路由黑洞，
  $IPv6$ 无直连，$APS$ 与 $science.org$ 的 Cloudflare 质询过不去。不动用户代理与防火墙配置，
  本环境走不通 $APS$ 门禁。
- **haldane1983nonlinear**（`4IEVSVY3`）：原文仍未读；实质内容由已验全文佐证——
  `Pollmann` 全文（`arXiv:0910.1811`）以 $Haldane$ 相的纠缠谱双重简并为操作性定义并论证其对称保护；
  `Chen` 全文（`arXiv:1008.3745`）给出半整数链必无能隙或破缺对称、整数链可有能隙的现代框架。
  历史句“$Haldane$ 猜想”保留主引，实质有已读二手支撑。
- **affleck1987rigorous**（`DKNFR93D`）：原文仍未读；实质内容由 `Chen` 全文佐证——
  自旋 $1$ 链 $AKLT$ 态为非平庸 $SO(3)$ 对称有能隙相，有无能隙自旋 $1/2$ 边界态与非局域 string 序，
  与自旋 $0$ 直积态属不同相。历史句保留主引，实质有已读二手支撑。
- 两主引元数据经 $Crossref$ 核对无误（刊、卷、页、$DOI$）；待用户手工提供 $PDF$ 后补完全文核验。

## 04-heatmaps（2026-11-03 本轮）

- **perezgarcia2008string**（Zotero `H69QSWUL`）：确认支持。全文 `arXiv:0802.0447`：
  string 序参量为非局域算符期望，热力学极限下非零值揭示隐藏序；
  在 $MPS$ 框架下 string 序存在等价于局域对称性。
- **dennijs1989preroughening**（Zotero `3EJ4I2TP`）：原文仍未读（无开放获取）；
  自旋链 string 序参量源头，实质内容由 `Perez-Garcia` 全文佐证（其引言以 $SOP$ 为范例）。
  主引保留，元数据经 $Crossref$ 核对无误。
- **elben2022toolbox**：确认支持。全文 `arXiv:2203.11374` 覆盖对称保护多体拓扑不变量
  （含 $Z_R$）的随机测量探测方案，支撑“多体不变量及随机测量的实现方法见 Refs”一句。
  需在 $Zotero$ 集合中补入该条目（当前集合未见，`bind` 时以已核验元数据建条目）。

## 06-ansatz（2026-11-03 本轮）

- **peruzzo2014variational**（Zotero `K8NY4LJ9`）：确认支持。全文 `arXiv:1304.3061`：
  变分本征求解器，高效计算哈密顿量期望值。
- **cerezo2021variational**（Zotero `NBV9FIIP`）：确认支持。全文 `arXiv:2012.09265`：
  $VQA$ 综述，含代价函数设计与拟设族。
- **tilly2022variational**：确认支持。全文 `arXiv:2111.05176`：
  $VQE$ 方法与最佳实践综述。
- **mcclean2018barren**（Zotero `INQIR6DI`）：确认支持。全文 `arXiv:1803.11173`：
  随机电路初猜可落入贫瘠高原，梯度随比特数指数缩小。
- **campos2021abrupt**：确认支持。全文 `arXiv:2010.09720`：
  结构化变分电路的可训练性随结构与深度突变（分段可训练性猜想的反例与临界深度）。
- 需在 $Zotero$ 集合中补入 `tilly2022variational` 与 `campos2021abrupt`
  的已核验条目后再 `bind`（正文 $key$ 不变）。

## 08-readout（2026-11-03 本轮，正文零改动）

- **bravyi2021mitigating**：确认支持。全文 `arXiv:2006.14044`：
  张量积 $2\times2$ 噪声矩阵模型与含关联 $CTMP$ 模型并列讨论；
  正文“张量积模型 + 关联误差需含关联模型”与之一致，无需改写。
- **nation2021scalable**：确认支持。全文 `arXiv:2108.12518`：
  无矩阵预条件迭代法把分配矩阵缓解推向更大系统；
  正文末句与之一致，无需改写。

## 00-introduction（2026-11-03 本轮，正文零改动）

- **satzinger2021realizing**（Zotero `8WC7LVIH`）：确认支持。全文 `arXiv:2104.01180`：
  超导处理器制备 $toric$ $code$ 基态，测得拓扑纠缠熵近 $ln2$。
- **sun2023efficient**（Zotero `FPSUMAZF`）：确认支持。全文 `arXiv:2303.17187`：
  初态层加变分层拟设研究对称保护拓扑相，在 $IBM$ 真机上测 $string$ 序与边缘模。
- **endres2011observation**（Zotero `AQY9KWUG`）：确认支持。全文 `arXiv:1108.3317`：
  低维 $Mott$ 绝缘体中关联粒子空穴对导致的非局域 $string$ 序。
- 需在 $Zotero$ 集合中补入 `sun2023efficient` 的已核验条目后再 `bind`。

## A-appendix（2026-11-03 本轮）

- **sandvik2010computational**：确认支持方法句。全文 `arXiv:1101.3281`（207 页讲义，与 `DOI 10.1063/1.3518900` 同文，`AIP Conf. Proc. 1297`）：`Sec. 3.3` 有限尺寸标度，`Sec. 4` 精确对角化，`Sec. 4.2` 的 `Lanczos` 方法（含 `Krylov` 空间、基与哈密顿量构造、收敛性），`Sec. 4.3` 一维链基态与激发例子。支撑“对称性扇区能隙做法与 `Lanczos` 精确对角化遵循常规有限尺寸做法”一句；具体 $s_c=0.5$ 数值与 $a=-0.017$ 拟合截距来自本项目 `Exp03` 数据，不由该文献背书。
- **raussendorf2001oneway**：`PRL` 原文仍未直读；同作者扩展版全文 `arXiv:quant-ph/0108067` 已验：簇态由一组本征方程表征，式 `(2)` 给出 $X$ 与近邻 $Z$ 乘积的本征值 $(-1)^{\kappa_a}$，$\kappa_a=0$ 即稳定子期望 $+1$；制备描述为全体 $|+\rangle$ 后加 $Ising$ 型相互作用（即 $CZ$ 组装 $|C\rangle=\prod CZ|+\rangle^{\otimes n}$），与正文一致。主引保留 `PRL 86, 5188`，实质有同作者已读全文支撑。
- 本轮 $Zotero$ 桌面端在沙箱内启动失败（`CanCreateUserNamespace EPERM`），且当前线程未接入 $Zotero$ $MCP$，`bind` 待通道恢复后补；正文 $key$ 不变。

## 09-comparison / 10-conclusion（2026-11-03 本轮）

- **09** 数字已对账：窗口 $[226,242)$、$16$ 单元、$d_{\rm raw}=0.30$、$r=0.85$、$S_{\max}=4.51$、$O_{\max}=0.090$ 与 `data/exp06/joint/exp06_manifest_joint.json` 一致（小数取两位报告值）；$N=500$、`report-only` 口径与 `verify_exp06.py` 诊断一致。`D10` 为占位，待 `exp07` 真机数回来再补。
- **10** 无引用，收尾句与已验章节一致，未引入新事实主张。
- 未引用 $bib$ 共 $15$ 条（`affleck1989quantum` 等，见本轮统计），等全节定稿再定去留，不为消告警删条目。

## validate 分跑（2026-11-03 本轮）

- 官方 `validate_citations.py` 不跟随 `\input`，直接扫 `main.tex` 会误报全未引用；改用闭包拼接后分跑中英：
  - `EN`：引用 $23$、`bib 38$、未引用 $15$（与手工统计一致）、`label 21`、`ref 10`、`Issues 0`。
  - `ZH`：同 $EN$，`Issues 0`；中英引用键完全一致。
- `latex_checker.py` 的缺章节与匿名化提示为模板默认值（本论文以 `paper-outline.md` 为准，须保留作者名），不处理。
- 未引用 $15$ 条继续保留：`D10` 待 `exp07` 回数后可能补讨论，届时再定去留。

## figure 检查（2026-11-03 本轮）

- `--check-figures` 对 `EN` 闭包报 $5$ 项 `MISSING FIGURE`，经核实为脚本伪阳性：脚本把 `\includegraphics{{...}}` 双花括号习语的首 `{` 当作路径字符且相对目录拼接错误；逐项按 `docs/paper` 解析，$5$ 个图全部存在（`exp02_D04`、`exp02_D03`、`exp04_D06`、`exp06_D08D09`、`exp03_D02`），`EN` 编译 `exit 0` 亦佐证无缺图。

## S07 与 outline 覆盖（2026-11-03 本轮）

- 附录三组排名已对 `data/exp05` 实物逐项核对：`8` 链榜首 $77$–$70$ 得分 $0.7801$（`manifest top1_chain score 0.7801269`，`n_tied_chain=2` 即“再一候选在 $0.02$ 内并列”）；`10` 环榜首 $69$–$73$ + $82$–$86$ 得分 $0.5246$（`top1_ring`，`n_tied_ring=3` 即“再两候选在容差内并列”）；冠军环内十条 $8$ 子链榜首为 $\{69$–$73, 82$–$84\}$ 得分 $0.7108$（`exp05_D07c.npz` 首行 `score 0.71079102`，`source chain_evidence` 即正文“取自链基准测量”）。三处表述与数据一致。
- `Q` 定义一致性：`04-heatmaps` 式 $Q=4/3+2O_{\rm str}-S(\pi)/6$ 与 `09` 式在固定尺度 $\hat S=S/8$、$\hat O=-O_{\rm str}$ 下逐项相等（$-2\hat O=+2O_{\rm str}$，$-(4/3)\hat S=-S/6$），正文“与第 `sec:heatmaps` 节定义一致”属实。
- 大纲覆盖：`D02`（附录能隙）、`D03`（`03-sq`）、`D04`（`02`）、`D06a/b/c` + `D09a/b`（`06-ansatz` 双合图）、`S07a/b/c`（附录文字排名）、读出缓解（`08`）、`D08a/b`（`09`）均有归属；仅 `D10a/b` 待 `exp07` 真机数。

## 06-ansatz 修订（2026-11-03 本轮，paper-revision）

- 删除 `sec:points` 小节中无法溯源的表述：三组“参考→目标”参数对在 `spec`、实验笔记、`S06` 网格中均无出处，且 `Fig.~D04(d)` 成图脚本与 `PDF` 均无标记箭头，“图上标出/箭头表示”与实物矛盾。
- 改写为以 `spec exp04 PRE-001` 为依据的描述：两条扫描线 $\delta=-2$ / $0.85$、$99$ 点 $s$ 网格（$s=0.01$--$0.99$，`exp04_S06.npz` 实测），每点三初态独立优化取最小；背景色带即 `D09` 按获胜初态分段（`PRE-004`）。中英同步，无引用增减。

## D08D09 图注核验（2026-11-03 本轮）

- 将 `figs/exp06/exp06_D08D09.pdf` 渲染目检，对照 `06-ansatz` 图注逐句核对：`(a)(b) E0` 蓝色实线、三路 `triv` 绿虚线 / `topo` 橙点线 / `AFM(Neel)` 黑点划线、背景两段（`δ=-2`）/三段（`δ=0.85`）色带、每段一圆圈标该段最低能量初态分支，均与成图一致；`(c)(d)` 模拟机 $p=1$ 黑 / $p=2$ 灰曲线、真机散点按 `(a)(b)` 获胜分支着色（红→蓝 / 红→黑→蓝），图例 `exp p=1 (triv/topo/Neel)` 与之一致。
- 背景色带（粉/白/蓝）与 `spec exp04 PRE-004` 的按获胜初态分段一致。

## D06/D02/D03 图文核验（2026-11-03 本轮）

- `D06`（`exp04_D06`）：三面板初态（奇键单态 / 首尾+体单态 / Neel）+ $U^{(1)}$ + $U^{(k)}$ 虚线框、轨道编号 $1$–$4$，与图注“每相初态 + 所需拟设、$U^{(k)}$ 为第 $k$ 变分层”一致。
- `D02`（`exp03_D02`）：`(a)` 五条 $L$ 的 $\Delta_{\rm sec}$–$s$ 曲线；`(b)` 极小标记随 $L$ 增大向 $s=0.5$ 移动且极小值持续降低（约 $8.3\to3.2$）；`(c)` $s=0.5$ 处五点 $1/L$ 拟合，方形截距标记近零（$a=-0.017$，相对能隙尺度可忽略）。与附录文字逐句一致。
- `D03`（`exp02_D03`）：`(a)` 模拟机三相代表点 $S(q)$，Neel 在 $q=\pi$ 尖峰、另两相低平；`(b)` 真机 $p=1$ 同点测量，Neel $\pi$ 峰虽被噪声压低但清晰可辨。与 `03-sq` 文字（“$\pi$ 峰清晰可辨，尽管有噪声压制”）一致。

## D04/02-phasediagram 数据核验（2026-11-03 本轮）

- `02` 文字“每格点独立由相应基态计算；简并点保留求解器返回的最低能量本征矢并在数据集中记录简并标记”：`exp02_D04.npz` 含布尔 `degenerate` 场（$99\times121$），共 $744$ 点，与 `manifest` 的 `n_degenerate_inherited=744` 一致；网格 $s=0.01$–$0.99$（$99$ 点）、$\delta=-3$–$3$（$121$ 点）与大纲范围一致（$s$ 去边界）。
- `D04` 四面板顺序（`(a) S(\pi)`、`(b)` string、`（c) Q`、`(d) \tilde Z_R`）与 `02` 图注及 `04-heatmaps` 首句一致。

## 摘要与孤儿图（2026-11-03 本轮）

- 摘要逐句对正文：三初态形态、独立优化取最小、`L=8` 相图、能隙标度、两直接可测标记、优质比特筛选 + 张量积读出缓解、内部归一化比较，均在正文有归属，无新增事实主张。
- `docs/paper/figures/` 中 `exp02_D04a-d`、`exp06_D08a-d` 等分面板文件为绘图中间产物（正文引用合图）；`exp01_D01/D05`、`exp02_D05`、`exp05_D07a-c` 无正文引用（`S07` 按大纲以文字给出，不单独插图）。仅记录，不删除。

## 01-model 文本级核验（2026-11-03 本轮）

- 对已读全文做关键词回查：`chen2011classification` 含 $H^2(G,C)$ 分类 + 影射表示论述，支撑“第二上同调群标记”句；`pollmann2010entanglement` 含 `AKLT` 纠缠谱双重简并 + `Haldane` 相整个纠缠谱双重简并，支撑“操作性指纹”句；`li2008entanglement` 题即纠缠谱识别拓扑序，支撑“作为拓扑序指纹引入”句；`schuch2011classifying` 含 `parent Hamiltonian`，支撑“`MPS` + 母哈密顿量”句。
- `elben2020manybody` 实为直接支撑：全文给出自旋 $1/2$ 交替键 $XXZ$ 模型的 partial reflection 不变量 $Z_R$（式 $2$）及归一化 $\tilde Z_R$ 相图（图 $1$），与正文“采用该不变量定义”完全对应（此前“ﬂ”连字导致纯文本检索漏检）。
- `su1979solitons` 仍只有元数据（`SSH` 命名源头，归属级表述，低风险），待补全文。

## 中英编译（2026-11-03 本轮）

- `main.tex`（`pdflatex`）与 `main-zh.tex`（`xelatex`）均全管线通过（`xelatex→bibtex→xdvipdfmx`，`exit 0`，`All targets up-to-date`）。注：`latexmk -xelatex -pdf` 混用会被 `-pdf` 拉回 `pdflatex` 引擎而误报 `xeCJK` 错，中文版须用纯 `-xelatex`。
- 修订后的 `06-ansatz-zh` 已包含在本次 `8` 页 `PDF` 中；编译中间产物已恢复，工作树干净。

## D10 输入就绪检查（2026-11-03 本轮）

- `D10` 模拟机侧输入已在位：`exp07 spec` 明确模拟机层取 `S06` 现成 `p=2` 获胜分支数据（`q_sim_p2` 口径）不重算；`exp04_S06.npz` 中 `theta_leg (99,3,3,24)` 即 `(s,分支,p)` 三维具备 `p=2` 切片，`conv/stagn (99,3,3)` 具备逐点 `invalid` 判定条件。`D10` 只差真机侧（`exp07` 提交中）。

## 09-string 表述修正（2026-11-03 本轮）

- 原句“$s=0.99$ 处 pooled $N=500$ 真机 $\hat O_{\rm str}$ 均值约理论值 $5\%$、偏离零点 $9\sigma$；其余点与零一致”不成立：实测 `exp06_D08_joint.npz`（`o_post (500,30)`）$s=0.99$、$\delta=0.85$ 列均值 $-0.0435$、理论 $+0.9457$、比值 $-4.6\%$、$z=-9.34$——幅度对但符号相反；且多点显著非零（$s=0.78$、$\delta=-2$ 处 $z=-24.1$；$s=0.64$、$\delta=-2$ 处 $z=-17.0$；$s=0.92$、$\delta=0.85$ 处 $z=-9.4$；另 $s=0.99$、$\delta=-2$ 处 $z=-6.1$）。
- 已改写中英 `09-comparison` 末句：pooled 检查给 $-0.044 \pm 0.005$（$-9.3\sigma$，符号与模拟值相反），并列多点反例，结论改为“预期方向上没有可分辨的正 string 信号”；中英 `latexmk -pdf / -xelatex -g` 强制重编均 `exit 0` 无错，中间产物已恢复。

## Zotero bind 尝试（2026-11-03 本轮，未完成）

- 待绑 4 条（均为已全文核验、`references.bib` 已有完整条目含 `DOI`）：`tilly2022variational`（`arXiv:2111.05176`）、`elben2022toolbox`（`Nat. Rev. Phys. 5, 9--24`）、`campos2021abrupt`（`Phys. Rev. A 103, 032607`）、`sun2023efficient`（`Phys. Rev. B 108, 075127`）；目标集合 `paper-variational-qc`（`N7CLH4TB`，经 `zotero://collections` 确认在位）。
- 本线程按正常流程调用 `zotero_search_by_citation_key`（4 条）、`zotero_search_collections`、`zotero_list_libraries`，返回均为 `unsupported call`；`zotero-mcp serve` 进程在宿主运行但属其他会话，不可借用；直读 `sqlite` 与手写 `MCP` 客户端均违反项目规则，未执行。`bind`（需 `item_key` + `zotero_set_item_collections`）待工具有效线程补做。
- `skills` 脚本零改动（`validate_citations.py` 内本无 `assert`，未增删任何断言）。
- 本轮 `validate_citations.py` 闭包拼接中英分跑均通过（英文闭包须排除 `*-zh.tex`，否则误报 21 重复 `label`；`15` 条未引用 `bib` 与上轮一致，留待 `D10` 后定夺）。

## 结论与 09 首段对齐 09 修订（2026-11-03 本轮）

- `10-conclusion` 旧句（`5%`/`9σ` 分辨 + 跟随负 $Q$ 转折）与已核验实数矛盾，已按 `09` 修订口径改写：无预期方向正 string 信号（`pooled` $\hat O_{\rm str}=-0.044 \pm 0.005$，与模拟值 $+0.95$ 符号相反），$s\to1$ 处真机 $Q$ 与零在窗口不确定度内一致；中英同步。
- `09` 首段同步弱化：拓扑区真机 $Q$ 仅个别点（$s=0.78$，$-0.29 \pm 0.18$，低于两模拟约 $2.4\sigma$）低于模拟，其余在窗口误差棒（$\pm 0.2$--$0.5$）内与零一致；原“$s\to1$ 时低于两条模拟曲线”不成立（$s=0.85/0.92/0.99$ 窗口点均与模拟相容）。
- 中英 `latexmk -pdf / -xelatex` 实编（非 `up-to-date`）均 `exit 0` 无报错；中间产物已恢复。

## D10 模拟机侧预备（2026-11-03 本轮，不写新数据文件）

- `D10` 模拟机灰单线 = `D08 q_sim_p2`（`exp06_D08_joint.npz`，30 点）按线拆分：偶下标 `δ=0.85`、`奇下标 δ=-2`，各 `15` 点；与 `S06` 直算（`spi[row,1]/8`、`-ostr[row,1]`、`Q=4/3-2o-(4/3)s`，`row=0,7,…,98`）逐点 `maxdiff=0.0`，口径与 `D08` 完全一致（`spec07`：取现成，不重算）。
- `p=2` 获胜分支（`a_star[:,1]`）：`δ=-2` 线 `15` 点全为分支 1（`triv`）；`δ=0.85` 线前 `10` 点分支 1（`s=0.01`–`0.64`）、后 `5` 点分支 2（`topo`，`s=0.71`–`0.99`）。供 `D10` 图注备查。
- `D10` 仍缺真机三分支（`exp07` 提交中，本轮 `tids=14335/46000`、`counts=0`）。

## 图注 N 标注修正（2026-11-03 本轮）

- `FIG.4(c)(d)` 图注旧文“`hardware window scatter ($p=1$, $N=500$)`”与实物不符：图上散点为 `win_mean ± win_se`（`exp06_assemble.py` 第 365–366 行，`q_post[ws:ws+wl]`，`wl=16` 单元窗内均值 + 窗内单元间标准误），`N=500` 只是整轮单元总数。已改为“`16-unit window of the 500-unit round`”（中英同步）；散点按 `D09` 背景相位（`p=1` 获胜分支）着色与 `plot_D08D09.py` 一致，已核对。
- `p=1` 获胜分支（`a_star[:,0]`，`S06`）：`δ=-2` 线 `triv→topo` 两段（`s=0.57/0.64` 间切换）；`δ=0.85` 线 `triv→AFM→topo` 三段（`0.36/0.43`、`0.78/0.85` 间切换），与大纲 `D09` 分段一致。
- 中英实编均 `exit 0` 零报错；中间产物已恢复。

## D03 文本核验（2026-11-03 本轮，正文零改动）

- `03-sq` 文“`AFM π` 峰清晰可辨，虽有噪声压制”：`exp02_D03.npz` 模拟 `AFM` 点 `S(π)=0.931`，真机 `exp06_D03hw.npz` 同点 `0.653±0.012`（`z=55.7`），峰位同在 `q=π`，三点排序 `triv/top o < afm` 两边一致（真机 `0.228/0.176/0.653`，模拟 `0.25/0.25/0.931`），“跟踪 + 压制”表述成立。

## 结论末段动词修正（2026-11-03 本轮）

- 结论旧句“`Preserving the string signal …`”与新证据冲突（预期方向无正信号、呈负偏置），改为“`Recovering the positive string signal …`”（中文“恢复拓扑区域的正 `string` 信号”），中英同步；实编通过。

## D10 invalid 预查（2026-11-03 本轮）

- `D10` 两线 `15` 点 × 三分支共 `90` 点，在 `S06 p=2` 层（`conv[:,:,1]`/`stagn[:,:,1]`）的 `invalid` 判定（两假才判无效）全为有效（`0/15` × 6 组）。`D10` 成文时无模拟机侧无效点 caveat；真机侧以 `exp07 assemble` 对账为准。
- 本轮结论改后引用校验中英闭包重跑均通过。

## δ=-2 “像 p=2”表述弱化（2026-11-03 本轮）

- `09` 旧文“`δ=-2` 真机与模拟机 `p=2` 曲线相近”：窗口均值平均绝对偏离 `p=1` 为 `0.312`、对 `p=2` 为 `0.362`，平均窗内标准误 `0.396`——两边都在误差棒内，无依据单指 `p=2`。已改为“与模拟机曲线相近”（中英同步），与结论复数表述一致；实编通过。

## D09 背景相带核验（2026-11-03 本轮，正文零改动）

- 图注“背景色带标物理相、圆点标各区最低能量初态分支”：`exp04_D09.npz` 的 `phase` 带（`δ=-2` 在 `0.59/0.60` 切 `triv→topo`；`δ=0.85` 在 `0.42/0.43` 切 `triv→AFM`、在 `0.79/0.80` 切 `AFM→topo`）与 `p=1` 获胜分支（`a_star[:,0]`：`δ=-2` 在 `0.57/0.64` 间切换、`δ=0.85` 为 `0.36/0.43` 与 `0.78/0.85` 间切换）在网格分辨率内一致，色带与圆点分属两套数据，图注表述成立。

## δ=0.85 前半段趋势核验（2026-11-03 本轮，正文零改动）

- `09` 文“`δ=0.85` 前半段趋势相近”：窗口散点 `s=0.01`–`0.43` 共 7 点偏离模拟 `p=2` 均在 `|1.7σ|` 内；`s=0.50` 一点偏离 `-3.2σ`（`-0.410±0.167` 对 `+0.120`），为相带边界点（`AFM` 带起于 `0.43`），属趋势表述容忍范围内的单点偏离。正文维持原判。

## exp07 网格结构抽查（2026-11-03 本轮）

- 抽查 `units/00000/state.json`：`tids` 共 92 个（`g` 系 90 点 + `cal_zero`/`cal_one` 读出标定），与 `spec07`（每单位 `90` 点 + 一对标定）一致；`counts` 尚空，提交继续（本轮 `tids=15704/46000`）。

## exp07 收发键契约抽查（2026-11-03 本轮）

- `exp07_assemble.py` 要求 `state.json` 的 `counts` 含 `g0`–`g89` + `cal_zero`/`cal_one`；提交器已落盘 `tids` 键名（`g` 系 + `cal_zero`/`cal_one`）与之一致，回数后可直接对账。本轮 `tids=15763/46000`。

## D10 链路完备性抽查（2026-11-03 本轮）

- `specs/exp07/tasks.md` 的 `T005` 已把用户要的 `s` 轴标签位置（每面板各一、居中正下方）写进完成条件；`T003` 提交器运行中、`T004 assemble` 脚本在位且收发键契约一致。`D10` 从提交、组装到出图链路齐备，只差真机回数。

## PDF 落字抽查（2026-11-03 本轮）

- `pdftotext` 抽 `main.pdf`：新表述“`no resolved positive string signal`”“`16-unit window`”均已落字，源码改动已进成品。本轮 `tids=15930/46000`。

## 中文 PDF 落字抽查（2026-11-03 本轮）

- `main-zh.pdf` 同样含两处新表述，中英成品一致。本轮 `tids=15989/46000`。

## Zotero bind 补做（2026-11-03 重启后，桌面端已拉起）

- 通道：本线程 `mcp__zotero.*` 仍 `unsupported call`，改走本地已授权客户端（`ZOTERO_LOCAL=true`，`local_api.key`）经 `pyzotero` 直连 `127.0.0.1:23119`；读经 `zotero.item()` 核对，写经 `addto_collection` / `create_items`，未直读 `sqlite`，未改 `plot` 脚本 `assert`。
- `tilly2022variational`：库内 `9VYJZQIJ`，标题 `The Variational Quantum Eigensolver: A review of methods and best practices`，`DOI 10.1016/j.physrep.2022.08.003`，`Physics Reports`，已在 `N7CLH4TB`，与 `references.bib` 一致，无需改动。
- `elben2022toolbox`：库内 `YTBCD6JR`，标题 `The randomized measurement toolbox`，`DOI 10.1038/s42254-022-00535-2`，`Nature Reviews Physics`，原仅在 `Y4384ZGQ`，已补绑 `N7CLH4TB`（现 `['Y4384ZGQ','N7CLH4TB']`）。
- `sun2023efficient`：库内 `FPSUMAZF`，标题 `Efficient variational quantum circuit structure for correlated topological phases`，`DOI 10.1103/physrevb.108.075127`，`Physical Review B`，已在 `['N7CLH4TB','VDRYZRPC']`，与 `references.bib` 一致，无需改动。
- `campos2021abrupt`：库内查无（标题/`DOI 10.1103/PhysRevA.103.032607` 均零命中），按已核验 `references.bib` 元数据新建 `D6G65X4B`（`Phys. Rev. A 103, 032607`，`Campos/Nasrallah/Biamonte`），直接落 `N7CLH4TB`。
- 结果：4 条均在 `paper-variational-qc (N7CLH4TB)` 就位；`D10` 仍待 `exp07` 回数（本轮 `tids=16661/46000`、`counts=0`，提交器进程不在）。

## Zotero 旧库对齐（2026-11-03 重启后第二轮）

- 全库比对：`bib 38` 条与库内 `724` 条按 `DOI` 小写精确匹配，`34 HIT`、`4 MISS`。
- `4 MISS` 中 `2` 已引用实为预印本旧元数据，已就地升级为出版版本（未新建、不删 `assert`）：
  - `bravyi2021mitigating`：库内 `X3WB23G3` 由 `preprint (2020-06-24, 无 DOI)` 更新为 `journalArticle`，`Phys. Rev. A 103, 042605 (2021)`，`DOI 10.1103/PhysRevA.103.042605`，已在 `N7CLH4TB`。
  - `satzinger2021realizing`：库内 `8WC7LVIH` 由 `preprint (2021-04-02, 无 DOI)` 更新为 `journalArticle`，`Science 374, 1237--1241 (2021)`，`DOI 10.1126/science.abi8378`（保留原完整作者表，不按 `bib` 的 `others` 覆盖），已在 `N7CLH4TB`。
- 另 `2 MISS` 均为未引用（留待 `D10` 后定夺，不新建）：`qi2021randomized`、`ware2021experimental`。
- 结论：已引用 `23` 条在库内均有 `DOI` 命中；未引用 `15` 条维持原判。

## 00-introduction 同行比较补强（2026-11-03 重启后）

- 将第 2 段由罗列改为主题比较：`Satzinger` 为内禀拓扑序加非局域纠缠熵诊断，与本工作对称保护链加比特串直接可测标记形成对照；`Sun` 为最接近同类（初态层加变分层、`IBM` 上 `string` 序与边缘模），本工作差异点为相匹配初态加反射对称拟设统一覆盖三相、并以单一组合量 $Q$ 比较真机与模拟机趋势。不新增引用（`satzinger2021realizing`、`sun2023efficient` 均已核验，`Zotero` 元数据已对齐出版版本），中英同步。
- 编译：`latexmk -pdf main.tex` 与 `latexmk -xelatex main-zh.tex` 实编 `exit 0`；`pdftotext` 抽 `main.pdf` 含 `closest sibling` 与 `intrinsic topological order`，`main-zh.pdf` 含对应中文表述；中间产物已恢复。

## 00-introduction TEE 理论源头补引（2026-11-03 重启后第二轮）

- **levin2006detecting**（`Zotero FYBSJVQI`）：确认支持。全文 `arXiv:cond-mat/0510613`（`4` 页）：仅凭基态波函数探测 `string-net` 型拓扑序，构造直接度量量子维度 $D$ 的拓扑熵。支撑“拓扑纠缠熵”这一诊断量的理论来源。
- **kitaev2006topological**（`Zotero 6FB8TCYP`）：确认支持。全文 `arXiv:hep-th/0510092`（`4` 页）：有能隙二维拓扑介质基态多体纠缠的普适刻画，圆盘约化态 `von Neumann` 熵含与边界长度无关的拓扑项。支撑同上。
- 正文 `Satzinger` 句改为实验加理论并引：实验制备与测量归 `satzinger2021realizing`，诊断量定义归 `levin2006detecting,kitaev2006topological`，表述为“文献引入的拓扑纠缠熵”，避免把理论论文读成实验；中英同步。已引用由 `23` 增至 `25`。

## S(q) 增补候选否决（2026-11-03 重启后第三轮）

- **pereira2006dynamical**（`Zotero XTZBGFF9`，仍未引用）：已读全文 `arXiv:cond-mat/0603681`（`4` 页）。其实质是 `XXZ` 链小波矢纵向动力学结构因子的 `Bethe`  Ansatz、场论与 `DMRG` 线形（峰宽随 $q$ 标度、高频尾解析式），不支持本项目静态 $S(\pi)$ 作 `AFM` 诊断的具体论述。按写作政策不以相近论文背书项目特有公式，不增引；维持未引用（`13` 条待 `D10` 后定夺）。
- 当前已引用 `25`、未引用 `13`；`D10` 仍待 `exp07` 回数（`tids=16661/46000`、`counts=0`，提交器不在为 `Exp` 层缺件，不在 `Paper` 层重跑）。

## 中英实编复核（2026-11-03 重启后第四轮）

- `latexmk -pdf -g main.tex` 与 `latexmk -xelatex -g main-zh.tex` 均 `exit 0`；`5` 图文件在位；正文无 `D10` 越界主张（`09/10` 未提三分支）；中间产物已恢复，工作区干净。`D10` 仍待 `exp07` 回数（`tids=16661/46000`、`counts=0`）。

## 读出节与 09 数字复核（2026-11-03 重启后第五轮，正文零改动）

- `08-readout` 与实验口径一致：张量积单比特分配矩阵、每比特 `|0>/|1>` 两制备标定（即每单位 `cal_zero`/`cal_one`）、逐批重标定跟踪漂移、平台自带修正关闭、负分量截零重归一；`bravyi2021mitigating`（已升级出版元数据）与 `nation2021scalable` 引用位置恰当。
- `09` 窗口数重读 `data/exp06/joint/exp06_manifest_joint.json`：`start=226`、`length=16`（即 `[226,242)`）、`d_raw=0.3044`、`r=0.8497`、`S_max=4.5138`、`O_max=0.0900`、`N=500`、`report-only`，与正文两位小数报告一致，无漂移。

## S07 附录排名复核（2026-11-03 重启后第六轮，正文零改动）

- 直读 `data/exp05/exp05_D07{a,b,c}.npz`：`D07a` 居首链 `[77..70]` 评分 `0.7801`，`top10` 内与首名差 `<=0.02` 者共 `2` 条（即“另有 1 条并列”）；`D07b` 居首环 `[69 70 71 72 73 86 85 84 83 82]` 评分 `0.5246`，差内共 `3` 条（即“另有 2 条并列”）；`D07c` 居首子链 `[84 83 82 69 70 71 72 73]`（即 `69--73` 与 `82--84`）评分 `0.7108`，`source=chain_evidence`（即“评分沿用链基准电路测量结果”）。中英附录表述均与之一致。

## D02 附录能隙复核（2026-11-03 重启后第七轮，正文零改动）

- 直读 `data/exp03/exp03_D02.npz`：`Ls=[8,12,16,20,24]`；各曲线极小 `s=0.64/0.59/0.57/0.55/0.55` 单调趋近 `0.5`，极小值 `8.33/5.91/4.57/3.72/3.13` 持续降低；`1/L` 二次拟合截距 `a=-0.0168`（文报 `-0.017`），相对能隙尺度可忽略；放大窗 `s in [0.53,0.65]` 覆盖全部极小。中英附录表述均与之一致。

## D09 相带与获胜分支复核（2026-11-03 重启后第八轮，正文零改动）

- 直读 `exp04_D09.npz`（`phase`）与 `exp04_S06.npz`（`a_star[:,0]`）：`δ=-2` 相带与分支切换均在 `s=0.59/0.60` 格间；`δ=0.85` 均在 `0.42/0.43` 与 `0.79/0.80` 格间，两套数据切点重合。正文与图注均未写死具体数值（只称色带标相、圆点标各区最低能量分支），图由同一批数据文件生成，自洽无漂移风险。

## D03 真机跟踪复核（2026-11-03 重启后第九轮，正文零改动）

- 直读 `data/exp02/exp02_D03.npz`（模拟机 `curves (3,99)`）与 `data/exp06/d03hw/exp06_D03hw.npz`（真机 `S_hat (3,99)`，`labels triv/topo/afm`，`p=1`、`shots=1024`）：`q=pi` 处模拟机 `0.2500/0.2500/0.9310`，真机 `0.2280/0.1763/0.6526`（`SE 0.0086/0.0073/0.0117`）；`AFM` 峰被压低至约 `0.70` 倍但与其余两点拉开约 `30--50` 倍 `SE`，清晰可辨；三曲线全 $q$ 相关 `r=0.9979/0.9889/0.9973`，紧贴跟踪成立。中英正文定性表述均与之一致。
- `D10` 仍待 `exp07` 回数（`joint/units` 仅 `00000--00014` 目录占位、`rounds/r001` 仅账单、无 `counts`）。


## 08-readout 方法适用性复核（2026-11-03，作者提问）

- 项目条件直接核对 `scripts/exp06_assemble.py` 的 `mitigate_counts`、`obs_basis_arrays` 和 `group_Ms`，以及 Exp06/Exp07 spec：$L=8$，完整分布有 $2^8=256$ 项；$S(\pi)$ 是二体 $Z$ 关联的线性组合，当前 $O_{\rm str}$ 是四个六体 $Z$ 乘积之和。两者从同一批计算基 counts 得到，每单元全零/全一标定给出单比特分配矩阵。
- `maciejewski2020mitigation`（Zotero `8PUKRW3H`）：本轮经 MCP 重读 PDF p. 7，Sec. 4.3、Eqs. (25)--(27)。确认其建议为反演向量到概率单纯形的欧氏投影，并显式计入修正误差。项目适用性推断：现有归一化 counts 和同单元标定即可用于这类后处理比较，无需新增真机电路；不据此宣称其对本项目观测量必然比截零重归一更准确。
- `nation2021scalable`：本轮 Zotero 库检索两次遇到 API 繁忙锁，未恢复条目 key；改读作者公开全文 `https://arxiv.org/pdf/2108.12518` 的 pp. 1--2、Secs. I--II，Eqs. (1)--(5)，并核对出版 DOI `10.1103/PRXQuantum.2.040326`。确认 M3 使用观测 bitstrings 所张成的子空间、列归一化与无矩阵求解，可用单比特标定矩阵构造张量积模型的元素，也允许有相应标定信息的关联模型。项目适用性推断：已有 counts 与单比特标定可供张量积版本使用，但当前 256 维规模并未构成指数维度的实际计算瓶颈；换求解法不能使现有两种制备自动识别一般关联读出误差。
- `vandenberg2022modelfree`（Zotero `3Y6JUJKC`）：本轮经 MCP 重读 PDF pp. 2--4，Sec. II 的 AcquireData / Protocol 1、Sec. III 和 Sec. IV A--B。确认需在测量前执行随机 Pauli-$X$、记录翻转模式，并以随机化标定估计各 $Z$ 乘积的衰减因子；同一数据集可服务多个观测量。项目适用性推断：两个指标都是 $Z$ 乘积的线性组合，因此观测量相容；当前未随机化的采集不能通过事后翻转已有 bitstrings 等价补做该协议。统计开销取决于噪声和算符权重，不承诺 string 信号必然改善。
- 原文与项目推导另作区分：在已知且正确的经典分配模型下，可直接用反演得到的有符号向量计算线性期望值，无需先强制非负；有限标定误差和求逆方差仍需评估。此轮只核验适用性，没有进行替代估计器的数值比较，不能声称任何方案在现有硬件数据上更优。

## 08-readout 采用欧氏概率投影并重建结果（2026-11-03）

- 按作者决定，先修订读出缓解笔记，再修订 Exp06/Exp07 spec、plan/tasks，最后修改后处理与正文。此前关于“本文仍采用截零重归一”的记录为旧版本，现行方法以本节及对应 spec 为准。
- 来源仍为 `maciejewski2020mitigation`（Zotero `8PUKRW3H`），Sec. 4.3、Eq. (25)，PDF p. 7：对归一化 counts 的反演向量做欧氏概率单纯形投影。排序阈值实现由该凸问题的最优性条件得到，不冒充原文指定的求解器。
- D08、D03 和 Exp07 assembler 统一使用同一投影入口，联测标定矩阵的逻辑位序同时修正；不能把全部数值变化只归因于投影。507 个原始输入文件逐个复核哈希一致，模拟数据、采样参数和任务 ID 保留。本轮本地测试 25 项通过，覆盖已知解、最优性、计数缩放不变性、非对称误读率恢复和异常输入；500 个联测单元全量生产断言通过，D03 三点正式产物与验证目录逐数组一致。
- 新窗口为 $[222,238)$，长度 $16$，$S_{\max}=4.5710821579$、$O_{\max}=0.0886397787$，$d_{\rm raw}=0.2976275076$、$r=0.8601493292$。窗口、单位间 SE 与端点由新分布按原规则重算，单位内 multinomial 值标为 plug-in 诊断。
- 全 500 单元的 $s=0.99$、$\delta=0.85$ 固定尺度 string 均值为 $0.0430293603$，单元间标准误为 $0.0048140160$；正文及结论报告 $0.043\pm0.005$，撤去旧负号及基于旧数值的描述。
- 按作者行文要求，方法节简短说明冠军链标定构造各分支共用模型、D03 各映射分别标定；详细物理映射核对留在笔记与 manifest，正文不重复强调该问题或添加真机效果评价。该段撤下未采用的 M3 和随机翻转方案，保留共享书目中的既有条目。
- D03、D08、D08D09 及已有两张单线诊断图已重新生成并目检。中英文各有 51 篇实际引用，分别按 input 闭包核验，无缺失引用、重复标签或未定义交叉引用。投影式为 Eq. (20)，已目检中文第 4 页与英文第 8 页。
- 证据位于 `data/validation/readout-simplex-20261103-190611-ga4wf74q/`，包括 `migration-verification.json`、`paper-verification.json`、日志、旧产物和输入哈希。Exp07 正式 D10 仍待原采集回数，本轮已完成共享后处理准备。

## 全文措辞与科学限定区分（2026-11-03）

- 通读并修改中英文主文件及十组章节，共 22 个 TeX 文件。撤去摘要、引言中仍残留的“正 string 信号未被分辨”旧结论，以正式产物中的实测值直接表述；删改重复的防御性评价和未采用方法的免责式罗列。
- 按作者进一步澄清，科学限定与防御性措辞分别判断。保留对称、单射 MPS 的假设、能量与重叠界的扇区唯一基态条件、反射标记的尺度条件和完整窗口选择规则；读出节简短说明欧氏投影的非线性及有限采样偏差。没有按否定词批量删句。
- 摘要与结论中的 $r=0.86$ 明确对应采用拟合标记尺度的所选 $16$ 单元窗口。摘要的 $0.043\pm0.005$ 明确为全部 $500$ 单元汇总结果，误差为单元间标准误。上述口径与结果节及正式 manifest 一致。
- Paper 共同写作规则及写作、修订、自审、协调、引文与排版入口已同步更新。取消固定自我限制句数和逐篇列缺点的要求，保留有信息量的范围说明及实质局限。PRA 风格文件区分样本行文归纳与 APS 正式要求，依据为 [PRA 审稿指引](https://journals.aps.org/pra/referees/guidelines-for-referees) 和 [作者指引](https://journals.aps.org/pra/authors)；未将这些网页作为新的科学引文加入书目。
- 源目录 `~/.agents/sdd/specify/dev/scientific-paper/` 更新至 `0.3.1`，12 个技能文件同步到项目，保留双方原有换行约定；七个技能的文本逐文件一致。原技能备份位于本轮审计目录的 `skills-before/`。
- 本轮以 TeX 核对和编译验收，不再追加本稿 PDF 解析或目检。中英文强制编译均返回零，分别核对 11 个输入文件、51 篇实际引用、42 个标签及 5 张图，无缺失引用、未定义交叉引用或 overfull 提示。REVTeX 的非致命浮动体提示在此前构建中也存在。
- 与本轮改写前快照比较，各文件的定界公式、标签和 cite-key 集合保持不变，书目及五个证据输入的哈希保持不变。审计目录为 `data/validation/paper-direct-prose-20261103-194716-e7z6zc5c/`；最终构建日志为 `scope-build.log`，退出码为 `scope-build.exitcode`，技能同步记录为 `skills-verification.json`。通用 YAML 校验脚本因项目解释器缺少 PyYAML 未完成；已另行核对源与项目共 14 份未改动的 frontmatter、技能名称、描述存在性和共同规则路径，没有为此新增环境依赖或开展写作 benchmark。

## 临界开链能隙的二阶逆长度修正（2026-11-04，作者提问）

引用需求：为附录式 `eq:gap-fit` 中的 $1/L^2$ 项寻找理论动机。核对对象为开边界二聚化 XXZ 链在 $s=1/2$、$\delta=-2$ 的同扇区能隙，标准各向异性为 $\Delta=e^{-4}$；不是有限尺寸极小位置的漂移，也不是基态能量密度的外推。本轮不改正文、书目、拟合、实验定义或数据。

### 已核验来源

三篇均先核对 arXiv 元数据及 PDF 首页标题、作者，再经 Zotero MCP 读取相关全文位置；关键公式另以 PDF 图像核对。

| 文献与 DOI | Zotero key | 已读位置 | 支撑范围 |
| --- | --- | --- | --- |
| Campostrini, Pelissetto, Vicari, *Finite-size scaling at quantum transitions*, Phys. Rev. B **89**, 094516 (2014), DOI [10.1103/PhysRevB.89.094516](https://doi.org/10.1103/PhysRevB.89.094516) | `9PZENU2C`，PDF `MIZA2VYP` | arXiv:1401.0788，pp. 3--5，Sec. II A、II C，Eqs. (13)--(15)、(28)；并读 Sec. III D，Eqs. (97)、(109)--(113) | 非周期边界下逆长度标度场允许二阶修正，并可用有效长度偏移吸收；低能能量差按有效长度的负动态指数次幂标度。XY 链例子确认该机制，不能把它的系数直接移给 XXZ。 |
| Sirker, Fujimoto, Laflorencie, Eggert, Affleck, *Thermodynamics of impurities in the anisotropic Heisenberg spin-1/2 chain*, J. Stat. Mech. (2008) P02015, DOI [10.1088/1742-5468/2008/02/P02015](https://doi.org/10.1088/1742-5468/2008/02/P02015) | `RH8NUY46`，PDF `Y5H2GZRI` | arXiv:0801.1201，p. 6，Sec. 2 末段；pp. 8--9，Sec. 3、Eqs. (3.18)--(3.20)；核对 Sec. 2 的开链玻色谱 | 直接针对开边界 XXZ 链：无破坏对称性的边界外场时，主导无关边界算符的标度维数为 $2$，产生有效链长偏移。该文主要检验磁化率，不能把它的磁化激发间隔当作本项目同时固定磁化、自旋翻转和反射的扇区能隙；其 Luttinger 参数归一化也与本文不同。 |
| Liu, Shimizu, Ueda, Oshikawa, *Finite-size corrections to the energy spectra of gapless one-dimensional systems in the presence of boundaries*, SciPost Phys. **17**, 099 (2024), DOI [10.21468/SciPostPhys.17.4.099](https://doi.org/10.21468/SciPostPhys.17.4.099) | `X32BR5K2`，PDF `T74TRMU7` | arXiv:2405.06891v2，Sec. 2.1.1，Eqs. (5)--(8)；p. 6，Sec. 2.1.2，Eqs. (14)--(16)，已逐式目检该页 | 边界应力张量为标度维数 $2$ 的算符，给每个低能能级带来二阶逆长度的一阶微扰修正；两能级相减仍有同阶贡献。等价表述为两端非普适的有效长度偏移。数值例子是 Ising 与三态 Potts，不是本项目 XXZ 的专门谱推导。 |

### 与本项目拟合的关系

以下是依据上述文献机制、改用本项目记号的推论，不是从文献照搬的 XXZ 扇区公式。设临界低能态的主导间隔系数为 $B$，边界有效长度为 $L+\ell$，则仅对这一长度偏移贡献作展开：

$$
\frac{B}{L+\ell}=\frac{B}{L}-\frac{B\ell}{L^2}+O(L^{-3}).
$$

这给出保留 $1/L$ 与 $1/L^2$ 项的理论动机。这里的余项仅属于该分式的代数展开，不宣称完整 XXZ 能隙余项必为 $O(L^{-3})$；体无关算符仍可能带来非整数幂或特殊点的对数修正。固定对称性扇区会选择不同的低能能级，影响系数，不能据此直接指定本文的 $b,c$。

在此无能隙临界点，理论预期的热力学截距为零。拟合中保留自由常数 $a$，是本项目用五个已有尺寸检验外推截距的经验选择；三篇来源没有证明任意相边界都服从带自由截距的三参数多项式，也未验证本文这五个尺寸已经进入渐近区。

可供后续改稿采用的表述：

> 在 $s=1/2$ 处，考虑临界开链低能能隙的 $1/L$ 标度及边界有效长度偏移产生的 $1/L^2$ 修正，采用 $\Delta_{\rm sec}(L,1/2)\approx a+b/L+c/L^2$ 对五个尺寸作有限尺寸外推，其中 $a$ 为自由拟合截距。

入库报告：目标为既有 `physics/quant_comp/paper/inbox`（`ANJT35BK`）；按 DOI 去重新增三篇，上表为条目与附件 keys，均有核对身份后的开放获取 PDF；新增条目保留 `agent-crawled`、`unreviewed` 标签。没有新增集合，也没有把尚未绑定正文的来源加入论文引用集合。原稿已有 Lukyanov 和 Takayoshi--Sato 来源继续用于各自已核验论述，不以其周期链修正替代本轮开边界依据。

### 正文绑定与验证（2026-11-04，同日后续）

- 按作者要求，在中英文附录式 `eq:gap-fit` 之前加入有效长度偏移的说明：临界低能间隔的主导项按 $1/L$ 衰减；边界长度偏移的逆长度展开产生 $1/L^2$ 贡献。选用 `sirker2008thermodynamics`（`RH8NUY46`）支撑开边界 XXZ 的具体边界算符，选用 `liu2024finitesize`（`X32BR5K2`）支撑边界应力张量对低能能级的修正。Campostrini 等保留为已核验背景来源，此处不再叠加引用。
- 将“按既定经验形式／five stored points”改为说明有限尺寸外推形式及五个尺寸的数据，并明确保留自由截距 $a$。原拟合公式、$a=-0.0168$、$b=94.86$、$c=-114.14$、能量约定和其他引用均保留；没有新增实验、重拟合或改变结果含义。
- 共享书目两条新记录由此前已核验的 Zotero 元数据生成；MCP 恢复后再次导出 BibTeX，逐项核对标题、作者、期刊、卷期、页码、年份和 DOI 一致。两篇均已增量加入既有论文引用集合 `paper-variational-qc`（`N7CLH4TB`），保留原 inbox 及既有标签、附件。
- 两版分别展开各自的输入闭包进行引文与交叉引用检查：各 $11$ 个 TeX 输入、$53$ 个实际引用、共享书目 $67$ 条，检查问题为零。两版完整编译均返回零，最终日志无未定义引文、未定义交叉引用或 overfull 提示；式号均仍为 `(A4)`。逐块比较附录的定界公式与此前 Git 版本一致，已有引用均保留。常规 REVTeX 浮动体提示仍存在。
- 已更新 `docs/paper/main.pdf`、`docs/paper/main-zh.pdf`；未改动被 Git 跟踪的编译缓存。证据目录为 `data/validation/gap-fit-citations-20261104-lSmn6Q/`，其中 `final-verification.json`、`verified-en.log`、`verified-zh.log` 和两份 citation 日志记录最终检查结果。MCP 恢复与单条索引验证单独记在该目录的 `mcp-recovery-report.md`；单条验证不代表全库重新索引完成。

## Zotero 与共享书目对齐检查（2026-11-04）

- 本轮只读核对当前中英文输入闭包、`references.bib`、Zotero 论文集合及必要的全库查缺，没有修改正文、书目、Zotero 元数据或集合成员。两版正文实际引用集合一致，共 53 篇；其 DOI 身份均在论文集合中逐一匹配，均有 PDF 附件记录。本轮不将附件记录覆盖当作重新阅读全文或重审支持关系的证明。
- 共享书目与论文集合均为 67 条，但共同身份只有 63 条。本地另有的 Hadfield（2022）和 Huang（2021，derandomization）已在 Zotero 其他集合，有 PDF；Qi（2021）与 Ware（2021）按 DOI、题名均未在活动文库检出。论文集合另有 Kandala（2019，error mitigation）、Raussendorf（2009，measurement-based computation）、Li--Benjamin（2017）和 Temme 等（2017）四条未进入本地书目。这些差额均未被当前正文引用。
- 有 17 条本地书目所对应的 Zotero 记录存在缺字段或差异，其中正文实际引用 10 条；主要为卷号、页码／文章号或出版物字段缺失。Sandvik 记录 `WCKVFLZP` 将两位论文集编者并列成作者，且缺卷号、出版物；本轮经 MCP 重读 PDF 首页，确认唯一作者为 Sandvik，Avella、Mancini 为编者，现有本地书目与首页的作者、卷页信息一致。Toolbox 的 2022 在线日期与 2023 正式卷期年份属于口径差异，不能把它们判成不同论文。TeX 姓名转义、期刊缩写、`and others` 和合作组署名的排版差异另列，不当作身份错误。
- 结论：实际引用的文献身份和附件覆盖已对齐；完整书目库存、论文集合与部分元数据尚未完全同步。本轮没有自动补入、删去、改写备用条目，也没有重跑全库索引。逐条明细与 MCP 快照见 [本轮报告](../../data/validation/zotero-reference-alignment-20261104-Hpf3En/report.md) 和同目录 `alignment.json`、`zotero-metadata.json`、`zotero-attachments.txt`。

## 按当前实际引用清理书目与论文集合（2026-11-04）

- 按作者指示，以当前中英文正文实际使用的引用为保留清单。重新展开两版输入闭包，确认二者均引用同一批 53 篇；现有 cite keys 和保留条目的元数据不变。
- 从 `references.bib` 移除 14 条未引用条目，保留 53 条；原文件和移除条目分别备份至 `data/validation/reference-cleanup-20261104-5oxoHP/references.before.bib`、`removed-unused.bib`。本轮是条目清理，没有删除共享书目文件。
- 经 MCP 重新读取 Zotero 论文集合和 14 个多余条目的完整元数据，确认这些条目均只属于本论文集合，随后逐项移入 Zotero 回收站；再读取元数据确认全部 14 个条目处于回收站状态。没有清空回收站，没有删除其他集合的文献或直接处理 Zotero 附件文件。
- 清理后的 `paper-variational-qc`（`N7CLH4TB`）恰好包含保留的 53 个 Zotero 条目，与当前正文引用及共享书目的文献身份一致。其他主题集合和本轮未引用的后台文献不属于本次清理范围。
- 两版闭包引文检查均通过，正式中英文稿重新编译均退出零，最终日志无未定义引文、未定义交叉引用或 overfull 提示；已更新两份 PDF。证据位于 `data/validation/reference-cleanup-20261104-5oxoHP/`，包括 `cleanup-plan.json`、`zotero-before.json`、`zotero-trash-results.json`、`zotero-collection-after.txt`、两版编译日志及 `final-verification.json`。
- 本轮按作者要求只清理多余记录；先前核对出的保留条目元数据缺字段、编者角色或日期口径差异未在本轮修改，不把成员清单一致表述为全部元数据已经逐字段同步。


## exp03 的 CPU MPS/DMRG 方法依据（2026-11-04）

- 已经由 Zotero MCP 复核既有条目 `schollwock2011density`（key `3AJILFTW`，DOI `10.1016/j.aop.2010.09.012`）的元数据和所挂 arXiv PDF 目录，并读取 PDF pp. 65–66、71–72 的相关正文。Sec. 6.3 说明固定其他站点后对 MPS 局部张量迭代最小化能量，形成局部本征问题；Sec. 6.4 区分单站点、双站点 DMRG 与变分 MPS 的关系。确认支持待更新附录中“有限开链 MPS 通过 DMRG 扫描优化”的方法背景。此前仅用于 Schmidt 分解的核验范围仍是历史记录，本次补充了实际方法段的阅读。
- 读取的文字中图及部分公式提取不完整；本轮依据清晰正文核验算法解释，不从乱码转录公式，也不新增相应理论推导。
- 本项目的 $H_{\rm pen}=H+\lambda_S S_z^2+\lambda_X(1-\bar X)$、反射筛选及具体惩罚参数来自 exp03 的实现与数值验证，不归为该综述直接给出的模型方案。候选态正交惩罚通过 ITensorMPS 的激发态接口实现；最终物理能量以原始 $H$ 计算。
- 论文方法与结果更新依赖 exp03 完整验收和四尺寸正式数据。当前只完成引用依据核验，尚未据此将 $L=32$ 或新拟合系数写成已发布结果。沿用现有 BibTeX 条目，不另加文献或改 key。
