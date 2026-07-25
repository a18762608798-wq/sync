以下是为Golem创建包含Qiskit库的Python镜像的完整步骤示例：

## 1. 创建项目目录结构

```
basic-golem-project/
├── Dockerfile
├── worker.py
└── requirements.txt
```

## 2. 创建具体的文件内容
参考文件。

## 3. 构建Docker镜像

在项目目录中执行以下命令：

```bash
# 构建Docker镜像(需要tun)
docker build -t qiskit-golem-worker .

# 测试镜像是否正常工作
docker run --rm qiskit-golem-worker python /app/worker.py 1
```

## 4. 转换为Golem镜像

```bash
# 安装Golem镜像构建工具
pip install gvmkit-build

# 转换并匿名上传到Golem仓库
gvmkit-build qiskit-golem-worker --push --nologin

for i in {1..100}; do gvmkit-build qiskit-golem-worker --push --nologin && break || { echo "失败，重试 $i"; sleep 1; }; done # 网络不好时候用。
```

执行后会得到一个类似这样的输出：
```
Image hash: 1f0ac0d39d98e7333f4a7c1ec443f3e844f676a7386ccf189a800810
```

## 5. 运行

创建main.py,

**启动golemsp run, 创建app-key.**
docker run --rm qiskit-golem-worker
粘贴app-key入main.py文件。

> 和连接的vpn关系很大，注意连接有效vpn

## 6. docker 管理

可以本地调试代码：docker run --rm qiskit-golem-worker python /app/worker.py 1

docker 可以删除多余镜像： 
```
docker image list
docker rmi golem-qiskit-worker:latest          # 用 tag 删除
```