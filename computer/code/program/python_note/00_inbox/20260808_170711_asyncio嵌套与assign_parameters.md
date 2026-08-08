# asyncio.run 不能嵌套 + qiskit assign_parameters 返回新电路

**日期**: 2026-08-08 17:07
**分类**: 编程/Python
**标签**: #asyncio #qiskit #调试 #异步

## 背景

提交量子任务链路上出现两个易踩的坑：`async` 函数里嵌套 `asyncio.run` 报错，以及 qiskit `assign_parameters` 不就地修改电路。

## 内容

### asyncio.run 不能在 running loop 中调用

```python
async def submit_ops_task(...):
    ...
    count = asyncio.run(submit_quark_task(...))   # 错误!
```
报错：
```
RuntimeError: asyncio.run() cannot be called from a running event loop
```
原因：`asyncio.run` 会创建一个新的事件循环，但 `submit_ops_task` 本身是 `async`，调用它时已经有一个 loop 在运行，无法再嵌套建 loop。

**修复**：在 `async` 函数里用 `await` 而非 `asyncio.run`：
```python
count = await submit_quark_task(...)
```
同时注意：`async` 函数必须被 await/`asyncio.run` 驱动，否则只是 "coroutine never awaited" 警告，什么都不执行。

### qiskit assign_parameters 返回新电路

```python
group_qc = qc.copy()
group_qc.assign_parameters(group_bind)   # 返回值被丢弃!
```
`qc.assign_parameters()` 默认**返回新电路、不就地修改**，丢弃返回值则电路仍含未绑定参数，导出 QASM 时报：
```
QASM2ExportError: Cannot represent circuits with unbound parameters
```
**修复**：捕获返回值：
```python
group_qc = group_qc.assign_parameters(group_bind)
```

## 要点

- `async` 函数内部调其他协程用 `await`，不要 `asyncio.run`。
- 不给 `async` 函数外层套 `asyncio.run` 时会 "coroutine never awaited"。
- qiskit 多数不可变 API（如 `assign_parameters`）返回新对象，必须接收返回值。
