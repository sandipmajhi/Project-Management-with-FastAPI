from fastapi import APIRouter, Query
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import requests, json



user = APIRouter()

templates = Jinja2Templates(directory="templates")

login_url = 'http://13.234.238.178/login'
logout_url = 'http://13.234.238.178/logout'

@user.get('/', response_class=HTMLResponse)
async def Index(request: Request):
    token = request.session.get("token")
    return templates.TemplateResponse("index.html", {"request": request, "token":token})

@user.get('/pages/login', response_class=HTMLResponse)
async def LoginPage(request: Request):
    
    return templates.TemplateResponse("login.html", {"request": request})

@user.post('/pages/login', response_class=RedirectResponse)
async def Login(request: Request):
    try:
        form_data= await request.form()
        login_data = dict(form_data)
        print(login_data)
        login_response = requests.post(login_url, data=json.dumps(login_data))
        res = (login_response.json())
        request.session["token"] = res["access_token"]
        redirect_url = request.url_for('Index')
        return RedirectResponse(url=redirect_url, status_code=303)

    except Exception as e:
        print(e)
    return templates.TemplateResponse("login.html", {"request": request})


@user.get('/pages/logout', response_class=HTMLResponse)
async def Logout(request: Request):

    try:
        token = request.headers.get("Authorization")
        print(token)
        logout_response = requests.get(logout_url, headers={"Authorization": f"{token}"})
        request.session.pop("token", None)
        redirect_url = request.url_for('LoginPage')
        res = logout_response.json()
        if res["detail"] == "Invalid token or expired token.":
            print(res["detail"])
            return templates.TemplateResponse("login.html", {"request": request, "token":False}, status_code=400)
        return templates.TemplateResponse("login.html", {"request": request})
    except:
        return RedirectResponse(url=request.url_for('Index'), status_code=303)

