# 安装

本机版本：`1.102.4`，Linux Mint（apt 源对应 `ubuntu noble`）。

## 前提

- Linux Mint，已联网。
- 有 `sudo` 权限。
- 已安装 `curl`（Mint 默认自带）。

## 步骤

1. 执行官方安装脚本（会自动加 apt 源并安装）：

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

本机实际写入的 apt 源：

```text
deb [signed-by=/usr/share/keyrings/tailscale-archive-keyring.gpg] https://pkgs.tailscale.com/stable/ubuntu noble main
```

2. 启动并登录：

```bash
sudo tailscale up
```

会输出登录链接，在浏览器用 Google / GitHub 登录即可。

3. 开机自启（安装后默认已启用，无需手动操作）：

```bash
systemctl is-enabled tailscaled
```

## 验证

```bash
tailscale version
```

本机输出 `1.102.4` 即成功。

```bash
systemctl is-active tailscaled
```

输出 `active` 即后台服务正常。

```bash
tailscale status
```

能看到本机 `100.x.x.x`（如本机 `100.110.207.103 mintsystem`）即已入网。
