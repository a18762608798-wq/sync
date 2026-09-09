# 05 排查：当前到底在用哪套 Node

> 解决大量“明明装了为什么找不到”问题的一组命令。

## 诊断五条

```bash
command -v node
command -v npm
node -v
npm -v
npm prefix -g
```

用 nvm 且正常时类似：

```text
/home/user/.nvm/versions/node/v24.20.0/bin/node
/home/user/.nvm/versions/node/v24.20.0/bin/npm
```

`npm prefix -g` 应为 `/home/user/.nvm/versions/node/v24.20.0`。

## `command -v` 与 `type -a`

- `command -v <cmd>`：回答“shell 实际会执行哪个程序”，排查价值高于 `<cmd> --version`。

  ```bash
  command -v node
  command -v npm
  command -v pi
  ```

- `type -a <cmd>`：怀疑有多个版本时，列出 PATH 中所有候选。

  ```bash
  type -a node
  type -a npm
  ```

## 工具坏了的排查顺序

```bash
node -v
command -v node

npm -v
command -v npm

npm prefix -g
npm ls -g --depth=0

command -v <坏掉的CLI>
```
