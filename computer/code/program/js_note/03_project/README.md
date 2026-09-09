# 03 项目三件套：package.json / lock / node_modules

> 进到一个 JS / TS 项目，最常看到的就是这三个。读懂它们就能理解 `npm test`、`npm run build` 在干什么。

```text
project/
├── package.json       # 要哪些依赖 + 元数据 + 常用脚本
├── package-lock.json  # 精确锁定最终装了哪些版本，npm 自动维护，不要手改
└── node_modules/      # 实际安装的依赖，可能很大，不要手改，不要提交 Git
```

## scripts：`npm test` 到底在跑什么

`package.json` 示例：

```json
{
  "scripts": {
    "test": "vitest",
    "build": "tsc",
    "dev": "vite"
  }
}
```

则 `npm test` = 执行 `vitest`，`npm run build` = 执行 `tsc`。Agent 让你跑 `npm run build` / `npm test` / `npm run lint`，本质都是跑这里定义好的脚本。

## package-lock.json

```text
package.json      → 我要哪些依赖
package-lock.json → 最终精确安装的是哪些版本
```

不要手动编辑，npm 会自己维护。

## node_modules

`npm install` 后出现，存放实际依赖。项目 `.gitignore` 一般包含它。出奇怪问题时的重建方法（非万能）：

```bash
rm -rf node_modules
npm install
```

## `npm install` 与 `npm ci`

| 命令 | 适用场景 |
|------|----------|
| `npm install` | 开发、增删改依赖；会更新 lockfile |
| `npm ci` | 按 lockfile 做干净、可复现安装；CI / Agent 自动测试常用 |

有 `package-lock.json` 的项目做复现安装优先 `npm ci`。
