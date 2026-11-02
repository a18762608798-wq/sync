# 文档导航与固定路径约定

本文档是项目目录约定的维护入口。以下完整路径均相对于项目根目录；Markdown 和 HTML 的实际链接须相对于所在文件解析。

## 规划与状态

- [论文大纲](planning/paper-outline.md)：论文内容清单与 Dxx 数据需求。
- [实验映射](planning/experiment-map.md)：Dxx / Sxx 的生产归属、实验划分与依赖。
- [论文看板](status/paper.html) / [实验看板](status/experiments.html)：派生的进度展示，不是实验定义或完成状态的权威来源。
- [实验规格](../specs/)：每个 feature 的 spec / plan / tasks；具体实验定义以 spec 为准，进度结合 tasks 与实际产物判断。
- [本地环境与非真机验证](status/local-validation.md)：本次环境安装、Pi 迁移与测试结果，包含 exp03 拟合重组装记录。

## 固定目录

| 目录 | 职责 |
| --- | --- |
| `assets/fonts/noto-serif-cjk/` | 中文论文使用的 Regular / Bold 字体与 LICENSE |
| `assets/fonts/times-new-roman/` | 绘图使用的四种 Times New Roman 字形与授权说明 |
| `docs/planning/` | `paper-outline.md`、`experiment-map.md`；若启用论文 feature，`paper-map.md` 也放这里 |
| `docs/status/` | `paper.html`、`experiments.html` 两个自包含状态页 |
| `docs/theory/` | 理论、模型、推导与背景 |
| `docs/paper/` | LaTeX 主文件、章节与参考文献，既有论文工程位置不变 |
| `specs/<feature>/` | 实验规格、实现计划和任务清单 |
| `figs/<feature>/` | 绘图产物：矢量 PDF 与 PNG 预览 |
| `data/<feature>/` | 实验数据，沿用现有忽略规则 |
| `.pi/prompts/` | Spec Kit 的 Pi prompt templates，提供 `/speckit.*` 命令 |
| `.pi/skills/` | Pi 项目技能及其脚本、引用和模板 |

不要在项目根目录重新生成字体、规划文档或状态页，不要复制一份规划文档到别处维护。新增目录或调整路径时，先更新本文档，再同步引用、模板与 skills。

## 字体

- 中文论文按文件路径加载 [Noto Serif CJK SC](../assets/fonts/noto-serif-cjk/)，不依赖系统中同名字体。字体来自 [Noto CJK](https://github.com/notofonts/noto-cjk)，[LICENSE](../assets/fonts/noto-serif-cjk/LICENSE) 为上游 Serif 目录的 SIL Open Font License 1.1；版权信息保留在原始字体元数据中。
- 从 `docs/paper/` 编译时，字体目录为 `../../assets/fonts/noto-serif-cjk/`。
- 绘图字体与中文论文字体分开管理：[Times New Roman 四种字形](../assets/fonts/times-new-roman/) 已纳入本项目 Git。`scripts/figure_style.py` 的 `apply_figure_style()` 自动按文件注册并优先于系统同名字体，不需要系统安装；数学字体仍为 Matplotlib 自带 STIX。
- 本地字体目录存在但不完整或字体族错误时立即报错。正式出图应检查最终解析到的字体路径确实位于 `assets/fonts/times-new-roman/`，而非静默回退。
- Times New Roman 不是开源字体；其[原授权说明](../assets/fonts/times-new-roman/README.md)与 Noto 的 SIL OFL 分开。纳入 Git 不代表获得额外的再分发权利；开发源同时保存字体依赖：`scientific-computing/assets/fonts/times-new-roman/` 保存四种 TTF 与原授权说明，`scientific-paper/assets/fonts/noto-serif-cjk/` 保存两种 OTF 与 LICENSE；各 preset 的 `scripts/install-fonts.sh` 将依赖复制到项目对应目录，已有同名文件内容不一致时停止，不静默覆盖。
- PDF 图嵌入字体；仅编译论文、不重新绘图时，不需要另外安装绘图字体。

## Pi 集成与本地验证

Spec Kit 默认集成为 `pi`；初始化参数记录于 `.specify/init-options.json`，当前集成记录于 `.specify/integration.json`。
项目 skills 从原宿主目录迁移到 `.pi/skills/`，命令由 Spec Kit 生成至 `.pi/prompts/`；当前 Pi 会话需执行 `/reload` 才会发现新资源。

Julia 与 Python 安装、测试命令见 [项目 README](../README.md)。非真机新计算和绘图测试产物放入 `data/validation/`，不覆盖正式数据或 `figs/`；真机提交脚本不属于本地环境验证范围。

## 维护与验证

- outline 的数据需求变更时，同步 experiment-map 中的 Data Products / Coverage，再更新受影响的 spec。
- 状态页仅按请求更新；迁移路径本身不改变状态徽标、任务计数或实验结论。
- 从 `docs/status/` 链接规划文档使用 `../planning/...`，链接 spec 与图片使用 `../../specs/...`、`../../figs/...`；两个看板之间直接用 `paper.html` / `experiments.html`。
- 路径迁移后检查本地链接、LaTeX 字体路径和 README 的在线地址；旧的编译缓存不作为有效路径依据，应在下一次正常编译时刷新。
- GitHub Pages 沿用项目根目录发布，根目录 `.nojekyll` 保留；在线入口改为 `docs/status/paper.html` 与 `docs/status/experiments.html`。
