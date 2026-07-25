浏览器钱包metamask 可用
地址: 0x7AdC8E8D911bdC47F90cA7e2Ad3209a9d1DE83dc
私钥：33af91ed59b0f66ff449711d38165d88434c61f18161931fc93565d8bf172e01
助记词：purpose swallow pitch dirt kind comfort cake annual dwarf year boss gap

打洞能力受限检测，null就不太行。：yagna net status

---
golem钱包地址收钱，但是还有yagna地址是付钱的

yagna id list 可以显示yagna有哪些地址

如果没有，先导入私钥：

yagna id create --from-keystore ./key.json
> Imported identity: 0x7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc

至于如何制作.json

```bash
# 安装 geth（Ubuntu）

# 2) 安装常规 geth（非 snap；Ubuntu 可用官方仓库或 PPA）
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install -y geth

cd

# 写入你的私钥（不要带 0x，且不要换行/空格）
echo -n "33af91ed59b0f66ff449711d38165d88434c61f18161931fc93565d8bf172e01" > raw.key
chmod +x raw.key

# 生成 keystore（会让你设置一个密码；这就是 keystore 的加密口令）
geth account import --datadir ~/.keystore ~/raw.key


# 找到刚才生成的 keystore 文件名（把 <UTC-file> 换成实际文件名）
ls ~/.keystore

# 导入（会要求输入你在 geth 导入时设置的那个口令）
yagna service run
yagna id create --from-keystore /home/mintusr/.keystore/keystore/UTC--2026-03-17T07-20-47.254235701Z--7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc

```

加密的密钥不要动，系统会调用。

设置

```bash
yagna service run

# 新开终端
yagna id update --set-default 0x7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc
yagna id show

# 重启
# ctrc + c杀死
yagna service run
# 再开解锁账户
yagna id unlock
# 账号初始化
yagna payment init --sender --account 0x7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc --driver erc20
# 验证
yagna payment status
# 去旧钱包，需要一段时间dekete in
yagna id drop 0xa4a9b742deab82d01f7f15a727bd39c0839f9eea 
```


更换到主网

```
# 设这把地址为 Polygon 主网的出款账户（sender）[注意如果在此过程创造了key需要解散]
yagna payment init --sender \
  --account 0x7adc8e8d911bdc47f90ca7e2ad3209a9d1de83dc \
  --driver erc20 \
  --network polygon

# 验证现在看的是 Polygon 主网
yagna payment status --driver erc20 --network polygon # 默认显示测试网不加参数
```

yagna payment status


刚需docker

参考docker安装

