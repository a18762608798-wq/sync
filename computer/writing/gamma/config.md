# 配置 Gamma

## 前提

部署目录为 `~/services/gamma`，由一个管理员维护服务。所有人的 PDF、笔记和账号保存在同一实例中，由 Gamma 管理访问权限。

## 内容

### 1. 创建 compose.yaml

以下命令用于首次创建配置；已有部署时先检查原文件，保留已有镜像、端口和数据卷设置。

```bash
cd ~/services/gamma
cat > compose.yaml <<'EOF'
services:
  gamma:
    image: ghcr.io/tim4431/gamma:latest
    container_name: gamma
    restart: unless-stopped
    ports:
      - "127.0.0.1:9001:9001"
    volumes:
      - gamma-data:/data

volumes:
  gamma-data:
EOF
```

此配置基于[官方 Compose 示例](https://github.com/tim4431/gamma/blob/main/docker-compose.yml.example)，只保留 Gamma 服务，将宿主机监听地址限制为回环地址，采用手动更新。

| 配置 | 作用 |
| --- | --- |
| `image` | 拉取官方镜像，无需本地编译 |
| `container_name: gamma` | 固定容器名，方便查看日志 |
| `restart: unless-stopped` | Docker 服务启动后自动恢复容器；手动停止的容器保持停止 |
| `127.0.0.1:9001:9001` | 宿主机仅通过本机端口接入，再由 SSH 转发给客户端 |
| `gamma-data:/data` | 用 Docker named volume 持久化用户、PDF、批注、笔记和数据库 |

`gamma-data` 不是服务目录里的普通文件夹。默认项目名为目录名 `gamma`，实际卷名通常是 `gamma_gamma-data`；`-p`、`COMPOSE_PROJECT_NAME` 或顶层 `name` 会改变前缀。

查看实际挂载和默认卷信息：

```bash
docker inspect gamma --format '{{json .Mounts}}'
docker volume inspect gamma_gamma-data
```

重建容器会保留数据卷。**不要使用 `docker compose down -v`，其中 `-v` 会删除持久化卷。**

### 2. 创建应用用户

管理员登录后进入 **Settings → Users**，创建账号、重置密码或调整管理员权限。Gamma 用户名可与 Linux 用户名不同；建议管理员账号用于管理，日常阅读使用普通账号。[官方用户管理说明](https://github.com/tim4431/gamma#docker-compose-recommended)

例如创建普通用户 `alice` 和 `bob`。两人分别通过自己的 Linux SSH 账号建立隧道，再使用各自的 Gamma 账号登录。

### 3. 管理 Workspace

进入 **Settings → Workspaces** 管理个人文献库；需要协作时，由管理员创建共享 Workspace，例如 `Research`，再由 Owner 管理成员。

| Workspace | 建议成员 | 用途 |
| --- | --- | --- |
| Alice 个人库 | alice | 保存个人 PDF 和笔记 |
| Bob 个人库 | bob | 保存个人 PDF 和笔记 |
| Research | 按需添加团队成员 | 团队共享阅读和批注 |

共享 Workspace 的 Owner 管理成员，Editor 编辑内容，Viewer 阅读内容。具体权限见[官方 Workspace 文档](https://gammapdf.com/docs/#workspaces)。

## 验证

```bash
cd ~/services/gamma
docker compose config
docker inspect gamma --format '{{json .HostConfig.PortBindings}}'
```

确认 `9001/tcp` 的 `HostIp` 为 `127.0.0.1`。分别用普通账号登录，检查个人库和共享库的可见范围；再用 Editor 和 Viewer 验证编辑权限。
