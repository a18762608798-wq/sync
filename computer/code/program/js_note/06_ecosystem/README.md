# 06 生态：TS 与其他工具

## TypeScript 与 Node 的关系

```text
TypeScript = JavaScript + 类型系统
```

传统流程：

```text
foo.ts → tsc → foo.js → node foo.js
```

现代工具链常把这步藏起来。作为使用者不需要学 TS、不需要手跑 `tsc`，只需保证：

```text
Node 版本正确
npm 包安装成功
CLI 能运行
```

## pnpm / yarn / bun / corepack

| 名称 | 一句话 |
|------|--------|
| npm | Node 默认自带 |
| pnpm | 很常见的替代包管理器 |
| yarn | 历史很久的包管理器 |
| bun | runtime + 包管理 + 工具链 |
| corepack | 帮 Node 管理 pnpm / yarn，只用 npm 可忽略 |

原则：进现有项目跟项目走，不要无故换包管理器。看锁文件认工具：

| 锁文件 | 通常用 |
|--------|--------|
| `package-lock.json` | npm |
| `pnpm-lock.yaml` | `pnpm install` |
| `yarn.lock` | yarn |
