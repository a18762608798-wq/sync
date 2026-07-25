from dask import delayed
import numpy as np

class Processor:
    def __init__(self, config):
        self.config = config

    def process(self, x):
        # 假设这里是计算逻辑
        return x * 2 + self.config["offset"]

# 使用时：把实例方法绑定后 delayed
p = Processor({"offset": 100})
delayed_process = delayed(p.process)

# 然后正常使用
tasks = [delayed_process(i) for i in range(100)]

# 任务分发

tasks = [delayed_process(i) for i in range(100)]
batches = np.array_split(tasks, 10)          # 得到 10 个子列表

print(batches[0])
