from fastapi import APIRouter
from .user_login import user as user_login_router

user_page_router = APIRouter()

user_page_router.include_router(user_login_router)


