from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from models.task import AssignTask
from routes.user import get_current_user
from schemas.user import userEntity
from config.db import conn
from bson import ObjectId
from schemas.task import TaskEntity, TasksEntity, AssignTaskEntity, AssignTaskEntities
from schemas.project import ProjectEntity

router = APIRouter()

@router.post("/assigntask_levelb", dependencies=[Depends(JWTBearer())], tags=["Assign task to Level B"])
async def AssignTask_LevelB(assigntask: AssignTask, current_user: dict = Depends(get_current_user)):
    # Assign task to Level B
    # Return JSON response with status code 200
    if current_user.permissions == "empa":
        try:
            task_found = conn.local.task.find_one(ObjectId(assigntask.task))
            try:
                user_entity = conn.local.empb.find_one({"user":ObjectId(assigntask.user)})
                if user_entity is None:
                    return JSONResponse(content={"message": "User not found"}, status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return JSONResponse(content={"error":f"{e}"}, status_code=status.HTTP_400_BAD_REQUEST)

            try:
                already_assigned = conn.local.assigned_task_empb.find_one({"task":assigntask.task, "user":assigntask.user})
                if already_assigned is not None:
                    return JSONResponse(content={"error":"this task already assigned to this user"}, status_code=status.HTTP_400_BAD_REQUEST)
                try:
                    user_found = conn.local.user.find_one(ObjectId(assigntask.user))
                    if task_found is None:
                        return JSONResponse(content={"error":"task not found"}, status_code=status.HTTP_404_NOT_FOUND)
                    if user_found:
                        assigntask = dict(assigntask)
                        assigntask["assigned_by"]=current_user.id
                        inserted_obj = conn.local.assigned_task_empb.insert_one(dict(assigntask))
                        print(inserted_obj.inserted_id)
                        response = AssignTaskEntity(conn.local.assigned_task_empb.find_one(ObjectId(inserted_obj.inserted_id)))
                        final_response = {}
                        task = TaskEntity(conn.local.task.find_one(ObjectId(response["task_id"])))
                        project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
                        user = userEntity(conn.local.user.find_one(ObjectId(response["user_id"])))
                        final_response["task_name"] = task["task_name"]
                        final_response["project"] = project["project_name"]
                        final_response["username"] = user["name"]
                        final_response["start_date"] = task["start_date"]
                        final_response["end_date"] = task["end_date"]
                        final_response["start_time"] = task["start_time"]
                        final_response["end_time"] = task["end_time"]
                        
                        final_response.update({"status":"Task assigned successfully"})
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
        return JSONResponse(content={"error": "You do not have permission to assign task to Level B"}, status_code=status.HTTP_404_NOT_FOUND)

@router.get("/view_assigned_task_levelb", dependencies=[Depends(JWTBearer())], tags=["View tasks assigned to Level B"])
async def ViewTask_LevelB(current_user: dict = Depends(get_current_user)):
    if current_user.permissions == "empa":
        try:
            response = AssignTaskEntities(conn.local.assigned_task_empb.find({"assigned_by":str(current_user.id)}))
            print(response)
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except:
            return JSONResponse(content={"error":f"something went wrong {e}"}, status_code=status.HTTP_400_BAD_REQUEST)
            
    elif current_user.permissions == "empb":
        try:
            response = AssignTaskEntities(conn.local.assigned_task_empb.find({"user":current_user.id}))
            return JSONResponse(content=response, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"error":f"No task Assigned{e}"}, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return JSONResponse(content={"error":f"You do not have permission to see task of Level B users"}, status_code=status.HTTP_403_FORBIDDEN)
