# config

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
