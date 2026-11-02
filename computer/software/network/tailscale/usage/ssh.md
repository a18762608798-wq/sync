# ssh

## 两台电脑都要做：

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale status
tailscale ip -4  # 记下 100.x.y.z
```

## 被控端（要被 SSH 连的那台）：

```bash
sudo apt install -y openssh-server # 装 OpenSSH 服务端，提供 sshd，这台机器才能被 SSH 连。不装的话只有 ssh 客户端，只能连别人。
sudo systemctl enable --now ssh # 保证开机自启：开机自启. 
# 只放行 Tailscale 网卡，不暴露公网 22 端口
sudo ufw allow in on tailscale0 to any port 22 proto tcp # 限制只有tailscale网络可以共享.
```

## 主控端直接连：

```bash
# 用 Tailscale IP 最稳，MagicDNS 开了也能用主机名
ssh 用户名@100.x.y.z
ssh 用户名@主机名  # 如 my-pc.tailxxxx.ts.net, 等价于第一种.
tailscale ping 对端主机名 # 先测组网通没通
```

## ~/.ssh/config 省事写法(控制位写)：

```text
Host mypc
  HostName 100.x.y.z
  User dell
  IdentityFile ~/.ssh/id_ed25519
```

之后 ssh mypc、VSCode Remote-SSH 选 mypc就行。
