如果机械盘是windows格式而不是ext4, 会出现挂载问题，这很头疼。  

---

## 🧩 一、情况总结

你的机械硬盘情况如下：

| 项目 | 内容 |
|------|------|
| 磁盘设备 | `/dev/sda` |
| 分区格式 | GPT |
| 分区1 | `/dev/sda1` – Microsoft 保留（系统辅助分区，没数据） |
| 分区2 | `/dev/sda2` – Microsoft 基本数据（**主分区、NTFS 格式**） |
| 容量 | 465.6 GB |
| 错误提示 | 无法挂载 / bad superblock / wrong fs type |

🔍 结论：  
`/dev/sda2` 是 **NTFS（Windows）格式分区**，  
Ubuntu 报错是因为：
- 文件系统损坏（superblock 异常），或者  
- Ubuntu 没装 `ntfs-3g` 驱动。

---

## 🧰 二、最安全修复步骤

### ✅ 1️⃣ 安装 NTFS 驱动

在终端执行：

```bash
sudo apt update
sudo apt install ntfs-3g -y
```

> 这个包是 Ubuntu 访问和修复 NTFS 分区的核心工具。

---

### ✅ 2️⃣ 修复 NTFS 文件系统

然后执行修复命令：

```bash
sudo ntfsfix /dev/sda2
```

你会看到类似输出：

```
Mounting volume... FAILED
Attempting to correct errors... OK
Processing of $MFT and $MFTMirr completed successfully...
NTFS volume version 3.1
NTFS partition /dev/sda2 fixed successfully.
```

这表示修复成功。

---

### ✅ 3️⃣ 手动挂载验证

```bash
sudo mkdir -p /media/ubuntu-usr/hdd
sudo mount /dev/sda2 /media/ubuntu-usr/hdd
```

如果没有报错，执行：

```bash
ls /media/ubuntu-usr/hdd
```

✅ 能看到文件，就说明硬盘修好了。

---

### ⚠️ 如果 `ntfsfix` 报错依然无法修复

有两种情况：

1. **轻度损坏（不影响读）**  
   可以先用 `sudo mount -t ntfs-3g /dev/sda2 /media/ubuntu-usr/hdd` 强制挂载；
2. **严重损坏**  
   就只能在 Windows 上运行 “chkdsk /f” 修复：
   - 插回 Windows；
   - 打开管理员命令提示符；
   - 输入：
     ```cmd
     chkdsk D: /f
     ```
     （假设该盘在 Windows 下是 D 盘）

`chkdsk` 是唯一能修复部分 NTFS 元数据错误的工具。

---

## 💡 三、几点说明

- 报错中的 “bad superblock” 对 NTFS 来说指的是 **MFT 元数据出错**；
- Ubuntu 无法自动修复这种问题，需要 `ntfsfix` 或 Windows 自带的 `chkdsk`；
- 不要随意格式化，否则数据彻底没了；
- 如果硬盘平时插在 Windows 上、Ubuntu 访问，只要修复一次就可以正常双系统使用。

---

## ✅ 总结指令清单（可直接复制执行）

```bash
sudo apt update
sudo apt install ntfs-3g -y
sudo ntfsfix /dev/sda2
sudo mkdir -p /media/ubuntu-usr/hdd
sudo mount /dev/sda2 /media/ubuntu-usr/hdd
ls /media/ubuntu-usr/hdd
```

执行完这几行后，**如果能看到文件列表**，就完全修好了 🎉。

---

你执行完 `sudo ntfsfix /dev/sda2` 之后，把输出贴给我看一下，  
我能确认它到底修好了还是还需进一步操作。


## 补充，开机自动挂载

```bash
注意查看UUID
sudo blkid /dev/sda1
sudo nano /etc/fstab
```

添加 "UUID=AE7CD9937CD95725 /media/mintusr/hdd ntfs-3g  defaults,windows_names,uid=1000,gid=1000,umask=022  0  0"

