# Idea

```text
Zotero = 文献资料层
Neovim = 思考与写作层
```

Zotero 主要负责：

* 保存和管理 PDF；
* 保存作者、标题、期刊、DOI 等书目信息；
* 阅读 PDF、划线和添加贴近原文的批注；
* 记录批注对应的页码和原文位置；
* 为 Zotcite 提供 citation key、摘要、附件和批注；
* 统一生成参考文献数据。

Neovim 主要负责：

* 写文献总结；
* 整理自己的理解；
* 跨文献比较；
* 建立 Markdown 链接；
* 写论文、报告或知识笔记；
* 使用 `@citation-key` 连接回 Zotero。

所以 Zotero 不只是 PDF 阅读器，它更像是：

> **PDF 阅读器＋文献数据库＋可靠的原文定位系统。**

而 Neovim 是你真正进行知识加工的地方。

一个典型流程就是：

```text
Zotero 收集论文
→ 阅读并高亮
→ Zotcite 将选中的批注导入 Neovim
→ 在 Markdown 中写自己的总结和观点
→ 需要核对时从 citation key 跳回 PDF
```

最关键的分界是：

* **原文说了什么**：留在 Zotero，高亮并保留页码。
* **你如何理解它**：写在 Neovim。
* **你在哪里使用它**：通过 `@citation-key` 引用。
