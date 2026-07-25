太棒了 🎯！你选 **A** ——用主网（Polygon）在 Golem 上跑一个超小任务。  
下面是完整但最小化、可直接复制执行的步骤。

---

## ✅ 前提检查
1. 你的钱包里已经有 GLM 和少量 MATIC（用于 gas）。  
2. Python 3.9 或更高版本。  
3. 已安装 `yapapi` SDK：  
   ```bash
   pip install yapapi
   ```

---

## 🧠 测试脚本（main.py）
在任意目录下新建文件 `main.py`：

---

## 🚀 运行任务

依赖：二进制传输工具。
sudo apt-get update
sudo apt-get install cmake cargo
2) 安装 gftp 
# 用 crates.io(rust) 安装 gftp 可执行文件
cargo install gftp --features bin --locked

 3) 确认版本并加入 PATH（~/.cargo/bin）
~/.cargo/bin/gftp --version
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.profile
source ~/.profile


需要逆天密钥

1. 生成一个新的应用密钥
yagna app-key create "yapapi-demo"
#b83e224dc7474c2d940620b3fec164d7

2. 临时导出为环境变量（仅当前终端有效）
export YAGNA_APPKEY=b83e224dc7474c2d940620b3fec164d7 # 这个直接放代码里面的命令我还不知道。


让 yapapi 默认使用 polygon 网络（而不是 testnet）
export YAGNA_NETWORK=polygon

yagna payment release-allocations


在保存脚本的目录执行：
cd ~/sync/computer/code/opt/golem

```bash
python main.py # vpn开全局模式
```

首次运行时可能看到：
- `Negotiating agreements with providers...`
- `Sending task...`
- `Task finished successfully...`

最终输出应类似：
```
Result: Hello Golem!
```

这表示你在 Polygon 主网上完成了真实的 Golem 计算任务 🎉。yapapi 的 execute_tasks 默认按任务提交顺序输出结果.

---

## 💰 验证支付记录
任务结束后查看付款情况：

```bash
yagna payment status --driver erc20 --network polygon
```

你会看到 `outgoing` 栏增加了一点点 GLM（几乎可以忽略）。

---

## 🧩 说明
- **预算 `budget=0.01`** 表示最多花 0.01 GLM；你也可以调低。  还有其他参数，懒着弄了。
- 所有交易均在 Polygon 上完成，用你的 0x7adc… 钱包。  
- 如果以后想运行复杂任务（Python、容器等），只需改脚本里的命令或用官方模板即可。

---

想不想我帮你把这个示例升级成能在 Golem 上运行一段 Python 计算（比如 计算 π 或 矩阵乘法）？  
那样可以更明显地看到真实计算和日志输出。