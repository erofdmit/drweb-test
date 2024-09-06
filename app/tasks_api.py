import asyncio
from fastapi import FastAPI, APIRouter
from .task_manager import start_next_task
from .db import add_task_to_db, get_task_status
from .models import TaskStatus

router = APIRouter(
    tags=["tasks"], prefix='/tasks'
)


@router.post("/add_task/")
async def add_task():
    task_id = await add_task_to_db()
    asyncio.create_task(start_next_task())
    return {"task_id": task_id}

@router.get("/task_status/{task_id}")
async def task_status(task_id: int):
    task = await get_task_status(task_id)  
    if task:
        create_time, start_time, exec_time, status = task
        return {
            'status': status,
            'create_time': create_time,
            'start_time': start_time,
            'time_to_execute': exec_time,
        }
    else:
        return {"error": "Task not found"}


