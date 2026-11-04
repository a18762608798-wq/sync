# exfat 挂载

我们更推荐共享数据通过这种形式挂载，但是最好加开机自动挂载：

```bash
# check the name
lsblk -f
```

```bash
# create fixed dir
sudo mkdir -p /mnt/hdd
sudo mkdir -p /mnt/snapshot
```

```bash
sudo nvim /etc/fstab
```

Write in

```text
UUID=7A5E-552C /mnt/hdd exfat defaults,uid=1000,gid=1000,umask=022,nofail 0 0 #exfat
UUID=85c2af98-a252-46e5-a4b3-0c314cd1385d /mnt/snapshot ext4 defaults,nofail 0 2 #ext4
```

然后重启你就只能在/mnt找到这两个挂载了。
