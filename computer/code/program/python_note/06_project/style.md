# 代码风格

以 `qmeas.random` 重构为范例，总结偏好的项目组织风格。适用于科学计算类 Python 项目（思路借鉴 Julia）。

## 核心原则

1. **单一职责分层**：一个文件（module）只管一层，按“职责/流程”切，而非按类切。
2. **类型附近放它的工厂和方法**：数据类型旁边就配它的构造工厂和相关操作。
3. **贫血数据类**：存数据的类只放字段，不放逻辑；逻辑放到别的层。
4. **不为组合爆炸写类**：正交的维度拆成可插拔的函数，用注册表组合，别每种组合写一个类。

**技巧：以 run_pipline(主要工作流，当然不一定只有一个文件) 为核心，构造所需要的class, 选择分支应该在class内部**

## 分层示例

```
meas_config.py    只放数据（纯 dataclass，无逻辑、无 IO）
params_setting.py 只生成参数
meas_runner.py    只执行
meas_pipeline.py  只串流程 + 存结果（全是函数，无 class）
```

不是每层都以某个 class 为核心：偏计算/流程的层可以干脆没有 class，全用函数。

## 常用模式

### 数据用 dataclass

```python
@dataclass(frozen=True)   # 不可变配置用 frozen
class SettingRun:
    setting_num: int
    shot_num: int
```

替代裸 `tuple`，字段有名字、有类型。

### 正交维度拆成函数 + 注册表

两个独立维度不要相乘展开成 N 个类。各自写小函数，用 dict 注册：

```python
GROUP_BUILDERS = {"independence": _independent_groups, "pair": _paired_groups}
ANGLE_SAMPLERS = {"haar": _sample_haar, "pauli": _sample_pauli, ...}
```

新增一种只加一行注册，不碰其它维度。

### 工厂函数集中字符串/类型判断

选择逻辑只出现在工厂里，调用方拿到对象后无分支使用：

```python
def create_parameter_generator(meas_mode, ensemble, *, seed=None):
    group_builder = GROUP_BUILDERS[meas_mode]     # 字符串 -> 函数
    angle_sampler = ANGLE_SAMPLERS[ensemble]
    return ParameterGenerator(group_builder, angle_sampler, np.random.default_rng(seed))

def create_runner(options):
    return {AerOptions: AerRunner, QuarkOptions: QuarkRunner}[type(options)](options)
```

对应 Julia 的多重分派；Python 无多重分派，用 `{类型: 类}` 查表模拟。

### 统一接口用 Protocol

结构化类型：只要“长得对”就算符合，不需显式继承。

```python
class MeasurementRunner(Protocol):
    async def run(self, ...) -> RunResult: ...
```

为接口整齐，各实现即使用不到某参数也保留（如 `AerRunner.run` 的 `name`），换取调用方无 `isinstance` 分支。

### 组装 vs 执行分离

- 工厂函数：**组装**，决定“用哪种策略”，只跑一次。
- 实例方法：**执行**，用选好的策略算出结果，可反复调用，内部无 `if mode == ...`。

### 签名习惯

- 可选/次要参数用 `*` 设为 keyword-only：`def f(a, b, *, seed=None)`。
- 私有函数前缀 `_`；模块 `__init__.py` 用 `__all__` 显式导出公共 API。

## 命名与导入

- 显式导入具体名字，避免无意义别名（用 `from qmeas.random import RandomMeasConfig`，不要 `import ... as src`）。
-, 选择分支应该在class内部 布局用 src-layout：`src/包名/子包/`。

