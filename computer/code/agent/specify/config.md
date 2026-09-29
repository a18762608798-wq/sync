# 配置

## 前提

- 已按 `install.md` 装好 `specify`。
- 站在你的项目根目录，`git status` 干净（已有项目直接 `--here`，不是重建项目）。
- 记住两套接口：终端跑 `specify ...`（装工作流），OpenCode 聊天框用 `/speckit.*`（真正干活）。

## 内容

初始化（告诉 Spec Kit 按 OpenCode 能识别的格式生成文件）：

```bash
specify init --here --integration opencode --script sh
```

参数说明：

- `--here`：在当前目录初始化；目录非空需加 `--force`。
- `--script sh`：Linux Mint 用 `sh`；Windows 用 `ps`，或统一用 `py`。

实测生成以下文件：

```text
.opencode/commands/speckit.{specify,clarify,plan,tasks,implement,...}.md
.specify/
├── memory/constitution.md   项目原则，长期保留
├── templates/               spec/plan/tasks/checklist 模板
├── scripts/bash/            create-new-feature.sh 等自动化脚本
├── integration.json
└── init-options.json
```

分工：`.opencode/` 是给 OpenCode 看的操作说明，`.specify/` 是 SDD 引擎（规则+模板+脚本）。`scripts/` 一般不要手工改。

已有项目接 Spec Kit：先提交干净，再 `--here`，先写 `constitution` 描述现有架构约束，再逐个 feature 纳入。

## 验证

```bash
ls .opencode/commands
ls .specify
```

在 OpenCode 输入 `/` 能看到 `/speckit.specify` 等命令即成功（以 `/` 补全和 `.opencode/commands/` 下实际文件名为准）。
