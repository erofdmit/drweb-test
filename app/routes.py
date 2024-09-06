from fastapi import APIRouter
from . import tasks_api

router = APIRouter()
router.include_router(tasks_api.router)
