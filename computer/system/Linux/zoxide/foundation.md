有，zoxide 的基础用法其实不多，核心就是把 `cd` 变聪明。

先假设你已经启用了它。

# 最常用的几个命令

## 1. `z <关键词>`

这是最核心的用法。

```bash
z proj
```

它会根据你的访问历史，跳到最匹配、最常去的目录。

比如你平时去过：                                                                                                        

```text
~/projects
~/work/project-a
~/Downloads/project-files
```

那你输入：

```bash
z proj
```

zoxide 会按“匹配度 + 访问频率”选一个最可能的目录跳过去。

---

## 2. `zi`

交互式选择，通常会配合 `fzf`。

```
sudo apt install fzf
```

```bash
zi
```

会弹出一个可选列表，你可以模糊搜索后再选目录。

这个很好用，尤其当你记不清关键词的时候。

---

## 3. `z foo bar`

可以多个关键词一起匹配：

```bash
z work api
```

它会找同时最符合 `work` 和 `api` 的目录。

这比只写一个词更准。

---

## 4. `z /完整/路径/的一部分`

也可以按路径片段跳：

```bash
z src/backend
```

只要你以前去过相关目录，它就会匹配。

---

# 和 `cd` 的关系

## 5. 普通 `cd` 仍然能用

zoxide 不是替代 `cd`，而是增强它。

```bash
cd ~/tmp
```

照常可用。

而且你每次 `cd` 到一个目录，zoxide 都会学习这个记录，之后你就可以直接：

```bash
z tmp
```

---

# 常见辅助命令

## 6. `zoxide query`

查某个关键词会匹配到哪个目录：

```bash
zoxide query proj
```

它不会跳转，只会打印结果。

适合测试匹配结果。

---

## 7. `zoxide query -l`

列出匹配结果：

```bash
zoxide query -l proj
```

会显示多个候选目录。

```bash
zoxide query -l # 所有列表
```
---

## 8. `zoxide add`

手动把目录加入数据库：

```bash
zoxide add ~/some/path
```

通常不太需要，因为平时 `cd` 就会自动记录。

---

## 9. `zoxide remove`

移除某个目录记录：

```bash
zoxide remove ~/old/project
```

---

# 很实用的使用习惯

## 场景 1：经常在几个项目之间切

以前：

```bash
cd ~/work/company/backend-service
cd ~/work/company/frontend-app
```

有了 zoxide：

```bash
z backend
z frontend
```

---

## 场景 2：目录很深

比如：

```text
~/Documents/notes/math/linear-algebra
```

以后可以直接：

```bash
z linear
```

---

## 场景 3：不知道准确路径，但记得关键词

```bash
z notes math
```

比手打完整路径快很多。

---

# 一个容易误解的点

zoxide 不是“全盘搜索你的文件系统”。

它只会在**你去过的目录记录里匹配**。

所以第一次去某目录还得：

```bash
cd ~/new/path
```

之后它学会了，你才能：

```bash
z new
```

---

# 你现在最该记住的最小集合

先会这 4 个就够了：

```bash
z keyword
z keyword1 keyword2
zi
zoxide query keyword
```

---

# 一个简单例子

假设你平时去过：

* `~/projects/blog`
* `~/projects/api-server`
* `~/notes/math`

那你以后可以这样：

```bash
z blog
z api
z notes math
zi
```

---

# 一句话总结

zoxide 的基础用法本质上就一句：

> **先正常 `cd`，让它记住；以后用 `z 关键词` 快速跳过去。**

如果你要，我可以接着给你一份“zoxide 从入门到顺手”的高频场景速查表。
