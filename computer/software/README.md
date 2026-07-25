## 1.1 封面制备

```desktop
[Desktop Entry]
Type=Application
Name=ViTables
Exec=/home/Hanyijie/Desktop/Synchronous_space/software/vitables/vitables.sh
Icon=
Comment=Start ViTables
Terminal=false
Categories=Development;
```

### 把文件desktop复制到~/.local/share/applications，否则一堆问题。

```bash
   cp desktop ~/.local/share/applications/
```

### 放权限，更新

```bash
   chmod +x ~/.local/share/applications/typora-open.desktop
   update-desktop-database ~/.local/share/applications
```

### 设置默认（选择）

```shell
   xdg-mime default ~/.local/share/applications/typora-open.desktop text/markdown text/x-markdown
```

## 1.2 AppImage

1. **提取 `.deb` 文件**：
   ```bash
   dpkg-deb -x clash-verge_1.7.7_amd64.deb clash-verge-appdir/
   ```

2. 执行文件显然在/home/hanyijie/下载/clash-verge-appdir/usr/bin/clash-verge

3. 根据你提供的信息，可执行文件位于 `clash-verge-appdir/usr/bin/clash-verge`。我们需要确保 AppRun 脚本能够正确指向这个可执行文件，并设置必要的环境变量。下面是一个示例 AppRun 脚本的创建过程，你可以在你的系统上修改和使用它：

   1. **编写 AppRun 脚本**：
      - 在 `clash-verge-appdir` 目录中创建一个名为 `AppRun` 的文件。
      
   ```bash
      nano clash-verge-appdir/AppRun
      ```
      
      - 编辑这个文件，加入以下内容：
      
      ```bash
   #!/bin/bash
      HERE=$(dirname $(readlink -f "${0}"))
   export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"
      exec "$HERE/usr/bin/clash-verge" "$@"
      ```
      
      - 这个脚本设置了动态链接器的库路径，然后执行主程序。
      
   2. **使 AppRun 脚本可执行**：
      - 通过运行以下命令来使脚本可执行：

      ```bash
      chmod +x clash-verge-appdir/AppRun
      ```

   3. **生成 AppImage**：
      
   * 安装'appimagetool'
      
      ```
      ~/下载/appimagetool-x86_64.AppImage clash-verge-appdir/ clash-verge.AppImage
   ```
      
      - 创造desktop，已经给出教程。
      - 确保你已经安装了 `appimagetool`，然后运行以下命令：
      
      ```bash
      appimagetool clash-verge-appdir/ clash-verge.AppImage
      ```
      
      - 这将创建一个名为 `clash-verge.AppImage` 的文件，你可以在任何支持的 Linux 发行版上运行它。

   
