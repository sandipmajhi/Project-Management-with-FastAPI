from fastapi import APIRouter
from .create_project import router as create_project_router
from .assign_project_to_empa import router as assign_project_to_empa_router
from .view_project_list import router as view_project_router
from .assigned_project_list import router as assigned_project_list_router


# Create a single APIRouter instance
project_router = APIRouter()

# Include individual routers
project_router.include_router(create_project_router)
project_router.include_router(assign_project_to_empa_router)
project_router.include_router(view_project_router)
project_router.include_router(assigned_project_list_router)