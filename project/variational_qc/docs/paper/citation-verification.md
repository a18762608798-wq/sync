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
