# 01 安装：得到一套能用的 Node

> 目标：装好一个 Node LTS，能跑 CLI。版本日常管理见 [04_nvm](../04_nvm/)。

## Node.js 是什么

一句话：在浏览器之外运行 JavaScript 的运行时。

对你而言更重要的是：很多现代 CLI（AI Agent、MCP Server、Neovim 辅助工具）本质就是：

```text
TypeScript / JavaScript 源码 → Node.js 执行
```

装 Node 时通常同时得到 `node`、`npm`、`npx`，无需单独装 npm。

## 版本选什么

不做 Node 开发、只用 CLI / Agent：优先当前 LTS，不要追 Current，除非工具明确要求。长期只维护一个 LTS 最省心。

## 首次安装（两步）

```bash
nvm install --lts
nvm alias default <版本>   # 例如 nvm alias default 24.20.0
```

之后基本可以忘掉 nvm 的存在。完整命令表见 [04_nvm](../04_nvm/)。

## 验证

```bash
node -v    # 例如 v24.20.0
npm -v
nvm --version
```

交互环境可快速自测（`Ctrl+D` 退出）：

```bash
node
```

```javascript
1 + 2
```

确认 `command -v node` 指向 nvm 目录（如 `~/.nvm/versions/node/v24.20.0/bin/node`）即正常。排查细节见 [05_debug](../05_debug/)。
