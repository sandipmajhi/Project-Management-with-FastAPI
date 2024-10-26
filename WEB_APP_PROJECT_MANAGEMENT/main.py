#  =================================Created by Sandip 27-09-2024======================================
#          ======================================  ======================================
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from page_routing.project import project
from page_routing.user import user_page_router

from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_page_router)
app.include_router(project)

app.add_middleware(
    SessionMiddleware,
    secret_key="some-random-string"

)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

