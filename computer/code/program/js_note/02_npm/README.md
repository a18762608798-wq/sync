# 02 npm：装依赖和装 CLI

> npm 是 Node 默认包管理器。默认从 npm registry 下载包，平时无需改 registry。

```bash
npm --version
npm config get registry  # 查看当前 registry
npm config list          # 排查“找不到包 / 来源奇怪”时用
```

## local 与 global：最核心的概念

| 类型 | 命令 | 装到哪里 | 用途 |
|------|------|----------|------|
| 项目安装 | `npm install <pkg>` | `./node_modules/`，只服务当前项目 | 库、构建工具，如 `typescript` |
| 全局安装 | `npm install -g <pkg>` | nvm 下对应 Node 版本的 `lib/node_modules/` | CLI，如 `prettier`、`pi` |

```bash
npm install typescript                          # 项目级
npm install -g prettier                         # 得到 prettier 命令
npm install -g --ignore-scripts @earendil-works/pi-coding-agent  # 得到 pi 命令
```

> 只用 Agent / CLI 的用户，`npm install -g` 是最常用的 npm 用法。

## npx：不装也能跑一次

一句话：临时运行一个包提供的命令，不一定全局安装。

```bash
npx prettier file.js
npx some-tool
```

适合偶尔用一次、试用 CLI、跑项目级工具。每天都用的（如 `pi`）就全局装，偶尔跑一次的优先 `npx`。

## 全局包管理

```bash
npm ls -g --depth=0              # 查看已装全局包
npm install -g <pkg>             # 安装
npm install -g <pkg>@latest      # 确保装最新版
npm update -g <pkg>              # 升级
npm uninstall -g <pkg>           # 卸载
npm ls -g --depth=0 <pkg>        # 查看某一个
```

## 不要 `sudo npm`

用 nvm 时全局包本来就在用户目录（`~/.nvm/...`），不要：

```bash
sudo npm install -g ...
```

会导致 root-owned 文件、PATH 混乱、系统 Node 与 nvm Node 混用。若 `npm install -g` 提示要 sudo，先查环境配置，不要直接加 sudo。

## `--ignore-scripts` 是什么意思

包可定义 `preinstall / install / postinstall` 等生命周期脚本。`--ignore-scripts` 表示只装文件、不执行这些脚本，是一种安全措施。

```bash
npm install -g --ignore-scripts <pkg>
```

注意：有些包靠 install 脚本完成编译 / 下载。只在官方明确推荐时才加，不要默认给所有包加。
