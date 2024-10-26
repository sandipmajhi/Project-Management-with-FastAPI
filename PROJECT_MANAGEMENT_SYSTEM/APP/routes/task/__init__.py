from .create_task import router as create_task_router
from .task_level_b import router as task_levelb
from .task_level_c import router as task_levelc
from .task_level_d import router as task_leveld
from .create_sub_task import router as create_sub_task_router
from .create_sub_task_d import router as create_sub_task_d_router
from .task_by_admin import router as task_by_admin_router
from .add_comment import router as edit_task_router
from fastapi import APIRouter

task_router = APIRouter()

task_router.include_router(create_task_router)
task_router.include_router(task_levelb)
task_router.include_router(task_levelc)
task_router.include_router(task_leveld)
task_router.include_router(create_sub_task_router)
task_router.include_router(create_sub_task_d_router)
task_router.include_router(task_by_admin_router)
task_router.include_router(edit_task_router)