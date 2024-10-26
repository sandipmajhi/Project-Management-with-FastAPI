from config.db import conn
from bson import ObjectId
from datetime import datetime


def convert_objectid_to_str(item):
    """Convert ObjectId fields in the item to string."""
    for key, value in item.items():
        if isinstance(value, ObjectId):
            item[key] = str(value)
        elif isinstance(value, list):
            item[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return item

def ProjectEntity(item) -> dict:

    start_date = item.get("start_date")
    end_date = item.get("end_date")
    start_date = start_date.isoformat() if isinstance(start_date, datetime) else str(start_date)
    end_date = end_date.isoformat() if isinstance(end_date, datetime) else str(end_date)
    created_at = item.get("created_at")
    created_at = created_at.isoformat() if isinstance(created_at, datetime) else str(created_at)
    return {
        "project_id":str(item["_id"]),
        "project_name":item["project_name"],
        "project_description": item.get("project_description", None),
        "project_code":item["project_code"],
        "project_start_date":start_date,
        "project_end_date":end_date,
        "project_start_time":item.get("start_time",None),
        "project_end_time":item.get("end_time", None),
        "created_at":created_at

    }

def ProjectsEntity(entity) -> list:
    return [ProjectEntity(item) for item in entity]


def AssignEntity(item) -> dict:
    # Convert ObjectId to string if present
    item = convert_objectid_to_str(item)
    
    return {
        "project_id": item.get("project", ""),
        "empa": str(item.get("empa_user", ""))
    }



def AssignEntities(entities) -> list:
    return [AssignEntity(item) for item in entities]

