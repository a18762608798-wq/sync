import asyncio
import pandas as pd
from typing import AsyncIterable
from yapapi import Golem, Task, WorkContext
from yapapi.payload import vm
from yapapi import events  # 新增导入
from datetime import timedelta
import json
import shlex
import os

def append_with_pandas(filename, data):
    df = pd.DataFrame(data)
    file_exists = os.path.isfile(filename)
    
    df.to_csv(
        filename,
        mode='a',           # 追加模式 [[2]]
        index=False,
        header=not file_exists,  # 仅首次写入表头 [[28]]
        encoding='utf-8-sig'     # 支持中文且Excel可正常打开
    )

# 新增：事件处理器
active_providers = set()
def event_consumer(event):
    # AgreementEvent及其子类（包括AgreementCreated/WorkerFinished）都有provider_id属性
    if isinstance(event, events.AgreementCreated):
        active_providers.add(event.provider_id)  # ✅ 正确：直接使用event.provider_id
        print(f"[Worker Monitor] 已连接Provider: {event.provider_id} | 当前总数: {len(active_providers)}")
    elif isinstance(event, events.WorkerFinished):
        if event.provider_id in active_providers:
            active_providers.remove(event.provider_id)
            print(f"[Worker Monitor] Provider断开: {event.provider_id} | 剩余总数: {len(active_providers)}")

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


async def main():
    package = await vm.repo(
        image_hash="1f0ac0d39d98e7333f4a7c1ec443f3e844f676a7386ccf189a800810",  
    )

    async with Golem(
        budget=0.0001 ,  
        subnet_tag="public",
        payment_driver="erc20",
        payment_network="polygon",
        event_consumer=event_consumer,  # 注入事件监听器
    ) as golem:
        tasks = [
            Task(data = str((i))) for i in range(29, 30)
        ]
        kwargs = {
            "payload": package,
            "max_workers": 1,
            "timeout": timedelta(minutes=1000),  # set longer if single task more than 5 min.
        }

        # save
        max_cut_cost_list = []
        qaoa_layer_list = []
        out_put_csv = 'max_cut_info.csv'
        async for completed in golem.execute_tasks(worker, tasks, **kwargs):
            result_dict = json.loads(completed.result)
            max_cut_cost_list.append(result_dict["max_cut_cost"])
            qaoa_layer_list.append(result_dict["qaoa_layer"])
            print(f"✅ Task completed: {completed.result}")
        data = {"qaoa_layer": qaoa_layer_list, "max_cut_cost": max_cut_cost_list}
        if os.path.exists(out_put_csv):
            os.remove(out_put_csv)
        append_with_pandas(out_put_csv, data)
        
if __name__ == "__main__":
    asyncio.run(main())