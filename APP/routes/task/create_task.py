
from fastapi import APIRouter, Depends, status
from models.user import User
from models.task import Task
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from schemas.task import TaskEntity, TasksEntity
from schemas.sub_task import SubTaskEntity, SubTasksEntity
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/create_task', dependencies=[Depends(JWTBearer())] , tags=["Create a Task"])
async def CreateTask(Task: Task, current_user: dict = Depends(get_current_user)):
    try: 
        check_permissions(["empa"], str(current_user.id))
    except:
        return JSONResponse(content={"error":"You do not have enough permissions"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:
    
        print(Task)

        try:
            Task = dict(Task)
            Task["created_by"] = current_user.id
            task_object = conn.local.task.insert_one(Task)
        except Exception as e:
            x = conn.local.task.list_indexes()
            for index in x:
                print(index)
            return JSONResponse(content={"error": f'Task Not Created {e}'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

        
        response = TaskEntity(conn.local.task.find_one(ObjectId(task_object.inserted_id)))
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except:
        JSONResponse(content={"error": "Task not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    

@router.get("/view_all_tasks", dependencies=[Depends(JWTBearer())], tags=["View all Tasks"])
async def ViewTask(current_user: dict = Depends(get_current_user)):
    if current_user.permissions == "empb":
        try:
            response = SubTasksEntity(conn.local.sub_task.find({"created_by":str(current_user.id)}))
            # print(response)
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except:
            return JSONResponse(content={"status":"No task Created"}, status_code=status.HTTP_204_NO_CONTENT)
    elif current_user.permissions == "empc":
        try:
            response = SubTasksEntity(conn.local.sub_task_d.find({"created_by":str(current_user.id)}))
            # print(response)
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except:
            return JSONResponse(content={"status":"No task Created"}, status_code=status.HTTP_204_NO_CONTENT)
    elif current_user.permissions == "empa":
        try:
            response = TasksEntity(conn.local.task.find({"created_by":str(current_user.id)}))
            # print(response)
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except:
            return JSONResponse(content={"status":"No task Created"}, status_code=status.HTTP_204_NO_CONTENT)

    else:
        return JSONResponse(content={"error":"Not enough Permission"}, status_code=status.HTTP_403_FORBIDDEN)

