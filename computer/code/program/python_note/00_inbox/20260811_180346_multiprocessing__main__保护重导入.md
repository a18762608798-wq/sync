# multiprocessing 的 __main__ 保护：forkserver/spawn 会重导入主脚本

**日期**: 2026-08-11 18:03
**分类**: 编程/Python
**标签**: #Python #multiprocessing #Pool #__main__ #forkserver #spawn

## 背景

用 `multiprocessing.Pool` 并行优化时，测试脚本在模块顶层直接调用 `optimize_pipeline()`，运行时崩溃，报 `ConnectionResetError` 和 "An attempt has been made to start a new process before the current process has finished its bootstrapping phase"。

## 内容

### 现象

测试脚本顶层直接执行任务：

```python
from optimize_pipeline import optimize_pipeline

print(optimize_pipeline(end))   # ← 模块顶层调用
```

运行报错：`RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase`，随后 `ConnectionResetError: [Errno 104] Connection reset by peer`。

### 原因

Python 3.14 默认启动方式已变为 **forkserver**（spawn 系）。这种模式下，子进程不是从父进程内存直接 fork，而是**重新导入主脚本**（通过 `runpy.run_path` 以 `__mp_main__` 名义）。

于是子进程导入 `test_optimize_pipeline.py` 时，顶层那句 `print(optimize_pipeline(end))` 又被执行 → 再次创建 `Pool` → 再次启动子进程 → **递归创建进程**，最终资源耗尽、连接被重置崩溃。

> 旧版 Linux 默认是 `fork`（子进程继承父进程内存、不重新导入主脚本），所以不易触发；Python 3.14 切到 forkserver 后，顶层调用这种写法就暴露了。

### 修复：__main__ 保护

```python
from optimize_pipeline import optimize_pipeline


if __name__ == "__main__":
    end = [0.5, 0.5]
    print(optimize_pipeline(end))
```

- 子进程导入主脚本时，`__name__` 是 `"__mp_main__"`（不是 `"__main__"`），不会执行保护块内代码
- 只注册函数定义供子进程调用，避免递归创建进程

### 经验

凡是用 `Pool` / `Process` / `spawn` 的程序，**入口代码必须放进 `if __name__ == "__main__":`**。这是 Python 官方文档 "Safe importing of main module" 明确要求的惯例，尤其在 Python 3.14 默认 forkserver 下是硬性要求。

## 要点

- forkserver/spawn 子进程会**重新导入主脚本**，顶层可执行代码会被再跑一遍
- 递归创建进程 → `ConnectionResetError`，报错信息含 "bootstrapping phase"
- 修复：入口调用包进 `if __name__ == "__main__":`
- Linux 上 Python 3.14 默认已从 fork 改为 forkserver，更易触发此坑
