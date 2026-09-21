# 使用

## 前提

- 项目已 `openspec init --tools opencode`，在项目根目录启动 `opencode`。
- 记住两套接口：终端跑 `openspec ...`（管理项目），OpenCode 聊天框用 `/opsx-*`（真正干活）。

## 内容

### 先看懂 openspec/ 的结构

```text
openspec/
├── config.yaml      项目配置（profile、开关）
├── changes/         草稿区：每次变更各占一个 <name>/ 目录
│   ├── <name>/      proposal.md、design.md、tasks.md + 本次增量 spec
│   └── archive/     归档区：做完的变更搬到这里
└── specs/           定稿区：按能力组织（如 specs/auth/），描述系统现在应该是什么样
```

`changes/` 按次，`specs/` 按能力：多次改登录功能，改的是同一个 `specs/auth/`，不会一次建一目录。

### `name` 是什么

每次变更的代号，一活一名，自己起，短横线小写，如 `add-dark-mode`、`add-jwt-auth`。`archive` 后变成 `changes/archive/<日期>-<name>/`。

### 两套入口：斜杠命令 vs skill

文档里 `/opsx-*` 这种叫**斜杠命令**（slash command），是你主动敲的（手动挡）；**skill**（`openspec-*`）是 OpenCode 按 description 自动套用的（自动挡）。同一套流程，对应关系：

| 你敲的斜杠命令 | 背后同一套流程的 skill |
|---|---|
| `/opsx-propose` | `openspec-propose` |
| `/opsx-explore` | `openspec-explore` |
| `/opsx-apply` | `openspec-apply-change` |
| `/opsx-update` | `openspec-update-change` |
| `/opsx-sync` | `openspec-sync-specs` |
| `/opsx-archive` | `openspec-archive-change` |

平时 skill 自动触发就够用；想明确走规范流程时，才手动敲斜杠命令。

### 主流程（核心只有三步）

```text
/opsx-propose <想法> → 检查 proposal/spec/design/tasks → /opsx-apply → /opsx-archive
```

1. `/opsx-propose 增加 JWT 登录，支持登录、退出和 token 刷新`
—— 生成 `openspec/changes/<name>/` 下的 `proposal.md`、`design.md`、`tasks.md`、`specs/`。
2. 先看规范再动手：打开 `openspec/changes/<name>/` 检查，不对现在就改 spec，不要等代码写完再返工。
3. `/opsx-apply` —— 按 `openspec/changes/<name>/tasks.md` 逐项写代码、跑测试、打勾。
`<name>` 一般不用写(AI会自动判断什么需要apply)：只有一个活跃变更时自动选中，
有多个时它会列出来让你选（活跃变更之间不按新旧排序，分不清就问，不猜）；
只有想明确指定时才写 `/opsx-apply <name>`（`/opsx-update`、`/opsx-archive` 同理）。
4. `/opsx-archive <name>` —— 归档，增量 spec 合并进 `specs/` 下对应的能力目录（如 `specs/auth/`）。

两个可选命令：

- `/opsx-explore` —— 需求不清楚时先分析架构和方案，不写代码。
- `/opsx-update <name>` —— 需求中途变了（如改存 HttpOnly Cookie），先更新规范再 `/opsx-apply` 追上。
- `/opsx-sync` —— 把某次变更的增量 spec 合并进 `specs/` 主规范（智能合并，不是整段复制）。
它是更精细的单步操作：只合规范，变更还留在 `changes/<name>/`。
正常走 `/opsx-archive` 时这步已经包含在内，不用单独敲；
只有"想合规范但不想归档"或"归档后发现没合好"时才手动用它。

不用记的：`openspec completion install` 只是 shell Tab 补全，可选；
`openspec list` / `show` / `validate` / `status` 是终端侧的查看检查命令。

## 验证

- OpenCode 输入 `/` 能看到 6 个 `/opsx-*` 命令。
- 跑完一次 propose 后 `openspec list` 能看到你的 change。
