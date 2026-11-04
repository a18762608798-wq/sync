# 通过 Tailscale 用 SSH 连接本机

本机作为被控端，主控端指发起 SSH 连接的另一台设备。这里使用 Tailscale 组网承载普通 OpenSSH，认证仍由 OpenSSH 负责，无需开启额外的 Tailscale SSH 功能。[官方说明](https://tailscale.com/docs/reference/ssh-over-tailscale)

## 本机配置

以下信息于 `2026-11-04` 核实：

| 项目 | 本机值 |
| --- | --- |
| 系统 | Ubuntu 24.04.3 LTS |
| 主机名 | `dell-Precision-7875-Tower` |
| SSH 用户名 | `dell` |
| Tailscale IPv4 | `100.107.33.112` |
| MagicDNS 完整域名 | `dell-precision-7875-tower.taila2e529.ts.net` |
| SSH 端口 | `22` |

- Tailscale 已登录并在线，`tailscaled` 服务正在运行，已启用开机自启。
- OpenSSH 服务端已安装，`ssh` 服务正在运行，已启用开机自启。
- 本机访问自身 Tailscale IP 的 `22` 端口，已收到正常 OpenSSH 响应；跨设备登录还需在主控端实际测试。

本机无需重复安装 Tailscale 或 `openssh-server`，可直接按下一节连接。

## 在主控端连接

前提：主控端已安装并启动 Tailscale，登录同一 tailnet（个人设备可使用同一 Tailscale 账号），且 tailnet 的访问策略允许主控端访问本机的 TCP `22` 端口。

在主控端终端执行：

```bash
# 检查到本机的 Tailscale 链路
tailscale ping 100.107.33.112

# SSH 登录本机
ssh dell@100.107.33.112
```

`dell` 是本机 Linux 用户名。按本机 OpenSSH 的认证配置，使用 `dell` 账户密码或已授权的 SSH 密钥登录。

如果主控端能正常解析 MagicDNS，也可以使用完整域名：

```bash
ssh dell@dell-precision-7875-tower.taila2e529.ts.net
```

## 在主控端配置快捷连接

将以下内容加入**主控端**的 `~/.ssh/config`：

```sshconfig
Host precision7875
  HostName 100.107.33.112
  User dell
  Port 22
  # 若使用此私钥，且对应公钥已在本机授权，可取消下一行注释
  # IdentityFile ~/.ssh/id_ed25519
```

之后可执行：

```bash
ssh precision7875
```

VS Code Remote-SSH 也可选择 `precision7875`。

## 在本机检查状态

以下命令在**被控端，也就是本机**执行：

```bash
tailscale status
tailscale ip -4
systemctl is-active tailscaled ssh
systemctl is-enabled tailscaled ssh
ss -ltn '( sport = :22 )'
```

正常情况下，IP 为 `100.107.33.112`，两个服务均为 `active`，自启状态均为 `enabled`，端口列表中能看到 `22` 正在监听。如果重新入网后 IP 发生变化，应同步更新主控端连接命令和 SSH 配置。

仅当服务未运行或未启用自启时，在本机执行：

```bash
sudo systemctl enable --now tailscaled ssh
```

如果 Tailscale 已退出登录或被断开，再执行以下命令并按提示登录：

```bash
sudo tailscale up
```

## 防火墙现状

- SSH 当前监听 `0.0.0.0:22` 和 `[::]:22`，即所有 IPv4、IPv6 接口。
- `/etc/ufw/ufw.conf` 当前为 `ENABLED=no`；核实时未取得需要 `sudo` 的运行时规则，不能据此断言其他防火墙规则的状态。
- 单独添加 `ufw allow in on tailscale0 to any port 22 proto tcp` 只会增加允许规则，不会启用 UFW，也不会自动禁止其他网卡上的 SSH 访问。[Ubuntu 官方说明](https://ubuntu.com/server/docs/firewalls/)

因此，当前配置不能描述为“只有 Tailscale 能连接 SSH”。若要限制其他网络的访问，需要另行结合现有防火墙规则和其他服务配置。通过 Tailscale 连接无需在路由器上设置公网 `22` 端口映射。[Tailscale 官方说明](https://tailscale.com/docs/reference/ssh-over-tailscale)

## 常见问题

- `tailscale ping` 不通：先确认两端 Tailscale 在线、加入同一 tailnet，以及目标 IP 是否正确。
- SSH 超时或拒绝连接：检查本机 `ssh` 服务、`22` 端口监听，以及 tailnet 访问策略和防火墙规则。`tailscale ping` 成功不代表 TCP `22` 一定可达。
- `Permission denied`：检查用户名是否为 `dell`，以及账户密码或 SSH 公钥授权是否正确。
