# 使用 Gamma

## 前提

服务器上的 Gamma 容器已启动，并已取得管理员初始密码或个人账号。服务器 `9001` 端口只绑定 `127.0.0.1`，客户端通过 SSH 转发访问。

## 步骤

### 1. 在客户端建立 SSH 隧道

在运行浏览器的电脑上执行；将 `<服务器IP>` 替换为实际地址，SSH 用户名按自己的账号调整：

```bash
ssh -o ExitOnForwardFailure=yes -N -L 127.0.0.1:9001:127.0.0.1:9001 dell@<服务器IP>
```

已有 SSH 主机别名时，也可将 `dell@<服务器IP>` 替换为 `<SSH主机别名>`。命令会保持运行且不打开远程终端；保留该窗口，关闭连接即断开隧道。

在同一台客户端电脑的浏览器打开 [http://localhost:9001](http://localhost:9001)。这里的 `localhost` 指浏览器所在电脑；转发目标 `127.0.0.1:9001` 指 SSH 服务器上的 Gamma。

如果客户端 `9001` 已被占用，改用 `19001`：

```bash
ssh -o ExitOnForwardFailure=yes -N -L 127.0.0.1:19001:127.0.0.1:9001 dell@<服务器IP>
```

此时浏览器访问 [http://localhost:19001](http://localhost:19001)。SSH 隧道提供传输加密，此访问方式无需为 Gamma 配置公网端口、反向代理或 HTTPS。

### 2. 首次登录

用 `admin` 和首次启动日志中的密码登录，修改管理员密码。需要多用户时，按[配置文档](config.md)创建普通账号和共享 Workspace。

### 3. 导入一份 PDF

选择自己的 Workspace，将一份本地测试 PDF 拖入文献库；也可点击 **+** 上传文件或粘贴 DOI、arXiv 等文献链接。[官方入门文档](https://gammapdf.com/docs/#getting-started)

先用本地 PDF 验证上传和阅读，之后再测试链接获取，便于区分应用问题与外部站点访问问题。

### 4. 高亮与写笔记

打开 PDF，选中一段文字并选择高亮颜色，在对应 Notes 块下写一句测试笔记；点击高亮和笔记，检查能否互相定位。刷新页面后确认内容仍存在。[官方批注文档](https://gammapdf.com/docs/#highlight-and-annotate)

### 5. 日常检索和客户端选择

用 `Ctrl+P` 按名称跳转到文献，用 `Ctrl+Shift+F` 搜索文献库；文件夹整理项目，标签标记关键词。[官方检索文档](https://gammapdf.com/docs/#search)

先通过 Web UI 完成基本测试。需要桌面端时，从 [GitHub Releases](https://github.com/tim4431/gamma/releases) 获取 Linux 安装包，连接同一个服务器；离线副本的设置见[官方文档](https://gammapdf.com/docs/#offline-copies)。

## 验证

- 通过隧道可以登录，上传的 PDF 可正常翻页和阅读。
- 高亮、笔记和阅读内容在刷新、重新登录后仍可访问。
- 管理员可在服务器运行下列命令，然后刷新客户端，确认 PDF 和批注仍保留：

```bash
cd ~/services/gamma
docker compose restart gamma
```

重启会短暂中断所有人的连接，执行前避开团队使用时间。多用户测试时，让两个账号在共享 Workspace 打开同一份测试文献，检查编辑同步和角色权限。
