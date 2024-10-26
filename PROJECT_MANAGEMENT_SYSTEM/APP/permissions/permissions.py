from config.db import conn
from fastapi import Security, HTTPException, status
from bson import ObjectId

def check_permissions(required_permissions: list[str], user_id: str):
    # Fetch the user from the database
    user = conn.local.user.find_one({"_id": ObjectId(user_id)})
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if the user has the required permissions
    if required_permissions[0] not in user.get("permissions", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions",
        )

    return user