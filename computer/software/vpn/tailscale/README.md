贴出来，我帮你判断有没有改善 👍

# 关于tailscale:

## 部署
* ✅ 1️⃣ 安装

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

* ✅ 2️⃣ 启动 + 登录

```bash
sudo tailscale up
```

👉 会弹浏览器，用 Google / GitHub 登录一下

* ✅ 3️⃣ 确认连上

```bash
tailscale status
```
## 一般功能

👉 能看到一个 `100.x.x.x` 的 IP 就行

# 连接
sudo tailscale up

# 断开
sudo tailscale down

# 查看状态
tailscale status

# 完全退出
sudo tailscale logout

