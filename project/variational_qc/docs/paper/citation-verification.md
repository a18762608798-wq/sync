# 引用核验记录（paper-zotero-hunter verify 台账）

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
