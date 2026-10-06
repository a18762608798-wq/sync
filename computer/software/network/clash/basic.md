# basic

## cofig

临时设置本机代理地址 `127.0.0.1:端口`

Clash Party 当前默认端口是(见内核设置, 在设置之外)：

* 混合端口：7890，同时接受 HTTP 和 SOCKS5
* SOCKS 端口：7891
* HTTP 端口：7892

最省事的是使用混合端口 7890：

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"

export HTTP_PROXY="$http_proxy"
export HTTPS_PROXY="$https_proxy"

export all_proxy="socks5h://127.0.0.1:7891"
export ALL_PROXY="$all_proxy"

export no_proxy="localhost,127.0.0.1,::1"
export NO_PROXY="$no_proxy"
```

其中 socks5h 表示域名也交给代理端解析，通常比 socks5 更适合代理访问。

## 测试

```bash
curl -I https://www.google.com
```

## 关闭临时代理

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
unset all_proxy ALL_PROXY no_proxy NO_PROXY
