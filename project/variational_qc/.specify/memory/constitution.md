# Constitution

## I. Spec 是实验定义的权威来源

任何影响实验语义、结果解释或可重复性的条件，都必须由对应
feature 的 spec 明确定义。

实现不得静默改变实验语义。
实验定义发生变化时，应先更新 spec。

Spec 是持续维护的活文档，而不是一次性交付物。

## II. 实验笔记、实验规范与论文分离

- `docs/experiment-notes/`：为 Exp 实现服务的模型、公式、符号与计算约定，
  允许简写和省略背景
- `spec.md`：实验或计算任务的定义
- `plan.md`：实现方案与技术决策
- `tasks.md`：具体实现工作
- `docs/planning/paper-outline.md`：唯一论文大纲
- `docs/paper/`：正式论文正文与参考文献

实验笔记与 spec 必须保持科学约定一致；不在 spec 重复推导，
也不将无必要的实现细节写入 spec。

正式论文理论必须先通过文献技能检索并阅读全文，核验来源对具体论述的
支撑与适用条件，再独立组织定义、前提与推导，并与 Exp 约定核对。
必须区分文献结论与项目自己的构造；已有正确公式可保留，
不得将笔记中的简写直接视为完整论证，也不得因补引文而改变实验含义。

Paper 按任务使用独立 skills，直接维护论文大纲和正文；
不创建 Paper spec、plan、tasks、paper-map 或 paper feature。

项目目录约定由 `docs/README.md` 维护：规划放 `docs/planning/`，
派生看板放 `docs/status/`，中文论文字体及许可证放
`assets/fonts/noto-serif-cjk/`，Times New Roman 绘图字体与原授权说明放
`assets/fonts/times-new-roman/` 并由 helper 按文件加载。新增文件和生成产物
必须遵守这些路径，不得在根目录另建副本。

## III. Feature 边界必须清晰

- 每个 feature 应拥有明确且尽量独立的职责。
- 不同 feature 不应重复定义同一实验流程或基础能力。
- 多个 feature 共用的能力应抽取为共享 capability，而不是重复实现。

## IV. 实验必须可重复和可追溯

- 影响结果的参数、输入、随机性、数值设置及必要运行信息必须能够被记录和恢复。
- 不得依赖影响结果但未被记录的隐式条件。
- 长时计算必须增量落盘、可中断恢复；禁止全量驻内存 + 单文件收尾。

## V. 科学正确性优先于性能

- 优化、重构或并行化不得静默改变科学结果的含义；并行化不得引入嵌套 oversubscription。
- 任何可能改变数值行为的修改都必须重新验证正确性。

## VI. Spec 必须清晰且可验证

- Spec 应区分面向研究者的科学描述与具有规范性的约束，并保持两者一致。
- 规范性约束应采用足以消除歧义、支持验证的最低必要形式化程度。
- 数学性质优先使用数学表达；行为性质可使用受控自然语言。
- 不得用多个彼此独立的表述重复定义同一规范性约束。

## VII. 项目技术与风格约定

| 域 | Skill |
| --- | --- |
| 研究型计算（仿真 / 参数扫描 / 论文复现） | `scientific-research-computing` |
| 可复用 Julia 包 / 库开发 | `scientific-package-development` |
| 运行环境 | `scientific-project-environment` |
| 出图风格 | `scientific-figure-style` |
| 论文写作、引用、排版与评审 | 按任务使用独立 `paper-*` skills |

## Governance

本宪法适用于 `variational_qc_v0.3.0` 项目，优先级高于其他开发实践。
修订须记录原因、更新版本号与日期，并在需要时给出迁移说明。

版本策略：MAJOR 为不兼容的治理或原则删除/重定义；
MINOR 为新增原则或实质性扩展；PATCH 为澄清、措辞与非语义修正。

合规要求：每次 `specify / plan / tasks / implement` 前检查是否符合
I–VI 原则；复杂度须有明确理由；违反宪法须在 plan 或任务中显式说明。

实验展开规则：以 `docs/planning/experiment-map.md`
为实验划分依据；每个 `shared-xx` / `expXX` 为一个独立 feature；
一次展开一个新实验；新建或实质重设计实验时走一轮完整 specify 流程
（specify → clarify → plan → tasks → analyze → implement → converge）；
不得将多个实验合并为一个 spec，不得在 spec 之外另行定义
Dxx / Sxx 产出归属与实验依赖关系。

已有 feature 的普通修改按实际影响增量维护：科学定义先更新 spec，
实现设计和任务仅在受影响时同步。日常工作方式由项目 AGENTS.md 约定，
不要求每次修改重走完整流程或经过工具门禁。
按需使用 analyze/converge 检查全项目及跨实验依赖；只读审计与修复、任务回填明确区分。
检查结论须注明覆盖范围与证据，不将未核验项记为通过。

上述 feature 与完整 Spec Kit 流程约束适用于 Exp。仅涉及论文措辞、文献核验、
排版与评审的修改不建立 Exp feature；需要新增实验，或改变实验定义、参数、
数据产品及结论含义时，先返回受影响的 Exp 评估和更新规范。
论文看板只展示图与数据的就绪度，不证明正文、引用或正式论证完成。

**Version**: 1.2.0 | **Ratified**: 2026-10-02 | **Last Amended**: 2026-11-03
