# 计算机工具与使用笔记

按用途查找；同一工具的安装、配置、使用和示例集中在一个主题目录。

| 目录 | 内容 | 常用入口 |
| --- | --- | --- |
| [development](development/README.md) | 编程语言与开发工具 | [Python](development/python/README.md)、[Julia](development/julia/README.md)、[Node.js](development/nodejs/README.md)、[Git](development/git/README.md) |
| [writing](writing/README.md) | 写作、排版、演示与文献管理 | [LaTeX](writing/latex/README.md)、[Quarto](writing/quarto/README.md)、[Slidev](writing/slidev/README.md)、[Zotero](writing/zotero/README.md) |
| [system](system/README.md) | 操作系统、文件系统与系统维护 | [Linux](system/linux/README.md)、[Windows](system/windows/README.md)、[Android](system/android/README.md) |
| [network](network/README.md) | 网络连接、远程访问与文件同步 | [Tailscale](network/tailscale/README.md)、[Syncthing](network/syncthing/README.md) |
| [apps](apps/README.md) | 其他应用与软件入口 | [Ollama](apps/ollama/README.md)、[HDFView](apps/hdfview/README.md)、[常用软件](apps/common-apps.md) |
| [hardware](hardware/README.md) | 硬件知识 | [计算机硬件](hardware/计算机硬件.ipynb) |

## 收纳规则

- 先按用途选择分区，再按语言或工具收纳。写作工具放 `writing/`，挂载、字体、swap 等系统维护资料放 `system/linux/`。
- 每个主题只有一个主目录。安装、配置、使用资料在该目录内逐步扩展；内容少时保留一篇笔记即可。
- 示例项目连同依赖声明、锁文件、配置和图片整体保存。Julia、Python 的既有编号结构继续使用。
- 新增目录使用小写英文，多个单词用连字符连接。工具目录名保持稳定，版本信息记录在正文中。
- 图片、模板、安装器随主题保存。已有导出文件保留；新增构建缓存与日志遵循忽略规则。
- 明确属于某主题的零散记录放入该主题的 `00_inbox/`；整理后补充到对应正文。

## 本次整理

`code/` 中的编程资料迁入 `development/`，写作资料迁入 `writing/`；`software/` 中的资料按具体用途归入各分区。挂载笔记归入 [文件系统](system/linux/filesystems/README.md)，原 Ubuntu 笔记按安装、字体、快捷键和内存管理分别收纳。

安装器、模板和历史导出文件均保留。有明确主题的空白笔记保留；无内容的占位文件已移入系统回收站。此次调整目录和导航，原有安装命令及软件版本信息仍需在实际使用时核实。
