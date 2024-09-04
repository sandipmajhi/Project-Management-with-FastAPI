from fastapi import FastAPI
from routes.superuser import superuser
from routes.Employee import router
from routes.user import user

from routes.project import project_router

from routes.task import task_router

app = FastAPI()


app.include_router(superuser)
app.include_router(router)
app.include_router(user)
app.include_router(project_router)
app.include_router(task_router)

