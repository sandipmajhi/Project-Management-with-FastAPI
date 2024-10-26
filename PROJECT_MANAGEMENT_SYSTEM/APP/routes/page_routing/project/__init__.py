from .project_router import project as project_route
from fastapi import APIRouter

project = APIRouter()

project.include_router(project_route)
