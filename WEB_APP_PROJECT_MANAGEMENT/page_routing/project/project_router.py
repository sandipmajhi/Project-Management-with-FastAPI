from fastapi import APIRouter, Depends, status
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests, json
import httpx
from fastapi.responses import JSONResponse
from datetime import datetime

project = APIRouter()

templates = Jinja2Templates(directory="templates")

project_url = 'http://127.0.0.1:8000/create_project'

task_url = 'http://127.0.0.1:8000/create_task_admin'

open_task_url = 'http://127.0.0.1:8000/edit_task_admin'
save_edited_task_url = 'http://127.0.0.1:8000/save_edited_task_admin'





#  include  dependencies=[Depends(JWTBearer())],
@project.get('/pages/project_create', response_class=HTMLResponse)
async def ProjectCreate(request: Request):
    token = request.session.get("token")
    print(token)
    return templates.TemplateResponse("project_form.html", {"request": request,"token": token})

@project.get('/pages/task_create', response_class=HTMLResponse)
async def Task(request: Request):
    token = request.session.get("token")
    print(token)
    return templates.TemplateResponse("task_form.html", {"request": request,"token": token})



@project.post('/pages/project_create', response_class=HTMLResponse)
async def Project(request: Request):
    form_data = await request.form()
    # token = request.query_params.get("token")
    token = request.session.get("token")
    
    headers = {"Authorization":f"Bearer {token}"}
    project_data = dict(form_data)
    print(project_data)
 
    project_insert = requests.post(project_url, data=json.dumps(project_data),headers=headers)
    print(project_insert.text)
    if project_insert.status_code == 200:
        return templates.TemplateResponse("project_form.html", {"request": request,"success": True, "token":token})
    else:
        return templates.TemplateResponse("project_form.html", {"request": request,"success": False, "token":token})

@project.post('/pages/task_create', response_class=HTMLResponse)
async def TaskCreate(request: Request):
    print("Processing task creation")
    try:
        # Fetch the token from the header
        token = request.headers.get('Authorization')
        print(f"Token: {token}")

        if not token:
            return JSONResponse(content={"error": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}
        task_data = await request.json()  # Ensure that the client sends JSON data

        print(f"Received Task Data: {task_data}")

        async with httpx.AsyncClient() as client:
            task_insert = await client.post(task_url, json=task_data, headers=headers)

        print(f"Task creation response: {task_insert.status_code}, {task_insert.text}")

        # Check if task creation was successful
        if task_insert.status_code == 200:
            print("Task successfully created")
            return JSONResponse(content={"success": True, "task_data": task_data}, status_code=200)
        else:
            print(f"Task creation failed: {task_insert.status_code} - {task_insert.text}")
            return JSONResponse(content={"error": "Task creation failed"}, status_code=task_insert.status_code)

    except Exception as e:
        print(f"Exception occurred: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@project.get('/pages/view_projects', response_class=HTMLResponse)
async def ViewProjects(request: Request):
    token = request.session.get("token")
    return templates.TemplateResponse("project_table.html", {"request": request,"token": token},status_code=status.HTTP_200_OK)


@project.get('/pages/view_tasks', response_class=HTMLResponse)
async def ViewTasks(request: Request):
    token = request.session.get("token")
    return templates.TemplateResponse("task_table.html", {"request": request,"token": token},status_code=status.HTTP_200_OK)

@project.get('/pages/task_edit_page', response_class=HTMLResponse)
async def TaskEditPage(request: Request):
    token = request.session.get("token")
    request.session["token"] = token
    task_id = request.query_params.get("id")
    print(task_id)

    data = {"task_id":task_id}
    headers = {"Authorization":f"Bearer {token}"}
    task_response = requests.post(open_task_url, data=json.dumps(data), headers=headers)
    task_response = task_response.json()[0]
    print(task_response)
    
    return templates.TemplateResponse("task_edit_form.html", {"request":request, "token":token, "task":task_response}, status_code=status.HTTP_200_OK)

@project.post('/pages/edit_task_api', response_class=HTMLResponse)
async def EditTask(request: Request):
    token = request.session.get("token")

    print(token)

    headers = {"Authorization": f"Bearer {token}"}
    task_data = await request.json() 
    async with httpx.AsyncClient() as client:
            task_insert = await client.post(save_edited_task_url, json=task_data, headers=headers)

    print(f"Task Edit response: {task_insert.status_code}, {task_insert.text}")

    # Check if task creation was successful
    if task_insert.status_code == 201:
        print("Task successfully edited")
        return JSONResponse(content={"success": True}, status_code=200)
    else:
        print(f"Task edit failed: {task_insert.status_code} - {task_insert.text}")
        return JSONResponse(content={"error": "Task creation failed"}, status_code=task_insert.status_code)

    