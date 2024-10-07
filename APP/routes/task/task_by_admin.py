from fastapi import APIRouter, Depends, status
from models.user import User
from models.adminTask import TaskAdmin, EditTaskAdmin, SaveEditTaskAdmin
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from fastapi.responses import JSONResponse
from schemas.task import AdminTaskEntities
from models.task import Date

router = APIRouter()

@router.post('/create_task_admin', dependencies=[Depends(JWTBearer())], tags=["Create Task - (ADMIN ONLY)"])
async def CreateTask(task_admin: TaskAdmin, current_user: dict = Depends(get_current_user)):
    try:
        # Check permissions
        check_permissions(["admin"], str(current_user.id))
    except Exception:
        return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        task_admin = dict(task_admin)
        task_admin["created_by"] = str(current_user.id)
        print(task_admin)

        if task_admin["project"] is "":
            return JSONResponse(content={"error": f"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)

        # Convert task_owner and assigned to ObjectId and handle invalid ID exceptions
        try:
            task_owner_id = ObjectId(task_admin["task_owner"])
            assigned_user_ids = task_admin["assigned"]
        except Exception as e:
            return JSONResponse(content={"error": f"Invalid ObjectId provided for task_owner or assigned{e}"}, status_code=status.HTTP_400_BAD_REQUEST)

        # Fetch task owner from the database
        task_owner = conn.local.user.find_one({"_id": task_owner_id})
        if task_owner is None:
            return JSONResponse(content={"error": "Task owner not found"}, status_code=status.HTTP_404_NOT_FOUND)

        for assigned_user in assigned_user_ids:
            # Fetch assigned user from the database
            assigned_user = ObjectId(assigned_user)
            user = conn.local.user.find_one({"_id": assigned_user})
            if user is None:
                return JSONResponse(content={"error": "Assigned user not found"}, status_code=status.HTTP_404_NOT_FOUND)

        # Insert task into the database
        conn.local.task_by_admin.insert_one(task_admin)
        return JSONResponse(content={"message": "Task created successfully"}, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/save_edited_task_admin', dependencies=[Depends(JWTBearer())], tags=["Save edited Task - (ADMIN ONLY)"])
async def SaveTask(save_edit_task_admin: SaveEditTaskAdmin, current_user: dict = Depends(get_current_user)):
    try:
        # Check permissions
        check_permissions(["admin"], str(current_user.id))
    except Exception:
        return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        save_edit_task_admin = dict(save_edit_task_admin)

        task_id = ObjectId(save_edit_task_admin["task_id"])

        del save_edit_task_admin["task_id"]

        if save_edit_task_admin["project"] is "":
            return JSONResponse(content={"error": f"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        # Convert task_owner and assigned to ObjectId and handle invalid ID exceptions
        try:
            task_owner_id = ObjectId(save_edit_task_admin["task_owner"])
            assigned_user_ids = save_edit_task_admin["assigned"]
        except Exception as e:
            return JSONResponse(content={"error": f"Invalid ObjectId provided for task_owner or assigned{e}"}, status_code=status.HTTP_400_BAD_REQUEST)

        # Fetch task owner from the database
        task_owner = conn.local.user.find_one({"_id": task_owner_id})
        if task_owner is None:
            return JSONResponse(content={"error": "Task owner not found"}, status_code=status.HTTP_404_NOT_FOUND)

        for assigned_user in assigned_user_ids:
            # Fetch assigned user from the database
            assigned_user = ObjectId(assigned_user)
            user = conn.local.user.find_one({"_id": assigned_user})
            if user is None:
                return JSONResponse(content={"error": "Assigned user not found"}, status_code=status.HTTP_404_NOT_FOUND)

        # Insert task into the database
        conn.local.task_by_admin.update_one({"_id":task_id}, {"$set":save_edit_task_admin})
        return JSONResponse(content={"message": "Task edited successfully"}, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.post('/edit_task_admin', dependencies=[Depends(JWTBearer())], tags=["Edit Task - (ADMIN ONLY)"])
async def EditTask(edit_task_admin: EditTaskAdmin, current_user: dict = Depends(get_current_user)):
    try:
        # Check permissions
        check_permissions(["admin"], str(current_user.id))
    except Exception:
        return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
       edit_task_admin = dict(edit_task_admin)
       task_id = ObjectId(edit_task_admin["task_id"])
       task = conn.local.task_by_admin.find({"_id":task_id})
       
       if task is None:
           return JSONResponse(content={"error": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
       else:
           task = AdminTaskEntities(task)
           return JSONResponse(content=task, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.get('/show_task_admin', dependencies=[Depends(JWTBearer())], tags=["Show Task Admin"])
async def ShowTask(current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception as e:
    #     return JSONResponse(content={"error": "You don't have permission to view an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:      
        tasks=[]   
        # Fetch all tasks from the database
        if current_user.role == 'Admin':
            
            tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by":current_user.id}))
        else:
            owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner":current_user.id}))

            
            user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}}))
                
            
            
            for index,task in enumerate(user_tasks):
                # if len(owner_tasks) == 0:
                user_tasks[index]["assigned"] = [current_user.name]
                
                    

            for index,task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"]="you are the owner"
                user_tasks.append(task)
                
            tasks = user_tasks
        
        return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.get('/open_tasks', dependencies=[Depends(JWTBearer())], tags=["Open Tasks"])
async def OpenTask(current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception as e:
    #     return JSONResponse(content={"error": "You don't have permission to view an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:      
        tasks=[]   
        # Fetch all tasks from the database
        if current_user.role == 'Admin':
            tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by":current_user.id, "status":"open"}))
        else:
            owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner":current_user.id,  "status":"open"}))

            
            user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}, "status":"open"}))
                
            
            
            for index,task in enumerate(user_tasks):
                # if len(owner_tasks) == 0:
                user_tasks[index]["assigned"] = [current_user.name]
                
                    

            for index,task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"]="you are the owner"
                user_tasks.append(task)
                
            tasks = user_tasks
        
        return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.get('/closed_tasks', dependencies=[Depends(JWTBearer())], tags=["Closed Tasks"])
async def ClosedTask(current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception as e:
    #     return JSONResponse(content={"error": "You don't have permission to view an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:      
        tasks=[]   
        # Fetch all tasks from the database
        if current_user.role == 'Admin':
            tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by":current_user.id, "status":"closed"}))
        else:
            owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner":current_user.id,  "status":"closed"}))

            
            user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}, "status":"closed"}))
                
            
            
            for index,task in enumerate(user_tasks):
                # if len(owner_tasks) == 0:
                user_tasks[index]["assigned"] = [current_user.name]
                
                    

            for index,task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"]="you are the owner"
                user_tasks.append(task)
                
            tasks = user_tasks
        
        return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@router.post('/tasks_by_date', dependencies=[Depends(JWTBearer())], tags=["Task By Date"])
async def ShowTaskByDate(date: Date, current_user: dict = Depends(get_current_user)):
    date = date.date
    d = date[:2]
    m = date[3:5]
    y = date[6:10]
    
    try:
        tasks = []  
        # Fetch all tasks based on the role of the user
        if current_user.role == 'Admin':
            tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by": current_user.id}))
        else:
            owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner": current_user.id}))
            user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}}))

            for index, task in enumerate(user_tasks):
                user_tasks[index]["assigned"] = [current_user.name]

            for index, task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"] = "you are the owner"
                user_tasks.append(task)

            tasks = user_tasks

        # Use list comprehension to filter the tasks based on the date
        tasks = [
            task for task in tasks
            if task["start_date_and_time"][:2] == d
            and task["start_date_and_time"][3:5] == m
            and task["start_date_and_time"][6:10] == y
        ]

        return JSONResponse(content=tasks, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
