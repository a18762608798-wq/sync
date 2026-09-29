# 使用

## 前提

- 项目已 `specify init --here --integration opencode`，在项目根目录启动 `opencode`。
- 记住：`specify init` 是终端 CLI；`/speckit.*` 是 OpenCode 聊天框里的 agent 命令，不要在 shell 里跑后者。

## 内容

### 先看懂目录关系

```text
.opencode/commands/   怎么执行 Spec Kit
.specify/             规则+模板+脚本（memory/templates/scripts）
specs/<NNN-name>/     每个功能的设计成果，重点 review 并提交 Git
src/                  最后实现的代码
```

`specs/` 是 `init` 时没有的，做第一个 feature 后才产生：

```text
specs/001-user-auth/
├── spec.md          做什么（需求+验收）
├── plan.md          怎么做（含 research/data-model/contracts/quickstart）
├── tasks.md         拆成什么（可执行、有依赖顺序）
└── checklists/
```

### 主流程（一次敲一个，看完结果再下一步）

小功能短路径：

```text
/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement → /speckit.converge
```

生产级全路径：

```text
/speckit.constitution → /speckit.specify → /speckit.clarify → /speckit.plan → /speckit.checklist → /speckit.tasks → /speckit.analyze → /speckit.implement → /speckit.converge
```

各步只做一件事：

- `/speckit.constitution`：定一次(就最开始)，管长期（如 REST/架构/测试/错误格式约束）。
- `/speckit.specify`：只讲 what/why，不讲技术栈。
- `/speckit.clarify`：消歧义，必须在 plan 之前。
- `/speckit.plan`：定技术栈和设计。
- `/speckit.checklist`：给需求做质量门禁。
- `/speckit.tasks`：拆出可执行任务。
- `/speckit.analyze`：只读检查 spec/plan/tasks 一致性，有问题回源头改。
- `/speckit.implement`：这时才写代码。
- `/speckit.converge`：对照 spec 查遗漏，未收敛则补 tasks 再 implement。

### 与 OpenSpec 的分工

```text
新项目 / 大改造 / 需重做完整设计 → Spec Kit（建立基线）
日常需求 / 改规则 / 小功能 / 局部调整 → OpenSpec（proposal → apply → archive）
```

不要同时用两套维护同一份事实（如 `specs/001-auth/spec.md` 和 `openspec/specs/auth/spec.md` 各说一套）。建议：`constitution` 长期保留管“必须遵守什么”，`openspec/specs/` 管“系统现在是什么”，大架构改造再切回 Spec Kit。

## 验证

- 跑完一次 `/speckit.specify` 后 `specs/` 下多出一个编号目录。
- 跑完 `/speckit.analyze` 无阻断性冲突后再 `/speckit.implement`。
