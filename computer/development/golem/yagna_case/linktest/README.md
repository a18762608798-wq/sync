# 测试需要js环境，穿透需要公网IP.

## js 环境：Ubuntu 安装 Node + npm（最稳的方法）

用 NodeSource：

```bash
sudo apt update
sudo apt install -y curl

curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```
不行就用默认的版本足够。

* ✅ 验证

```bash
node -v
npm -v
```

👉 应该看到类似：

```bash
v20.x.x
10.x.x
```


* ✅ 创建项目（你要跑 golem-js 必须）

```bash
mkdir golem-js-test
cd golem-js-test

npm init -y
npm install @golem-sdk/golem-js
```

---

* ✅ 关键（不然 import 会报错）

```bash
npm pkg set type=module
```

---

* ✅ 运行脚本

```bash
node test.mjs
```

## 公网IP

* 测试sessions(p2p而非 relay)

mintusr@mintusr-Lenovo-V14-G1-IML:~$ yagna net status
bandwidth:
  inAvgKiBps: '0.00'
  inKiBps: '0.00'
  inMib: '0.00'
  outAvgKiBps: '0.00'
  outKiBps: '0.00'
  outMib: '0.00'
listenAddress: 0.0.0.0:11500
nodeId: 0x7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc
publicAddress: null
sessions: 0

*  部署tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale status # 出现100.x即可
sudo tailscale down # 后续断开。
```

* 重启 yagna（关键）

```bash
yagna service stop
yagna service run &
```

* 看效果

```bash
yagna net status
```