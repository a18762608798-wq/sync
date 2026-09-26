# 配置

Tailscale 在 Linux 本机几乎无配置文件，配置 = `tailscale up` 参数 + Admin Console 开关。

## 前提

- 已按 `install.md` 安装，本机版本 `1.102.4`。
- 已执行过一次 `sudo tailscale up` 并登录。

## 内容

### 1. 本机配置文件位置

```text
/etc/default/tailscaled
```

本机实测内容：

```bash
cat /etc/default/tailscaled
```

```text
PORT="41641"
FLAGS=""
```

- `PORT`：UDP 打洞监听端口，远端自动感知，一般不用改。
- `FLAGS`：传给 `tailscaled` 的额外参数，一般留空。
- 改完后重启生效：`sudo systemctl restart tailscaled`。

### 2. 关键配置项（`tailscale up` 参数）

| 参数 | 一句话说明 |
| --- | --- |
| （无参） | 默认加入 tailnet，默认互通 |
| `--hostname=<名字>` | 指定在 tailnet 中的机器名 |
| `--ssh` | 开启 Tailscale SSH，可免 22 端口公网暴露 |
| `--advertise-exit-node` | 本机作为出口节点，供其他设备经本机上网 |
| `--accept-routes` | 接受其他设备发布的子网路由 / 出口节点 |

最小可用配置示例（本机当前即此状态）：

```bash
sudo tailscale up
```

指定机器名 + 开启 SSH 示例：

```bash
sudo tailscale up --hostname=mintsystem --ssh
```

### 3. Admin Console 配置（网页端）

地址：`https://login.tailscale.com/admin/dns`

- `MagicDNS`：开启后可用机器名代替 `100.x`，如 `ssh mintusr@mintsystem`。
- `ACL`：默认同 tailnet 全互通，个人单用户不用改。

## 验证

```bash
tailscale status
```

能看到 `100.110.207.103 mintsystem` 即配置生效。

```bash
tailscale ip
```

输出 `100.x` + `fd7a:...` 即网络已就绪。
