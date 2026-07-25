import asyncio
from typing import AsyncIterable
from yapapi import Golem, Task, WorkContext
from yapapi.payload import vm
from datetime import timedelta
import shlex
import os


async def worker(context: WorkContext, tasks: AsyncIterable[Task]):
    async for task in tasks:
        script = context.new_script()
        safe_input = shlex.quote(str(task.data))
        
        fut = script.run(
            "/bin/sh",
            "-c",
            f"python /app/worker.py {safe_input}"
        )
        
        yield script
        
        try:
            result = await fut
            stdout = result.stdout
            
            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors="ignore")
            
            stdout = (stdout or "").strip()
            
            if stdout:
                task.accept_result(stdout)
            else:
                task.reject_result(message="Empty output")
        except Exception as e:
            task.reject_result(message=f"Execution failed: {str(e)}")

# ... 其他保持不变 ...

async def main():
    package = await vm.repo(
        image_hash="8010a5114f1652849c974bef171ef4aaad281092c0f89eaf46e8ef77",  # 重新上传后替换这里
    )

    async with Golem(
        budget=1.0,  # N 大时任务稍长，预算稍提高点（实际花不了多少）
        subnet_tag="public",
        payment_driver="erc20",
        payment_network="polygon",
    ) as golem:
        # 改大 N 测试 NumPy 性能（100万~1000万点都很合适）
        tasks = [
            Task(data = str(100000 * (i + 1))) for i in range(1, 6)
        ]
        kwargs = {
            "payload": package,
            "max_workers": 10,
            "timeout": timedelta(minutes=15),  # 稍延长点
        }
        
        async for completed in golem.execute_tasks(worker, tasks, **kwargs):
            print(f"✅ Task completed: {completed.result}")

# ... 其余不变 ...

if __name__ == "__main__":
    asyncio.run(main())