# Get_start

## reps

### global

>nvm（Node Version Manager）管理 Node.js 版本。Node.js 是 JavaScript 运行时。npm（Node Package Manager）随 Node.js 一起发布，是 Node.js 的包管理器。

- **nvm** → **pyenv** / **conda**：管理 Python 版本
- **Node.js** → **Python**：运行时解释器
- **npm** → **pip**：包管理器
- **npx** → **pipx run**：临时下载包并运行，用完删除
- **pnpm** → **uv** / **poetry**：替代 npm/pip 的高效包管理器，特点是磁盘效率高、安装快、严格的依赖隔离。

```bash
# nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh | bash
source ~/.bashrc
command -v nvm
nvm --version
# npm, node
# `nvm install --lts` 这一步会下载并安装 **Node.js**，而 npm 随 Node.js 捆绑发布，所以 **npm 也一并装好了**。
nvm install --lts
nvm alias default 'lts/*' # 将 nvm 的默认 Node.js 版本设置为最新的 LTS（长期支持）版本
node --version
npm --version
# pnpm
npm install -g pnpm # Node.js 22 及以上：安装当前最新 pnpm
```
