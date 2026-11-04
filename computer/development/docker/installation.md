# Docker 安装

通过 Docker 官方 APT 仓库安装 Docker Engine，适用于 Ubuntu 和基于 Ubuntu 的 Linux Mint。Linux Mint 使用下面命令中的 `UBUNTU_CODENAME` 获取 Ubuntu 基础版本代号，无需写死为 `noble`；LMDE 不适用本文的 Ubuntu 仓库配置。

## 1. 检查旧安装（如有）

如果安装过发行版提供的 Docker 或容器运行时包，先检查是否存在冲突：

```bash
dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc
```

如果有已安装的冲突包，使用 `sudo apt remove 包名` 卸载对应包，再继续安装。已有的官方 `docker-ce` 安装可以通过下文命令更新，无需先卸载或清空数据目录。

如果按旧版本文创建过 `docker.list`，先将旧源文件改名停用，避免与新的 `docker.sources` 重复或产生 `Signed-By` 冲突：

```bash
if [ -f /etc/apt/sources.list.d/docker.list ]; then
  sudo mv -n /etc/apt/sources.list.d/docker.list \
    "/etc/apt/sources.list.d/docker.list.disabled-$(date +%Y%m%d-%H%M%S)"
fi
```

## 2. 配置 Docker 官方 APT 仓库

使用 `.sources` 格式保存仓库配置，直接下载 ASCII 格式的 GPG 密钥到 `docker.asc`。

```bash
# 更新软件源
sudo apt update

# 安装依赖
sudo apt install -y ca-certificates curl

# 创建密钥目录
sudo install -m 0755 -d /etc/apt/keyrings

# 下载 Docker 官方 GPG 密钥
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

# 添加 Docker 官方 APT 仓库
sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# 更新软件源索引
sudo apt update
```

## 3. 安装 Docker

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

这些包包含 Docker Engine、命令行工具、containerd、Buildx 和 Compose 插件。

## 4. 验证安装

```bash
sudo systemctl status docker
sudo docker --version
sudo docker compose version
sudo docker run hello-world 
```

如果 Docker 服务未运行，执行 `sudo systemctl start docker`。`hello-world` 会下载测试镜像并运行容器，输出成功消息后退出。

## 5. 配置非 sudo 运行（可选）

```bash
sudo usermod -aG docker "$USER"
```

注销后重新登录，使组成员变更生效，然后运行 `docker run hello-world` 验证。`docker` 组成员拥有等同于 root 的权限，仅将可信用户加入该组。

参考：[Docker 官方 Ubuntu 安装文档](https://docs.docker.com/engine/install/ubuntu/)、[Linux 安装后配置](https://docs.docker.com/engine/install/linux-postinstall/)。

