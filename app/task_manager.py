import asyncio
import random
import time
from datetime import datetime
from app.db import get_active_task_count, update_task_status, get_next_task_in_queue

async def execute_task(task_id: int):
    """Функция, имитирующая выполнение задачи."""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update_task_status(task_id, 'Run', start_time=start_time)

    exec_time = random.randint(0, 10)
    await asyncio.sleep(exec_time) 
    await update_task_status(task_id, 'Completed', exec_time=exec_time)
    await start_next_task()

async def start_next_task():
    """Функция запуска следующей задачи, если есть свободное место."""
    active_task_count = await get_active_task_count()
    if active_task_count < 2:
        next_task = await get_next_task_in_queue()
        if next_task:
            task_id = next_task[0]
            asyncio.create_task(execute_task(task_id)) 