# Basical command

主要三个命令，这三个命令其实是在执行 `package.json` 里预先定义的脚本：

```json
{
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export"
  }
}
```

我们也可以可以自定义:

```json
{
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export",
    "chromium": "pnpm add -D playwright-chromium",
    "export:pptx": "slidev export --format pptx",
  }
}
```

## `pnpm dev`

启动本地开发服务器，并在浏览器中预览幻灯片。

```bash
pnpm dev
```

默认读取项目根目录的：

```text
slides.md
```

修改 Markdown 后，浏览器会自动更新。它主要用于**编写和预览**。([Slidev][1])

也可以指定另一个入口文件：

```bash
pnpm dev talk.md
```

不过脚本参数的具体传递方式取决于脚本定义。更明确的写法是：

```bash
pnpm slidev talk.md
```

或者在 `package.json` 里增加专门的命令。

## `pnpm build`

把幻灯片构建成可部署的网站：

```bash
pnpm build
```

默认输出到：

```text
dist/
```

里面是一个静态 Web 应用，可以部署到 GitHub Pages、Netlify、Vercel 或普通 Web 服务器。

本地预览：

```bash
pnpm exec vite preview
```

## `pnpm export`

把幻灯片导出为文件：

```bash
pnpm export
```

默认导出 PDF，通常生成：

```text
slides-export.pdf
```

还可以导出其他格式：

```bash
pnpm export --format pptx
pnpm export --format png
```

注意，PPTX 中的幻灯片主要以图片形式导出，文字通常不能像普通 PowerPoint 那样直接编辑。命令行导出通常还需要安装：

```bash
pnpm add -D playwright-chromium
# pnpm remove -D playwright-chromium # remove.
```

这个下载实体不在项目内, 每一个项目内部add即可，不用担心空间问题.

谷歌等现代内核可以直接在网页转换，但是firefox的转换一般. 这里的 `--` 是把后面的参数传递给 `slidev export`。在 pnpm 中有时可以省略，但写上更清楚.
