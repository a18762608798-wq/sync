# 文档导航与固定路径约定

本文档是项目目录约定的维护入口。以下完整路径均相对于项目根目录；Markdown 和 HTML 的实际链接须相对于所在文件解析。

## 规划与状态

- [论文大纲](planning/paper-outline.md)：论文内容清单与 Dxx 数据需求。
- [实验映射](planning/experiment-map.md)：Dxx / Sxx 的生产归属、实验划分与依赖。
- [论文看板](status/paper.html) / [实验看板](status/experiments.html)：派生的进度展示，不是实验定义或完成状态的权威来源。
- [实验规格](../specs/)：每个 feature 的 spec / plan / tasks；具体实验定义以 spec 为准，进度结合 tasks 与实际产物判断。

## 固定目录

| 目录 | 职责 |
| --- | --- |
| `assets/fonts/noto-serif-cjk/` | 中文论文使用的 Regular / Bold 字体与 LICENSE |
| `assets/fonts/times-new-roman/` | 绘图使用的四种 Times New Roman 字形与授权说明 |
| `docs/planning/` | 唯一论文大纲 `paper-outline.md` 与 Exp 生产归属 `experiment-map.md` |
| `docs/status/` | `paper.html`、`experiments.html` 两个自包含状态页 |
| `docs/experiment-notes/` | 核心理论笔记：模型、定义、符号、假设、公式与必要推导 |
| `docs/paper/` | LaTeX 主文件、章节与参考文献，既有论文工程位置不变 |
| `specs/<feature>/` | 实验规格、实现计划和任务清单 |
| `figs/<feature>/` | 绘图产物：矢量 PDF 与 PNG 预览 |
| `data/<feature>/` | 实验数据，沿用现有忽略规则 |
| `.agents/skills/` | Exp 的 Spec Kit skills、科学计算公共 skills 与独立的 Paper skills |

不要在项目根目录重新生成字体、规划文档或状态页，不要复制一份规划文档到别处维护。新增目录或调整路径时，先更新本文档，再同步引用、模板与 skills。

## Exp 与 Paper 的边界

- Exp 继续以 `specs/<feature>/spec.md` 定义实验，`plan.md` 记录实现决策，`tasks.md` 跟踪执行与验证；普通修改按项目 [AGENTS.md](../AGENTS.md) 增量维护。
- [理论笔记](experiment-notes/README.md) 只描述核心理论，不提前安排后续实验，也不放执行状态、产物记录或文献事务。具体参数、采集与处理流程、验收条件写入对应 spec/plan/tasks；参考文献与来源核验记录归 `docs/paper/`。理论与 Exp 的科学约定保持一致，笔记中的简写不能直接充当正式论文论证。
- Paper 直接维护 [论文大纲](planning/paper-outline.md) 与 `docs/paper/`，通过写作、引文、排版、评审和修订 skills 完成工作；不创建 Paper spec、plan、tasks、paper-map 或 paper feature。
- 写作理论部分时，先检索并阅读全文，核验文献对具体论述的支撑与适用条件，再独立组织定义、前提和推导，并核对 Exp 的符号、参数与观测量约定。区分文献结论与项目自己的构造，不因补引文而改变实验含义。
- [引用支撑索引](paper/citation-verification.md) 按文献维护当前的来源、已读位置、支撑论述、适用条件和正文绑定位置；证据缺口就地标注，论述范围变化时更新对应条目。实验参数和验收结果引用既有 Exp 规范与正式产物，修订历史通过 Git 查看，详细验证输出沿用 `data/validation/` 下的运行目录；日常改稿不向引用索引追加修订或编译日志。
- 缺少文献或论证时在 Paper 任务中补齐；需要新增实验、改动参数或改变结果解释时返回受影响的 Exp。Dxx / Sxx 编号保持稳定，不随章节重排重编号。
- 论文看板展示所需图与数据的就绪度；数据齐全不代表正文、理论论证或引用核验已经完成。

## 工作方式与整体对齐

日常按 [AGENTS.md](../AGENTS.md) 处理受影响的规范和验证。新建或实质重设计实验走完整 Spec Kit 流程；已有 feature 的维护按影响增量进行。

- `$speckit-analyze 全项目`：只读检查所有 feature、规划、数据归属与跨实验依赖。
- `$speckit-converge 全项目 仅检查`：只读核对实际实现、结果和验证证据，不回填任务。
- `$speckit-converge 全项目`：核验后将已有规范下真正缺失的工作补入相应 tasks；已有任务不重复追加。
- 明确要求“修复并对齐”时，先检查，再按问题所在层处理并复查；科学意图不明时提出问题。
- 审计不自动重算正式实验、提交真机任务或更新看板。报告区分文档一致性、实现/结果核验及尚未核验的项目。

## 字体

- 中文论文按文件路径加载 [Noto Serif CJK SC](../assets/fonts/noto-serif-cjk/)，不依赖系统中同名字体。字体来自 [Noto CJK](https://github.com/notofonts/noto-cjk)，[LICENSE](../assets/fonts/noto-serif-cjk/LICENSE) 为上游 Serif 目录的 SIL Open Font License 1.1；版权信息保留在原始字体元数据中。
- 从 `docs/paper/` 编译时，字体目录为 `../../assets/fonts/noto-serif-cjk/`。
- 绘图字体与中文论文字体分开管理：[Times New Roman 四种字形](../assets/fonts/times-new-roman/) 已纳入本项目 Git。`scripts/figure_style.py` 的 `apply_figure_style()` 自动按文件注册并优先于系统同名字体，不需要系统安装；数学字体仍为 Matplotlib 自带 STIX。
- 本地字体目录存在但不完整或字体族错误时立即报错。正式出图应检查最终解析到的字体路径确实位于 `assets/fonts/times-new-roman/`，而非静默回退。
- Times New Roman 不是开源字体；其[原授权说明](../assets/fonts/times-new-roman/README.md)与 Noto 的 SIL OFL 分开。纳入 Git 不代表获得额外的再分发权利；开发源同时保存字体依赖：`scientific-computing/assets/fonts/times-new-roman/` 保存四种 TTF 与原授权说明，`scientific-paper/assets/fonts/noto-serif-cjk/` 保存两种 OTF 与 LICENSE；Exp preset 与 Paper 技能包各自的 `scripts/install-fonts.sh` 将依赖复制到项目对应目录，已有同名文件内容不一致时停止，不静默覆盖。
- PDF 图嵌入字体；仅编译论文、不重新绘图时，不需要另外安装绘图字体。

## Codex 集成与本地验证

Spec Kit 默认集成为 `codex`；初始化参数记录于 `.specify/init-options.json`，当前集成记录于 `.specify/integration.json`。
Spec Kit skills 由 `specify` 生成至 `.agents/skills/`；独立的 Paper skills 也安装在此目录，直接按任务使用。
Paper 技能包的源保留在 `~/.agents/sdd/specify/dev/scientific-paper/`。

Julia 与 Python 安装、测试命令见 [项目 README](../README.md)。非真机新计算和绘图测试产物放入 `data/validation/`，不覆盖正式数据或 `figs/`；真机提交脚本不属于本地环境验证范围。

## 维护与验证

- outline 的数据需求变更时，同步 experiment-map 中的 Data Products / Coverage，再更新受影响的 spec。
- 状态页仅按请求更新；迁移路径本身不改变状态徽标、任务计数或实验结论。
- 从 `docs/status/` 链接规划文档使用 `../planning/...`，链接 spec 与图片使用 `../../specs/...`、`../../figs/...`；两个看板之间直接用 `paper.html` / `experiments.html`。
- 路径迁移后检查本地链接、LaTeX 字体路径和 README 的在线地址；旧的编译缓存不作为有效路径依据，应在下一次正常编译时刷新。
- GitHub Pages 沿用项目根目录发布，根目录 `.nojekyll` 保留；在线入口改为 `docs/status/paper.html` 与 `docs/status/experiments.html`。
