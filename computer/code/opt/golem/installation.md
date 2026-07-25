好的，我们来用中文梳理一下在 **Ubuntu** 上如何安装和运行 **Golem**（出售算力）：

---

## 🧩 一、Golem 简介

Golem 是一个分布式算力共享网络，你可以让你的电脑“出租”空闲 CPU/GPU 资源，赚取 **GLM 代币**（以太坊上的代币）。

在 Ubuntu 上，目前主要通过命令行（CLI）运行，还没有官方 GUI（图形界面）。不过命令行方式非常简单。

---

## ⚙️ 二、系统要求

你的配置（4 核 8 线程，10 GB RAM）完全够用。最低要求：

- 操作系统：Ubuntu 20.04 / 22.04（64 位）  
- CPU：支持虚拟化（Intel VT-x 或 AMD-V，需在 BIOS 中开启）  
- 内存：≥ 4 GB  
- 硬盘：≥ 20 GB  
- 网络：需要稳定的网络，最好能打开 UDP 11500 端口（用于连接其他节点）  

---

## 🧠 三、安装步骤

打开终端，执行一条命令即可：

```bash
curl -sSf https://join.golem.network/as-provider | bash -
```

它会自动下载并安装 Golem 节点程序（核心组件叫 **Yagna**，管理命令叫 `golemsp`）。

安装完后，更新你的环境变量（只需做一次）：（一般系统添加过了。）

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
source ~/.profile
```

---

## 🚀 五、启动 Golem 提供算力

执行：

```bash
golemsp run
```

如果一切正常，会看到日志输出，例如：

```
INFO Starting provider service...
INFO Connected to mainnet
INFO Node ready and offering resources
```

你的节点现在已经上线并在 Golem 网络上提供算力！

> 想让它后台运行，可使用：
> ```bash
> screen -S golem bash -c "golemsp run"
> ```
> 然后按 `Ctrl + A + D` 让它在后台继续运行。

---

## 📊 六、查看状态与收益

查看节点状态：

```bash
golemsp status
```

输出示例：

```
Status: running
Version: 0.17.0
Wallet: 0xabc123...
Network: mainnet
Balance: 0.00 GLM

```

如果开始处理任务，这里会显示“processed tasks”的数量。

---

## 🧮 七、资源与价格调整

查看当前配置：

```bash
golemsp settings show
```

修改共享资源：

```bash
golemsp settings set --cores 7 --memory 8GiB --disk 50GiB
```

修改价格：

```bash
# 降 CPU 小时价到 0.00005 GLM/CPU·h
golemsp settings set --cpu-per-hour 0
# 降环境小时价到 0.000005 GLM/h
golemsp settings set --env-per-hour 0
# 启动费设 0
golemsp settings set --starting-fee 0
# 让新价格生效
golemsp stop
golemsp run
```

0.00001；0.000005 应该是正常的，头一个星期定低一点？

修改完后重启节点：

```bash
golemsp run
```

---
删除旧的钱包

## 八 VM 模式

一般自动开启。


