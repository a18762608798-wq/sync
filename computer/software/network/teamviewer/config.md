# TeamViewer 配置

## 前提

- 已安装 TeamViewer 完整客户端，并拥有 TeamViewer 账号。
- **无人值守访问需要在 Mint 电脑旁完成一次设置**；先设置好再离开，之后不需要有人在远端读出随机密码或点击接受。

## 步骤 / 内容

### 推荐：用 Easy Access（轻松访问）免输主机密码

1. 在 Mint 电脑打开 TeamViewer；如果尚未登录，先登录自己的 TeamViewer 账号。
2. 点击右上角齿轮进入**设置**，打开**常规（General）**。
3. 向下找到**管理此设备（Manage this device）**，点击它并按提示登录/确认账号。完成后，该电脑会关联到你的账号并配置无人值守访问。
4. 在控制端登录**同一个 TeamViewer 账号**，进入“设备（Devices）”查看这台 Mint 电脑。具体连接步骤见 [usage.md](usage.md)。

若客户端显示的是旧式界面，可在“远程控制（Remote Control）”页点击“授予轻松访问（Grant Easy Access）”，登录账号并点击“Assign”。

### 保持电脑可连接

- Mint 电脑要保持开机、联网，并避免进入睡眠/挂起状态；关机或休眠时无法远程连接。
- 检查 TeamViewer 后台服务：

  ```bash
  teamviewer daemon status
  ```

  服务应为 `active (running)`，并随系统启动。

### 安全建议

- 给 TeamViewer 账号启用两步验证，并使用强密码；不要把账号密码交给他人。
- Easy Access 设置完成后，优先通过账号设备列表连接。随机密码用于临时协助；不要把它公开分享。

官方说明：[无人值守访问设置](https://www.teamviewer.com/en-us/global/support/knowledge-base/teamviewer-remote/remote-control/provide-unattended-remote-support/) · [Easy Access](https://www.teamviewer.com/en/global/support/knowledge-base/teamviewer-classic/remote-control/connection-methods/remote-control-via-easy-access)。

## 验证

在另一台设备登录同一个 TeamViewer 账号，进入“设备（Devices）”并找到这台 Mint 电脑。通过“Easy Access/轻松访问”发起连接；若设置成功，不需要在 Mint 电脑旁输入当次随机密码或接受连接。
