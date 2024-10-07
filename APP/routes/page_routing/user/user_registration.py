from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from auth.auth_bearer import JWTBearer
import requests


user = APIRouter()

templates = Jinja2Templates(directory="templates")
