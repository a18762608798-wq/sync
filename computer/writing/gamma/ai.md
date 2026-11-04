# 配置 AI 与 MCP

## 前提

已完成登录、PDF 上传和批注测试。AI 为可选功能；Gamma 内部聊天使用所连接的提供商，外部助手通过 MCP 读取获授权的 Workspace。

## 步骤

### 1. 配置 Gamma 内部 AI

进入 **Settings → AI → Connections**，按界面选择提供商、填写 API Key 和所需地址，再选择模型。官方列有 OpenAI、Anthropic、DeepSeek 和兼容 OpenAI API 的自定义端点，也提供 ChatGPT 订阅登录入口；以当前界面的可用选项为准。[官方 AI 连接说明](https://gammapdf.com/docs/#ai-services-you-can-connect)

各用户可自行配置连接；先让它总结已打开的测试 PDF，检查回答中的页码引用。

在 **Settings → AI → Tool usage** 设置工具权限，初期保留修改操作需要批准。Gamma 内部 AI 可检索、获取文献，以及整理标题、文件夹、标签和笔记。[官方工具权限说明](https://gammapdf.com/docs/#the-library-agent)

### 2. 连接 Codex CLI

在 **Settings → AI → Integrations** 查看当前版本的连接指引。远程部署时，先由管理员在 **Settings → Server** 确认 **Public server URL**，使其与实际访问入口一致；这是应用设置，无需重启容器。

在运行 Codex 的机器上执行：

```bash
codex mcp add gamma --url http://localhost:9001/mcp
codex mcp login gamma
```

浏览器打开授权页后，使用自己的 Gamma 账号登录，只批准需要读取的 Workspace。上述手动配置方式来自 [Gamma 官方 MCP 指引](https://gammapdf.com/docs/#connect-an-assistant)，命令参数也已用本机 CLI 帮助核对。

| Codex 运行位置 | 访问条件 |
| --- | --- |
| Ubuntu 工作站 | 直接连接服务器本机 `localhost:9001` |
| 自己的客户端电脑 | 先在同一电脑保持 SSH 隧道运行 |
| 客户端使用本地 `19001` | MCP URL 改为 `http://localhost:19001/mcp` |

如果 Codex 在纯 SSH 终端中运行，无法自动打开浏览器，可使用以下方式，并按提示完成授权和回填回调 URL：

```bash
codex mcp login gamma --no-browser
```

使用 `19001` 时，还需核对 Public server URL 和授权链接的端口；多个客户端若需长期稳定授权，优先统一访问入口，后续再配置固定 HTTPS 地址。

### 3. 理解 MCP 的能力范围

外部 MCP 当前面向获授权的单个 Workspace 提供搜索和读取，包括 PDF 文本、笔记与高亮。自动修改文献库使用 Gamma 内部 AI 及其工具权限设置。[官方外部助手说明](https://gammapdf.com/docs/#assistants)

## 验证

让 Gamma 内部 AI 总结测试 PDF，并检查引用；再让 Codex 搜索一条已知笔记、读取对应高亮，确认能访问授权的 Workspace。

API Key、授权令牌和管理员密码均不写入 Compose、说明文档或 Git 仓库。
