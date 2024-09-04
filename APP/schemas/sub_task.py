from bson import ObjectId
from config.db import conn
from schemas.user import userEntity
from schemas.project import ProjectEntity
from schemas.task import TaskEntity

def convert_objectid_to_str(item):
    """Convert ObjectId fields in the item to string."""
    for key, value in item.items():
        if isinstance(value, ObjectId):
            item[key] = str(value)
        elif isinstance(value, list):
            item[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return item

def SubTaskEntity(item) -> dict:
    return {
        "sub_task_id":str(item["_id"]),
        "sub_task_name":item["sub_task_name"],
        "sub_task_description":item["sub_task_description"],
        "sub_task_status":item["sub_task_status"],
        "task":item["task"],
        "start_date":item["start_date"],
        "end_date":item["end_date"],
        "created_by":item["created_by"]

    }

def SubTasksEntity(entity) -> list:
    return [SubTaskEntity(item) for item in entity]


def AssignSubTaskEntity(item) -> dict:
    # Convert ObjectId to string if present
    item = convert_objectid_to_str(item)
    print(item["_id"], item["user"])
    return {
        "sub_task_id": str(item["task"]),
        "user_id": str(item["user"])
    }


def AssignSubTaskEntities(entities) -> list:
    print(entities)
    final_response = []
    for item in entities:
        response1 = AssignSubTaskEntity(item)
        response2 = {}
        sub_task = SubTaskEntity(conn.local.sub_task.find_one(ObjectId(response1["sub_task_id"])))
        task = TaskEntity(conn.local.task.find_one(ObjectId(sub_task["task"])))
        project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
        user = userEntity(conn.local.user.find_one(ObjectId(response1["user_id"])))
        response2["sub_task_id"] = sub_task["sub_task_id"]
        response2["sub_task_name"] = sub_task["sub_task_name"]
        response2["task_name"] = task["task_name"]
        response2["created_by"] = sub_task["created_by"]
        response2["project"] = project["project_name"]
        response2["username"] = user["name"]
        response2["start_date"] = sub_task["start_date"]
        response2["end_date"] = sub_task["end_date"]
        final_response.append(response2)

    return final_response



def AssignSubTaskEntitiesD(entities) -> list:
    print(entities)
    final_response = []
    for item in entities:
        response1 = AssignSubTaskEntity(item)
        response2 = {}
        print(item)
        sub_task_d = SubTaskEntity(conn.local.sub_task_d.find_one(ObjectId(item["task"])))
        print(sub_task_d)
        sub_task = SubTaskEntity(conn.local.sub_task.find_one(ObjectId(sub_task_d["task"])))
        print(sub_task)
        task = TaskEntity(conn.local.task.find_one(ObjectId(sub_task["task"])))
        print(task)
        project = ProjectEntity(conn.local.project.find_one(ObjectId(task["project"])))
        user = userEntity(conn.local.user.find_one(ObjectId(response1["user_id"])))
        response2["sub_task_id"] = sub_task["sub_task_id"]
        response2["sub_task_name"] = sub_task["sub_task_name"]
        response2["task_name"] = task["task_name"]
        response2["created_by"] = sub_task["created_by"]
        response2["project"] = project["project_name"]
        response2["username"] = user["name"]
        response2["start_date"] = sub_task["start_date"]
        response2["end_date"] = sub_task["end_date"]
        final_response.append(response2)

    return final_response