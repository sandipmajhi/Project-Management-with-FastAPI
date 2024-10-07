#  =================================Created by Sandip 27-09-2024======================================
#          ======================================  ======================================
from fastapi import FastAPI
from routes.superuser import superuser
from routes.Employee import router
from routes.user import user

from routes.project import project_router

from routes.task import task_router
from routes.page_routing.project import project
from routes.page_routing.user import user_page_router
from starlette.middleware.sessions import SessionMiddleware

from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="some-random-string"

)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Update this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)




app.include_router(superuser)
app.include_router(router)
app.include_router(user)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(user_page_router)
app.include_router(project)



#  =================================Created by Sandip 27-09-2024======================================
#          ======================================  ======================================
