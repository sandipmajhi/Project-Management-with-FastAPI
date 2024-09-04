from config.db import conn
from bson import ObjectId
from schemas.user import userEntity, usersEntity

def EmpcEntity(item) -> dict:

    try:
        user_id = ObjectId(item["user"]) if not isinstance(item["user"], ObjectId) else item["user"]
    
    
        # Fetch the related user data
        related_data = userEntity(conn.local.user.find_one({"_id": user_id}))

        return {
            "empc_id": str(item["_id"]),
            "user_id": str(related_data["id"]),
            "name": related_data["name"],
            "role": related_data["role"],
            "email": related_data["email"]
        }
    except Exception as e:
        return {
            "empc_id": None,
            "user_id": None,
            "name": None,
            "role": None,
            "email": None
        }


def EmpcEntities(entity) -> list:
    return [EmpcEntity(item) for item in entity]