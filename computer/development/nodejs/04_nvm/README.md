# 04 nvm：版本管理与最大的坑

> nvm = Node Version Manager。它不是 Node，也不是 npm，只负责安装、切换、删除不同版本的 Node。首次安装见 [01_install](../01_install/)。

## 常用命令

```bash
nvm --version              # nvm 自身版本
nvm ls                     # 查看已安装的 Node
nvm install 24             # 装指定大版本
nvm install --lts          # 装最新 LTS
nvm use 24.20.0            # 切换版本（当前 shell 生效）
nvm alias default 24.20.0  # 设默认版本
nvm uninstall 22.23.0      # 删旧版本
```

## 坑：切换 Node 后全局 CLI“消失”

nvm 的目录结构大致是：

```text
~/.nvm/versions/node/
├── v22.x/
│   ├── bin/
│   └── lib/node_modules/   # Node 22 的全局包
└── v24.x/
    ├── bin/
    └── lib/node_modules/   # Node 24 的全局包
```

复现：

```bash
nvm use 22
npm install -g foo   # foo 属于 Node 22

nvm use 24
foo                  # 找不到，不是 PATH 坏了，是本来就是两套全局包
```

结论：不做 Node 开发就只保留一个 LTS，避免多版本维护成本。

## 更新 Node 后的检查

```bash
nvm install --lts
```

新版本不会继承旧版本的全局包。更新后检查缺了什么，重装即可：

```bash
npm ls -g --depth=0
npm install -g --ignore-scripts @earendil-works/pi-coding-agent  # 示例
```
