# 使用

核心模型：`Tailnet = 你的私有虚拟局域网`，同账号设备各拿一个 `100.x`（CGNAT，仅 tailnet 内可达），设备间自动加密直连，打不通时自动走 DERP 中继。

## 前提

- 已 `sudo tailscale up` 并登录。
- 对端也在同一 tailnet（如本机 `mintsystem 100.110.207.103` + 手机 `100.74.17.75`）。

## 内容

### 1. 查看全网状态

一句话：看谁在线、谁是什么 IP。

```bash
tailscale status
```

本机实测输出示例：

```text
100.110.207.103  mintsystem  linux
100.74.17.75     vyg-al30    android
```

### 2. 看本机 Tailscale IP

```bash
tailscale ip
```

本机输出：`100.110.207.103` + `fd7a:...`。

连接示例（**需要登录同一个tailscale帐号或者组织共享**）：

```bash
ssh mintusr@100.110.207.103
```

### 3. 测走直连还是中继

一句话：`tailscale ping` 会告诉你是 `direct` 还是 `via DERP`。

```bash
tailscale ping --c=2 100.74.17.75
```

本机实测（手机走中继）：

```text
pong from vyg-al30 (100.74.17.75) via DERP(lax) in 400ms
direct connection not established
```

记住：`direct = 最佳`，`via DERP(...) = 能用但慢`。

### 4. 查本机网络 NAT 类型

一句话：打洞失败时定位是本机 UDP / 防火墙问题还是对端问题。

```bash
tailscale netcheck
```

本机关键输出：`UDP: true`，`Nearest DERP: Hong Kong`。`UDP true` 说明本机允许打洞。

### 5. 连接 / 断开 / 完全退出

一句话：日常只用 `up/down`，换账号才用 `logout`。

```bash
sudo tailscale up
sudo tailscale down
sudo tailscale logout
```

## 验证

- `tailscale status` 能看到 `100.x` 即在线。
- `tailscale ping <对端100.x>` 出 `pong` 即链路通，再看是 `direct` 还是 `via DERP` 判断性能。
- 浏览器/SSH 访问 `http://100.110.207.103:<端口>` 只有同 tailnet 设备能打开，外网打不开即符合安全预期。
