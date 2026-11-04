# 安装 Gamma

## 前提

采用 Docker Compose、单个 Gamma 服务、多个 Gamma 用户，通过 SSH 隧道访问。服务器无需图形界面，普通使用者只需 SSH 账号和 Gamma 账号。

本文按 Ubuntu 工作站场景整理，也适用于已配置 Docker Engine 和 Compose 插件的 Linux Mint。官方资料核对日期：2026-11-04；镜像采用浮动标签 `latest`，具体版本以部署时拉取的镜像为准。

编写时本机为 Ubuntu 24.04、`x86_64`，已验证 Docker CLI 29.9.3 和 Compose v5.7.0 可执行。本文未实际拉取、启动或登录 Gamma，部署后按下文及[使用文档](usage.md)验收。

## 步骤

### 1. 检查 Docker

以下命令在服务器执行：

```bash
docker --version
docker compose version
docker info
```

`docker info` 应能正常连接 Docker Engine。尚未安装时参考仓库中的 [Docker 安装文档](../../development/docker/installation.md)。如果当前管理员仅能通过 `sudo` 使用 Docker，后续 Docker 命令也加 `sudo`；其他用户无需加入 `docker` 组。

### 2. 建立部署目录

```bash
mkdir -p ~/services/gamma
cd ~/services/gamma
```

按[配置文档](config.md#1-创建-composeyaml)创建 `~/services/gamma/compose.yaml`。文档目录 `writing/gamma/` 与实际服务目录分开保存。

### 3. 检查配置并启动

```bash
cd ~/services/gamma
docker compose config
```

确认输出的宿主机绑定地址为 `127.0.0.1`、端口为 `9001`，再启动：

```bash
docker compose up -d
```

首次启动会拉取镜像，耗时取决于网络。基础安装无需设置 AI Key 或管理员密码环境变量。

### 4. 查看初始管理员密码

```bash
docker compose ps
docker compose logs --tail=50 gamma
docker logs gamma
```

全新数据目录会自动创建 `admin`，随机密码仅在创建账号时写入日志；后续启动不会重新生成。首次登录后修改密码，勿将含密码的日志提交到仓库或公开分享。[官方安装说明](https://github.com/tim4431/gamma#quickstart)

## 验证

- `docker compose ps` 显示 Gamma 正在运行，端口映射为 `127.0.0.1:9001->9001/tcp`。
- 日志没有持续报错或反复重启。
- 按[使用文档](usage.md)建立 SSH 隧道，登录并完成 PDF 批注测试。
