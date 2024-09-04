from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from models.task import AssignTask
from routes.user import get_current_user
from schemas.user import userEntity
from config.db import conn
from bson import ObjectId
from schemas.task import TaskEntity, TasksEntity, AssignTaskEntity, AssignTaskEntities
from schemas.sub_task import SubTaskEntity, AssignSubTaskEntities, AssignSubTaskEntity, SubTasksEntity
from schemas.project import ProjectEntity

router = APIRouter()

@router.post("/assigntask_levelc", dependencies=[Depends(JWTBearer())], tags=["Assign task to Level C"])
async def AssignTask_LevelC(assigntask: AssignTask, current_user: dict = Depends(get_current_user)):
    # Assign task to Level C
    # Return JSON response with status code 200
    if current_user.permissions == "empb":
        try:
            task_found = conn.local.sub_task.find_one(ObjectId(assigntask.task))
            try:
                already_assigned = conn.local.assigned_task_empc.find_one({"task":assigntask.task})
                if already_assigned is not None:
                    return JSONResponse(content={"error":"task already assigned"}, status_code=status.HTTP_400_BAD_REQUEST)
                try:
                    
                    user_found = conn.local.user.find_one(ObjectId(assigntask.user))
                    if task_found is None:
                        return JSONResponse(content={"error":"task not found"}, status_code=status.HTTP_404_NOT_FOUND)
                    if user_found:
                        assigntask = dict(assigntask)
                        assigntask["assigned_by"]=current_user.id
                        inserted_obj = conn.local.assigned_task_empc.insert_one(dict(assigntask))
                        print(inserted_obj.inserted_id)
                        response = AssignSubTaskEntity(conn.local.assigned_task_empc.find_one(ObjectId(inserted_obj.inserted_id)))
                        final_response = {}
                        print(response)
                        sub_task = SubTaskEntity(conn.local.sub_task.find_one(ObjectId(response["sub_task_id"])))
                        print(sub_task)
                        task = TaskEntity(conn.local.task.find_one(ObjectId(sub_task["task"])))
                        print(task)
                        project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
                        print(project)
                        user = userEntity(conn.local.user.find_one(ObjectId(response["user_id"])))
                        print(user)
                        final_response["task_name"] = sub_task["sub_task_name"]
                        final_response["task_name"] = task["task_name"]
                        final_response["project"] = project["project_name"]
                        final_response["username"] = user["name"]
                        final_response["start_date"] = sub_task["start_date"]
                        final_response["end_date"] = sub_task["end_date"]
                        
                        final_response.update({"status":"Sub Task assigned successfully"})
                        return JSONResponse(content=final_response, status_code=status.HTTP_200_OK)
                    else:
                        return JSONResponse(content={"error": "Server error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    return JSONResponse(content={"error": f"User not found{e}"}, status_code=status.HTTP_404_NOT_FOUND)
            except:
                return JSONResponse(content={"error":"task already assigned"}, status_code=status.HTTP_400_BAD_REQUEST)
        except:
            return JSONResponse(content={"error":"Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return JSONResponse(content={"error": "You do not have permission to assign task to Level C"}, status_code=status.HTTP_404_NOT_FOUND)

@router.get("/view_assigned_task_levelc", dependencies=[Depends(JWTBearer())], tags=["View Sub tasks assigned to Level C"])
async def ViewTask_LevelC(current_user: dict = Depends(get_current_user)):
    if current_user.permissions == "empb":
        try:
            
            response = AssignSubTaskEntities(conn.local.assigned_task_empc.find({"assigned_by":str(current_user.id)}))

            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"error":f"something went wrong {e}"}, status_code=status.HTTP_400_BAD_REQUEST)
            
    elif current_user.permissions == "empc":
        try:
            response = AssignSubTaskEntities(conn.local.assigned_task_empc.find({"user":current_user.id}))
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"error":f"something went wrong {e}"}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse(content={"error":f"You do not have permission to see task of Level C users"}, status_code=status.HTTP_403_FORBIDDEN)
