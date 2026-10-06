# TeamViewer 使用

## 前提

- 本机环境：Linux Mint 22.3，TeamViewer 15.82.6（DEB）。
- 远程无人值守访问需先完成 [config.md](config.md) 中的 Easy Access 设置。

## 步骤 / 内容

1. **启动客户端**：从应用菜单打开 TeamViewer，或在终端运行：

   ```bash
   teamviewer
   ```

2. **查看版本和后台状态**：

   ```bash
   teamviewer --version
   teamviewer daemon status
   ```

   后台服务正常时应显示 `active (running)`。

3. **临时协助（需要远端提供当次密码）**：控制端打开“远程支持（Remote Support）”，在“提供支持（Provide support）”中输入对方 ID 并连接，再输入对方提供的密码；若别人要临时连接本机，可在本机 TeamViewer 的“允许远程控制”区域查看本机 ID 和当前密码，只分享给可信的人。

4. **连接已配置的 Mint 电脑（无需读取随机密码）**：控制端登录绑定设备的 TeamViewer 账号，打开“设备（Devices）→ 所有受管理设备（All managed devices）”，选择这台 Mint 电脑并点击“Easy Access/连接”。

官方操作说明：[通过 ID 和密码连接](https://www.teamviewer.com/en-us/global/support/knowledge-base/teamviewer-remote/remote-control/connect-via-id-and-password/) · [查找本机 ID 和密码](https://www.teamviewer.com/en-us/global/support/knowledge-base/teamviewer-remote/remote-control/where-to-find-my-id-and-password/)。

## 验证

运行 `teamviewer --version` 应显示已安装版本；无人值守使用时，从控制端通过设备列表连接，且不需要本机人员提供随机密码或点击接受。
