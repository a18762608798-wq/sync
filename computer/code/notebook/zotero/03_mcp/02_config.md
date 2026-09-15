# config

## zotero-mcp 配置

在 `~/.config/zotero-mcp/config.json`

最好增加读取约束限制:

```json
{
  "semantic_search": {
    "extraction": {
      "fulltext_display_max_pages": 100
    }
  }
}
```

## 配置opencode MCP

```jsonc
  "mcp": {
    "zotero": {
      "type": "local",
      "command": ["zotero-mcp"],
      "enabled": true,
      "timeout": 15000,
      "environment": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
```

## 配置pi MCP

关闭自更新, 因为无法检测代理地址.

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": ["serve"],
      "transport": "stdio",
      "lifecycle": "eager",
      "env": {
        "FASTMCP_CHECK_FOR_UPDATES": "off",
        "NO_PROXY": "127.0.0.1,localhost"
      }
    }
  }
}
```

## 编辑模式开启

原因：`Zotero` 本地 API 只读，`local-only` 下写工具直接报错
`Cannot perform write operations in local-only mode`。
需切 `hybrid` 模式（本地读 + `web API` 写）：

1. 取凭证（需先登录）：`https://www.zotero.org/settings/keys/new`
   （`Settings → Feeds/API → Create new private key`），`Description` 如 `opencode-mcp-write`；
   `Personal Library` 勾 `Allow library access + Allow notes access + Allow write access`，
   `Default Group Permissions` 不用群组库选 `None`。
   同页顶部 `Your userID for use in API calls is ...` 即数字 `userID`（如 `17874348`，
   不是用户名，也不是本地的 `0/1`；群组库才用 `groupID` + `ZOTERO_LIBRARY_TYPE=group`）。
2. 密钥存 `~/.profile`，不明文落盘：

```bash
export ZOTERO_API_TOKEN="..."
export ZOTERO_USERID="17874348"
```

3. 改 `~/.config/opencode/opencode.jsonc` 的 `mcp.zotero.environment`，用 `{env:...}` 引用
   （`zotero-mcp` 只认 `ZOTERO_API_KEY`，名字必须对上）：

```jsonc
"zotero": {
  "type": "local",
  "command": ["/home/mintusr/.local/bin/zotero-mcp"],
  "enabled": true,
  "environment": {
    "ZOTERO_LOCAL": "true",
    "ZOTERO_API_KEY": "{env:ZOTERO_API_TOKEN}",
    "ZOTERO_LIBRARY_ID": "{env:ZOTERO_USERID}",
    "ZOTERO_LIBRARY_TYPE": "user"
  }
}
```

4. 从 `source ~/.profile` 过的终端重启 `opencode`
   （桌面图标启动继承不到变量会掉回只读），`opencode mcp list` 显示 `zotero connected` 即通；
   写后桌面端点 `Sync` 才能看到。
5. 含密钥引用，注意 `chmod 600 ~/.config/opencode/opencode.jsonc`，别提交。

## 语义搜索

### 基础配置

这东西默认配置的mcp是claude，所以需要手动设置:

```bash
# 只配置语义搜索
zotero-mcp setup --semantic-config-only
# 建立全文索引(下载model环境变量问题不要开代理), 从 Zotero 读取文献和 PDF 文字，建立一份供语义搜索使用的本地 ChromaDB 索引。
zotero-mcp update-db --fulltext
#zotero-mcp update-db --fulltext --force-rebuild # If you change the model.
#zotero-mcp update-db --fulltext --no-openai-batch # openai 更新

# 检查 OpenCode 连接
opencode mcp list
```

### 模型升级

#### api 测试

用api, ollama毫无作用; 使用qwen模型, 写入环境变量(存成openai的):

```bash
curl --fail-with-body \
  "${OPENAI_BASE_URL}/embeddings" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-v4",
    "input": "这是一个语义向量测试"
  }'
```

#### zotero mcp 配置

一路默认设置:

```bash
zotero-mcp setup --semantic-config-only
```

```bash
nvim ~/.config/zotero-mcp/config.json
```

把其中`"semantic_search": {`
改成

```text
"embedding_model": "openai",
"embedding_config": {
  "model_name": "text-embedding-v4"
},
"openai_batch": {
  "enabled": false
},
```

保护配置文件

```bash
chmod 600 ~/.config/zotero-mcp/config.json
```

然后强制rebuild

```bash
zotero-mcp update-db \
  --fulltext \
  --force-rebuild \
  --no-openai-batch
```

后续手动更新:

```bash
zotero-mcp update-db --fulltext --no-openai-batch
```
