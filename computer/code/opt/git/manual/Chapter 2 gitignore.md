# 2 Chapter 2 gitignore

## 2.1 create .gitignore file

```bash
nvim .gitignore
```

## 2.2 the format of file

### ignore certain file

```text
config.json
.env
.DS_Store
```

### ignore certain folder in any directory

```text
node_modules/
dist/
build/
```

### ignore certain kind of files

```text
*.log
*.tmp
*.class
*. # however we do not recommend ignore all . files.
```

### ignore the folder or files in root directory

```text
/config.json
/dist/
```

### ignore the files in certain folders

```text
logs/*
!logs/.gitkeep # reverse exclusion
```

## 2.3 push

```python
# 4. 提交 .gitignore
git add .gitignore
git commit -m "添加 gitignore 配置"
```

## 2.4 test

```bash
# 检查哪些文件会被忽略
git check-ignore -v *

# 检查特定文件是否被忽略, if the files have been tracked, the result is null.
git check-ignore -v .obsidian/app.json

# 查看实际生效的忽略规则
git status --ignored

# clean the file in history
git rm --cached path/to/file
```
