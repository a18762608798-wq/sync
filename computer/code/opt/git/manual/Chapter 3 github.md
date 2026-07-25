# Chapter 3 github

## 3.1 ssh

### new ssh

```bash
ls -al ~/.ssh # 查看是否已有密钥
ssh-keygen -t ed25519 -C "a18762608798@gmail.com" # 创造

# 添加 SSH Key 至 ssh-agent
eval "$(ssh-agent -s)" # 启动服务
ssh-add ~/.ssh/id_ed25519 # 添加私钥
xclip -sel clip < ~/.ssh/id_ed25519.pub # copy pulic key, 此次为ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN/SXpNe8cbwJFdZjnzMC4zGHsKofXCe76cq0E/Glaeo a18762608798@gmail.com
```

**然后在github官网粘贴剪贴板ssh public key, 运行：**

```bash
ssh -T git@github.com
```

### old ssh

```bash
# power
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
# add 
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
# 新机子可能还是要添加ssh到github
# 复制公钥：
cat ~/.ssh/id_ed25519.pub
# 打开 GitHub → Settings → SSH and GPG keys → New SSH key，粘贴保存。
# test
ssh -T git@github.com
```

## 3.2 push

在github创建新项目，复制其中的 SSH 地址。

> 切勿勾选 "Add a README file"。
> 切勿勾选 "Add .gitignore"。
> 切勿勾选 "Choose a license"。

```bash
git remote add origin <repository-url> # Case: git@github.com:a18762608798-wq/MOT.git, 不用<>; git init firstly.
# git@github.com:a18762608798-wq/julia_note.git
# 将当前分支重命名为 main，
git branch -M main

# 暂存所有文件(mast add at first time)
# git add .
# 提交更改
# git commit -m "Initial commit"

# 推送到云
git push -u origin main
```
