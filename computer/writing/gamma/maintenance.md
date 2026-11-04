# 备份、更新与排查

## 前提

下文 Docker 命令在服务器的 `~/services/gamma` 执行。更新会影响所有用户，先完成备份并安排维护时间；备份副本另存到其他磁盘或机器。

## 步骤

### 1. 创建备份

| 入口 | 用途 |
| --- | --- |
| Settings → Backups | 创建 Workspace 快照，按需设置定时任务 |
| Settings → Workspaces → Export | 导出整个 Workspace 的 ZIP，保存到其他位置 |
| Settings → Server（管理员） | 创建服务器级快照，覆盖整个实例 |

Workspace ZIP 可从 **Settings → Workspaces → Import** 恢复或合并；Workspace 快照从 **Settings → Backups** 回滚。服务器级恢复需要停止 Gamma，并按[官方安装说明](https://github.com/tim4431/gamma#docker-compose-recommended)中的 `manage.py backups --restore` 流程执行，不能用 Workspace 导入代替。

服务端快照若仍位于同一数据卷中，不能抵御整盘损坏；至少另存一份 Workspace ZIP，完整实例则按需配置异地备份。Gamma 还提供 S3 兼容存储的异地副本设置。[官方备份文档](https://gammapdf.com/docs/#backups-and-upgrades)

### 2. 手动更新

完成备份后，记录当前镜像，便于定位版本：

```bash
cd ~/services/gamma
docker inspect gamma --format '{{.Image}}'
docker image inspect ghcr.io/tim4431/gamma:latest --format '{{json .RepoDigests}}'
```

再拉取镜像并重建容器：

```bash
cd ~/services/gamma
docker compose pull
docker compose up -d
```

`latest` 是浮动标签，拉取后可能对应新构建。此配置没有 Watchtower，运行中的容器不会自行拉取更新。更新保留原数据卷，但新版本可能迁移数据；不要直接用旧镜像打开已经迁移的数据。若页面要求先运行中间版本，按其提示处理。[官方更新说明](https://github.com/tim4431/gamma#docker-compose-recommended)

### 3. 查看状态与日志

```bash
cd ~/services/gamma
docker compose ps
docker compose logs --tail=100 gamma
```

### 4. 临时停止与恢复

```bash
cd ~/services/gamma
docker compose stop gamma
```

需要恢复时执行：

```bash
cd ~/services/gamma
docker compose up -d
```

停止服务不删除数据卷。日常维护不使用 `docker compose down -v`，也不清理 Gamma 数据卷。

### 5. 常见问题

| 现象 | 检查方向 |
| --- | --- |
| `docker info` 权限不足或连不上 | 检查 Docker 服务与部署管理员权限，必要时使用 `sudo docker` |
| 镜像下载失败 | 检查服务器到 `ghcr.io` 的网络，再重试启动 |
| 浏览器打不开 | 查看容器状态、SSH 终端及本地转发端口；客户端和浏览器必须在同一电脑 |
| SSH 报本地端口占用 | 将本地端口改为 `19001`，浏览器和 MCP URL 一起调整 |
| 新建容器后文献库为空 | 检查 Compose 项目名和 `/data` 挂载，确认是否误用了新卷，保留原卷 |
| 日志里没有初始密码 | 已有数据不会再次生成密码；由现有管理员重置账号密码，勿重建空卷找回密码 |
| MCP 授权失败 | 检查隧道、MCP URL、Public server URL，以及浏览器可达的授权地址 |

## 验证

更新后确认容器正常运行，重新登录并打开已有 PDF，检查高亮和笔记；备份后在独立测试 Workspace 试导入 ZIP，确认 PDF 和批注可读取。
