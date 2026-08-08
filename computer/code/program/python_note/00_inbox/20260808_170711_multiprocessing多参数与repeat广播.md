# multiprocessing pool.imap 多参数传递 与 itertools.repeat

**日期**: 2026-08-08 17:07
**分类**: 编程/Python
**标签**: #multiprocessing #pool #imap #starmap #itertools

## 背景

用 `Pool.imap` 并行扫描参数，`_run_one` 有多个输入参数，且其中一个参数对每个 worker 相同。

## 内容

### pool.imap 只接受单参数

`pool.imap(func, iterable)` 的每个元素会被**当作单个位置参数**传给 `func`。传多个输入有几种写法：

**方案1：函数接收元组**
```python
def _run_one(args):
    s, chip = args
    ...
pool.imap(_run_one, zip(slist, chip_list))
```

**方案2：包一层解包（推荐，保持原函数签名）**
```python
def _run_one(s, chip): ...
def _wrapper(args):
    return _run_one(*args)
pool.imap(_wrapper, zip(slist, chip_list))
```

**方案3：`starmap`（自动解包，但不惰性）**
```python
pool.starmap(_run_one, zip(slist, chip_list))  # 自动展开成 _run_one(s, chip)
```
`starmap` 一次性返回，配 `tqdm` 不如 `imap` 方便（`imap` 惰性、可配进度条）。

### 广播常量：itertools.repeat

当某个参数对所有 worker 相同（如共享的 `optimizer_options` dict）：
```python
pool.imap(_wrapper, zip(slist, chip_list, x0_maps, itertools.repeat(optimizer_options)))
```
- `itertools.repeat(x)` 生成无限重复 `x` 的迭代器，`zip` 在最短列表处截断，所以无限也无妨。
- 比 `[x]*len` 更省内存（惰性、不复制对象）。
- 与 `_run_one(s, chip, x0, optimizer_options)` 四参对齐。

## 要点

- `imap` 单参数、`starmap` 自动解包但不惰性。
- 多参数 + 惰性 + 进度条 → `imap` + `_wrapper(*args)` + `zip`。
- 共享常量参数用 `itertools.repeat` 广播。
- 注意参数个数：`zip` 提供的元素数必须与目标函数参数个数一致。
