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
docker build -t basic-golem-worker .

# 测试镜像是否正常工作
docker run --rm basic-golem-worker
```

## 4. 转换为Golem镜像

```bash
# 安装Golem镜像构建工具
pip install gvmkit-build

# 转换并匿名上传到Golem仓库
gvmkit-build basic-golem-worker --push --nologin
```

执行后会得到一个类似这样的输出：
```
Image hash: 8010a5114f1652849c974bef171ef4aaad281092c0f89eaf46e8ef77
```

## 5. 运行

创建main.py,

**启动golemsp run, 创建app-key.**

粘贴app-key入main.py文件。

## 6. docker 管理

可以本地调试代码：docker run --rm basic-golem-worker python /app/worker.py 1000000

docker 可以删除多余镜像： 
```
docker image list
docker rmi golem-qiskit-worker:latest          # 用 tag 删除
```