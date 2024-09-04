from bson import ObjectId
from config.db import conn
from schemas.user import userEntity
from schemas.project import ProjectEntity

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
        task = TaskEntity(conn.local.task.find_one(ObjectId(response1["task_id"])))
        project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
        user = userEntity(conn.local.user.find_one(ObjectId(response1["user_id"])))
        response2["task_id"] = task["task_id"]
        response2["task_name"] = task["task_name"]
        response2["created_by"] = task["created_by"]
        response2["project"] = project["project_name"]
        response2["username"] = user["name"]
        response2["start_date"] = task["start_date"]
        response2["end_date"] = task["end_date"]
        final_response.append(response2)

    return final_response