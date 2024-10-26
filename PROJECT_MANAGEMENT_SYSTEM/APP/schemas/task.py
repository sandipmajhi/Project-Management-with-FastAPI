from bson import ObjectId
from config.db import conn
from schemas.user import userEntity
from schemas.project import ProjectEntity
import copy
from datetime import datetime, timedelta

def convert_objectid_to_str(item):
    """Convert ObjectId fields in the item to string."""
    for key, value in item.items():
        if isinstance(value, ObjectId):
            item[key] = str(value)
        elif isinstance(value, list):
            item[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return item

def TaskEntity(item) -> dict:
    return {
        "task_id":str(item["_id"]),
        "task_name":item["task_name"],
        "task_description":item["task_description"],
        "task_status":item["task_status"],
        "project":item["project"],
        "start_date":item["start_date"],
        "end_date":item["end_date"],
        "start_time":item.get("start_time", None),
        "end_time":item.get("end_time", None),
        "created_by":item["created_by"]

    }

def TasksEntity(entity) -> list:
    return [TaskEntity(item) for item in entity]


def AssignTaskEntity(item) -> dict:
    # Convert ObjectId to string if present
    item = convert_objectid_to_str(item)
    
    return {
        "task_id": item.get("task", []),
        "user_id": str(item.get("user", ""))
    }


def AssignTaskEntities(entities) -> list:
    final_response = []
    for item in entities:
        response1 = AssignTaskEntity(item)
        response2 = {}
        try:
            task = TaskEntity(conn.local.task.find_one(ObjectId(response1["task_id"])))
            print("sandip",task)
            project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
            print("sandip",project)
            user = userEntity(conn.local.user.find_one(ObjectId(response1["user_id"])))
            print("sandip",user)
        except:
            return final_response
        response2["task_id"] = task["task_id"]
        response2["task_name"] = task["task_name"]
        response2["created_by"] = task["created_by"]
        response2["project"] = project["project_name"]
        response2["username"] = user["name"]
        response2["start_date"] = task["start_date"]
        response2["end_date"] = task["end_date"]
        response2["start_time"] = task["start_time"]
        response2["end_time"] = task["end_time"]

        final_response.append(response2)

    return final_response



def AdminTaskEntity(item) -> dict:
    # Convert ObjectId to string if present
    item = convert_objectid_to_str(item)

    start_date_and_time = item["start_date_and_time"].isoformat() if isinstance(item["start_date_and_time"], datetime) else str(item["start_date_and_time"])
    target_end_date_and_time = item["target_end_date_and_time"].isoformat() if isinstance(item["target_end_date_and_time"], datetime) else str(item["target_end_date_and_time"])
    
    actual_end_date_and_time = item.get("actual_end_date_and_time")
    actual_end_date_and_time = actual_end_date_and_time.isoformat() if isinstance(actual_end_date_and_time, datetime) else str(actual_end_date_and_time)
    created_at = item.get("created_at")
    created_at = created_at.isoformat() if isinstance(created_at, datetime) else str(created_at)
    
    return {
        "id": str(item["_id"]),
        "task_name": str(item["task_name"]),
        "project": item["project"],
        "task_description": item["task_description"],
        "dependency": item["dependency"],
        "status": item.get("status", None),
        "task_owner": item["task_owner"],
        "assigned": item.get("assigned", []),
        "start_date_and_time": start_date_and_time,
        "target_end_date_and_time": target_end_date_and_time,
        "target_duration": item["target_duration"],
        "actual_end_date_and_time": actual_end_date_and_time,
        "actual_duration": item.get("actual_duration", None),
        "remarks": item.get("remarks", None),
        "created_by": item.get("created_by", None),
        "created_at": created_at
    }

def AdminTaskEntities(entities) -> list:
    final_response = []
    users = []
    
    for item in entities:
        response1 = AdminTaskEntity(item)
        
        p_id = ObjectId(response1["project"])
        project = ProjectEntity(conn.local.project.find_one({"_id":p_id}))
        response1["project_name"] = project["project_name"]
        owner_id = ObjectId(response1["task_owner"])
        owner = userEntity(conn.local.user.find_one({"_id":owner_id}))
        response1["task_owner_name"] = owner["name"]
        assigned_user_ids = response1["assigned"]
        # assigned = userEntity(conn.local.user.find_one({"_id":assigned_id}))
        # response1["assigned_user_name"] = assigned["name"]
        print(assigned_user_ids)
        for assigned_user in assigned_user_ids:
            # Fetch assigned user from the database
            assigned_user = ObjectId(assigned_user)
            user = conn.local.user.find_one({"_id": assigned_user})
            if user is None:
                users.append("")
            else:
                users.append(user["name"])

            
        response1["assigned_user_ids"] = response1["assigned"]
        response1["assigned"] = users
        print(response1["assigned"])
        created_id = ObjectId(response1["created_by"])
        created = userEntity(conn.local.user.find_one({"_id":created_id}))
        response1["created_by"] = created["name"]
        list_of_response = copy.deepcopy(response1)
        final_response.append(list_of_response)

        response1["assigned"].clear()
    
    return final_response