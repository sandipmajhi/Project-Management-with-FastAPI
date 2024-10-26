from fastapi import APIRouter, Depends, status
from models.user import User
from models.adminTask import TaskAdmin, EditTaskAdmin, SaveEditTaskAdmin
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from fastapi.responses import JSONResponse
from schemas.task import AdminTaskEntities, AdminTaskEntity
from models.task import Date
from datetime import datetime, timedelta

router = APIRouter()


def is_valid_datetime(date_string):
    try:
        # Try to parse the string into a datetime object
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False



def serialize_task(task):
    # Convert datetime fields to string
    task["created_at"] = task["created_at"].isoformat() if isinstance(task["created_at"], datetime) else task["created_at"]
    return task

def serialize_task2(task):
    # Convert datetime fields to string
    task["start_date_and_time"] = task["start_date_and_time"].isoformat() if isinstance(task["start_date_and_time"], datetime) else task["start_date_and_time"]
    return task

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

        if task_admin["project"] == "":
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


        try:
            task_admin["start_date_and_time"] = task_admin["start_date_and_time"] if is_valid_datetime(task_admin["start_date_and_time"]) else datetime.strptime(task_admin["start_date_and_time"], "%d-%m-%Y %H:%M")
            task_admin["target_end_date_and_time"] = task_admin["target_end_date_and_time"] if is_valid_datetime(task_admin["target_end_date_and_time"]) else datetime.strptime(task_admin["target_end_date_and_time"], "%d-%m-%Y %H:%M")
            
            print(task_admin["start_date_and_time"], task_admin["target_end_date_and_time"])
        except ValueError as e:
            return JSONResponse(content={"error": f"Invalid date format: {e}"}, status_code=status.HTTP_400_BAD_REQUEST)

        # Insert task into the database
        conn.local.task_by_admin.insert_one(task_admin)
        return JSONResponse(content={"message": "Task created successfully"}, status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/save_edited_task_admin', dependencies=[Depends(JWTBearer())], tags=["Save edited Task - (ADMIN ONLY)"])
async def SaveTask(save_edit_task_admin: SaveEditTaskAdmin, current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception:
    #     return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        print(current_user.id)
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

        try:
            print(save_edit_task_admin["start_date_and_time"], save_edit_task_admin["target_end_date_and_time"])
            if save_edit_task_admin["start_date_and_time"] is not None:
                save_edit_task_admin["start_date_and_time"] = save_edit_task_admin["start_date_and_time"] if is_valid_datetime(save_edit_task_admin["start_date_and_time"]) else datetime.strptime(save_edit_task_admin["start_date_and_time"], "%d-%m-%Y %H:%M")
                save_edit_task_admin["target_end_date_and_time"] = save_edit_task_admin["target_end_date_and_time"] if is_valid_datetime(save_edit_task_admin["target_end_date_and_time"]) else datetime.strptime(save_edit_task_admin["target_end_date_and_time"], "%d-%m-%Y %H:%M")
                save_edit_task_admin["actual_end_date_and_time"] = save_edit_task_admin["actual_end_date_and_time"] if isinstance(save_edit_task_admin["actual_end_date_and_time"], datetime) else datetime.strptime(save_edit_task_admin["actual_end_date_and_time"], "%d-%m-%Y %H:%M")
                
        except ValueError as e:
            print(e)
            return JSONResponse(content={"error": f"Invalid date format: {e}"}, status_code=status.HTTP_400_BAD_REQUEST)

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
        return JSONResponse(content={"error": "You don't have permission to edit an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

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
                user_tasks[index]["assigned_ids"] = [current_user.id]
                
                    

            for index,task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"]="you are the owner"
                user_tasks.append(task)
                
            tasks = user_tasks
        
        print(tasks)
        # Sort the tasks by created_at field
        tasks.sort(key=lambda x: x.get("created_at"), reverse=True)

        # Serialize the tasks
        serialized_tasks = [serialize_task(task) for task in tasks]
        return JSONResponse(content=serialized_tasks, status_code=status.HTTP_200_OK)
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
            tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by":current_user.id, "$or":[{"status":"open"},{"status":"Open"}]}))
        else:
            owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner":current_user.id,  "$or":[{"status":"open"},{"status":"Open"}]}))

            
            user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}, "$or":[{"status":"open"},{"status":"Open"}]}))
                
            
            
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
    
    if date != '':
        date = datetime.strptime(date, "%d-%m-%Y")
        end_of_day = date + timedelta(hours=23, minutes=59, seconds=59)

        print(date)
        print(end_of_day)
    
    try:
        tasks = []  
        # Fetch all tasks based on the role of the user
        if current_user.role == 'Admin':
            if date == '':
                tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by": current_user.id}))
            else:
                tasks = AdminTaskEntities(conn.local.task_by_admin.find({"created_by": current_user.id, "start_date_and_time":{"$lte":end_of_day},"target_end_date_and_time":{"$gte":date},"status":"open"}))
        else:
            if date == '':
                owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner": current_user.id}))
                user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]}}))
            else:
                owner_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"task_owner": current_user.id,  "start_date_and_time":{"$lte":end_of_day},"target_end_date_and_time":{"$gte":date},"status":"open"}))
                user_tasks = AdminTaskEntities(conn.local.task_by_admin.find({"assigned": {"$in": [current_user.id]},  "start_date_and_time":{"$lte":end_of_day},"target_end_date_and_time":{"$gte":date},"status":"open"}))

            for index, task in enumerate(user_tasks):
                user_tasks[index]["assigned"] = [current_user.name]

            for index, task in enumerate(owner_tasks):
                if task["task_owner"] == current_user.id:
                    owner_tasks[index]["details"] = "you are the owner"
                user_tasks.append(task)

            tasks = user_tasks

       
        # tasks.sort(key=lambda x: parse_datetime(x.get("start_date_and_time")), reverse=False)
        for task in tasks:
            task["start_date_and_time"] = datetime.strptime(task["start_date_and_time"], "%Y-%m-%dT%H:%M:%S")
            

        # Now sort by start_date_and_time
        tasks.sort(key=lambda x: x["start_date_and_time"])


        # Serialize the tasks
        serialized_tasks = [serialize_task2(task) for task in tasks]
        return JSONResponse(content=serialized_tasks, status_code=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
