# Build on github

## bases

需要在github上构建disk/, 和本地没有关系.

### Create a git warehouse

注意ignore相关文件，参考 [.gitignore](../.gitignore)

### Create github reps dir

Ref to [deploy.yml](/.github/workflows/deploy.yml)

### Action

Push 之后找到改仓库, Action 中即可。

### 限制

一个仓库只能放映一个 `\dist` 目录，所以如果想在一个仓库放多个需要看提高篇.

## enhance

只用修改yml命令既可.

Ref to [deploy.yml](/.github/workflows/deploy.yml)
