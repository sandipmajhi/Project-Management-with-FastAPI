
from fastapi import APIRouter, Depends, status
from models.user import User
from models.sub_task import SubTask, AssignSubTask
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from schemas.sub_task import SubTaskEntity, SubTasksEntity, AssignSubTaskEntities, AssignSubTaskEntity
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/create_sub_task', dependencies=[Depends(JWTBearer())] , tags=["Create a Sub Task"])
async def CreateSubTask(subTask: SubTask, current_user: dict = Depends(get_current_user)):
    try: 
        check_permissions(["empb"], str(current_user.id))
    except:
        return JSONResponse(content={"error":"You do not have enough permissions"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:
    
        print(subTask)

        try:
            subTask = dict(subTask)
            subTask["created_by"] = current_user.id
            sub_task_object = conn.local.sub_task.insert_one(subTask)
        except Exception as e:
            return JSONResponse(content={"error": f'Task Not Created {e}'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

        print(sub_task_object.inserted_id)
        response = SubTaskEntity(conn.local.sub_task.find_one(ObjectId(sub_task_object.inserted_id)))
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except:
        JSONResponse(content={"error": "Task not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    

