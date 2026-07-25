根据官方文档，在Ubuntu上安装Docker的标准步骤如下：

## 1. 卸载旧版本（如有必要）
```bash
sudo apt-get remove -y docker docker-engine docker.io containerd runc
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -rf /etc/docker
```

## 2. 安装必要的依赖包(mint)
```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 6. 验证Docker安装
```bash
sudo docker --version
sudo docker run hello-world
```

## 7. 配置非sudo运行（可选但推荐）
```bash
sudo usermod -aG docker $USER
```
然后重新登录或重启系统，这样就不需要每次使用sudo来运行Docker命令。

完成这些步骤后，您的Ubuntu系统就成功安装了Docker，可以正常运行Golem Provider所需的容器环境。建议安装完成后重启系统以确保所有配置生效。

