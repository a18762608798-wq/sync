# Node / npm / nvm 基础环境笔记

> 适用对象：不做 JavaScript 开发，但需要使用 Node 编写的 CLI / AI Agent / MCP Server 的 Linux 用户。
> 目标：能安装、能运行、能排查。不学 JS 语法，不做 Node 开发。
> 原文存档见 `ref.md`，本目录是整理后的分篇版本。

## 心智模型

```text
nvm
 │  安装 / 切换 Node
 ▼
Node.js
 │  自带 npm / npx
 ▼
npm
 ├─ 项目依赖 → node_modules/、TypeScript、各类库
 └─ 全局 CLI   → pi、prettier、…
```

| 工具 | 一句话 | 类比 Python（仅助记，不完全准确） |
|------|--------|----------------------------------|
| Node.js | 在浏览器之外运行 JS 的运行时 | Python 解释器 |
| npm | Node 默认包管理器，管依赖和 CLI | pip |
| nvm | Node 版本管理器，只管装 / 切 / 删 Node | pyenv |
| npx | 临时运行某个包的命令，可不全局安装 | - |

执行 `pi` 时的链路：

```text
shell → 找到 npm 装的 pi 可执行文件 → Node.js → 运行 Pi 的 JS/TS 构建产物
```

所以真正要管好的只有三样：Node 版本、npm 包、PATH。

## 目录导航

| 目录 | 内容 |
|------|------|
| [01_install](01_install/) | Node 是什么、选什么版本、nvm 首次安装、验证 |
| [02_npm](02_npm/) | local / global 安装、npx、全局包管理、registry、sudo、ignore-scripts |
| [03_project](03_project/) | package.json、package-lock.json、node_modules、scripts、install vs ci |
| [04_nvm](04_nvm/) | 版本切换、多版本全局包隔离坑、更新迁移 |
| [05_debug](05_debug/) | 环境排查：诊断命令、command -v、排查顺序 |
| [06_ecosystem](06_ecosystem/) | TS 与 Node 的关系、pnpm / yarn / bun / corepack |

阅读顺序：按编号从 01 到 06 即可。赶时间只看本页速查 + [05_debug](05_debug/)。

## 日常速查

```bash
# 当前环境
node -v
npm -v
nvm --version

# 真正在跑哪个程序
command -v node
command -v npm

# Node 管理（单 LTS 策略下很少用）
nvm ls
nvm install --lts # 安装最新版本
nvm use <version>
nvm alias default <version>
nvm alias default 'lts/*' # 将 nvm 的默认 Node.js 版本设置为最新的 LTS（长期支持）版本
nvm uninstall <version>

# npm 全局 CLI
npm ls -g --depth=0
npm install -g <package>
npm uninstall -g <package>

# 当前项目
npm install
npm test
npm run build
npm run lint
```

## 推荐策略

```text
只保留一个 Node LTS
不折腾多版本
不 sudo npm
不主动升级 npm 本体
不学全所有 JS 包管理器，项目用什么跟什么
```
