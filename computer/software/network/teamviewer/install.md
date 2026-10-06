# 安装 TeamViewer

## 前提

- 本说明适用于本机的 **Linux Mint 22.3（Zena）、x86_64**。本机当前实测安装版本为 **TeamViewer 15.82.6（DEB）**。
- 官方 Linux 安装说明列出的 Mint 版本为 Mint 21；本机为 64 位，应选择 AMD64 `.deb` 包。
- 从 TeamViewer 官方 Linux 下载页选择 Ubuntu/Debian 的 64 位 `.deb` 完整客户端。需要无人值守访问时，不要下载 QuickSupport。

## 步骤 / 内容

1. 打开 [TeamViewer Linux 下载页](https://www.teamviewer.com/en-us/download/linux/)，下载 Ubuntu/Debian 64 位完整客户端 `.deb`。
2. 图形界面安装：在“下载”目录双击 `.deb` 文件，选择软件安装器并点击安装。
3. 也可以在终端安装。先将尖括号占位符替换为下载文件的实际完整文件名（包含 `.deb`）：

   ```bash
   cd ~/Downloads
   sudo apt install ./<TeamViewer完整安装包文件名.deb>
   ```

   例如，若文件名是 `teamviewer_15.82.6_amd64.deb`，就把占位符替换为该文件名。

4. 从 Mint 应用菜单启动 TeamViewer，或在终端运行 `teamviewer`。

官方说明：[Linux 安装说明](https://www.teamviewer.com/en-us/global/support/knowledge-base/teamviewer-remote/download-and-installation/linux/install-teamviewer-classic-on-linux)。

## 验证

检查安装版本和后台服务：

```bash
teamviewer --version
teamviewer daemon status
```

本机输出版本为 `15.82.6 (DEB)`；服务状态应显示 `active (running)`，并已设置为开机启动（`enabled`）。
