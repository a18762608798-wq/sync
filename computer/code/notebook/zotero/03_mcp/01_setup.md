# 54yyyu/zotero-mcp

## 开启 Zotero 本地 API

打开 Zotero：

设置 → 高级
→ 勾选“允许此计算机上的其他应用程序与 Zotero 通信”

使用本地 API 时不需要 Zotero API Key，但 Zotero 桌面程序必须保持运行。本地模式读取速度快，并支持 PDF 全文访问。

## 安装 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

重新加载 Shell：

```bash
exec "$SHELL" -l
uv --version
```

## 安装 Zotero MCP

```bash
uv tool install "zotero-mcp-server[all]"
```

验证安装：

```bash
zotero-mcp version
zotero-mcp setup-info
command -v zotero-mcp
```
