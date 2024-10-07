from config.db import conn
from bson import ObjectId
from schemas.user import userEntity, usersEntity

def EmpdEntity(item) -> dict:

    try:
        user_id = ObjectId(item["user"]) if not isinstance(item["user"], ObjectId) else item["user"]
    
    
        # Fetch the related user data
        related_data = userEntity(conn.local.user.find_one({"_id": user_id}))

        return {
            "empd_id": str(item["_id"]),
            "user_id": str(related_data["id"]),
            "mozi_id": str(related_data["mozi_id"]),
            "name": related_data["name"],
            "role": related_data["role"],
            "email": related_data["email"]
        }
    except Exception as e:
        return {
            "empd_id": None,
            "user_id": None,
            "mozi_id": None,
            "name": None,
            "role": None,
            "email": None
        }


def EmpdEntities(entity) -> list:
    return [EmpdEntity(item) for item in entity]