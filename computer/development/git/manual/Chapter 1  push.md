# Chapter 1 push

```bash
# 1. 初始化
# rm ./.git # if there has exist a storage
git init

# 2. Add to Cache area
git add . # all of the file, do not use it before bulid ignore file.
git add ./manual # add specified file
git add **/*.md # 添加当前目录及所有子目录中的 .md 文件
git add *.md # 或者只添加当前目录的 .md 文件
git add manual/*.md # 添加特定目录下的所有 .md 文件

# 从暂存区移除 .obsidian 目录（保留工作区文件, if u use .gitignore which is a important operation）
git rm -r --cached .obsidian/

# 3. 提交
git commit -m "Initial commit"
git status # 查看缓存区
git log --graph --oneline --all # 查看提交记录

# 4. 撤销
git reset --hard HEAD # 回到本次log
git reset --hard HEAD~1 # 回到上一次log
```
