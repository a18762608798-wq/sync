# swap file

本页作为 swap 笔记入口。原 Ubuntu 目录中的 [旧笔记](legacy-notes.md) 保留用于对照；两份文档的容量示例不同，操作前按本机情况选择。

## 查看 Swappiness 参数

```bash# 
free -h # search the internal memory

cat /proc/sys/vm/swappiness  # 查看

sudo nvim /etc/sysctl.conf
# 添加vm.swappiness = 90
sudo sysctl -p
```

## deployment

```bash
sudo dd if=/dev/zero of=/swapfile bs=1G count=50
sudo chmod 600 /swapfile
# 格式化交换文件
sudo mkswap /swapfile
# 启用交换文件
sudo swapon /swapfile
# 添加至系统文件
echo '/swapfile none swap defaults 0 0' | sudo tee -a /etc/fstab
```

## unload

```bash
sudo swapoff /media/hanyijie/新加卷/debian_room/swapfile
sudo nano /etc/fstab
```

在打开的文件中，找到 `home/hanyijie/swapfile none swap sw 0 0` 这一行，然后按下 `Ctrl + K` 来删除该行。接着按下 `Ctrl + X` 退出编辑器，按 `Y` 确认保存修改，最后按 `Enter` 键。

```bash
sudo rm /media/hanyijie/新加卷/debian_room/swapfile
sudo systemctl daemon-reload
```

