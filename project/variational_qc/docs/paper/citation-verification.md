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
