from fastapi import APIRouter, status, Depends
from models.user import User
from routes.user import get_current_user
from config.db import conn
from bson import ObjectId
from schemas.user import userEntity, usersEntity
from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt, decode_jwt
from passlib.context import CryptContext
from password_manager.password import hash_password, verify_password
from fastapi.responses import JSONResponse
from permissions.permissions import check_permissions



superuser = APIRouter()




@superuser.post('/create_superuser', tags=["Create Superuser"])
async def createsuperuser(user: User, current_user: dict = Depends(get_current_user)):
    try: 
        check_permissions(["admin"], str(current_user.id))
    except:
        JSONResponse(content={"error": "Premission Denided"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:
        user.is_superuser = True
        user.password = hash_password(user.password)
        user = dict(user)
        user.update({"permissions":"admin"})
        user.update({"role":"Admin"})
       
        try:
            dbObj = conn.local.user.insert_one(user)
        except:
            return JSONResponse(content={"error: This email already Exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        access_token = sign_jwt(str(user["_id"]))
        response = userEntity(conn.local.user.find_one(ObjectId(dbObj.inserted_id)))
        response.update(access_token)
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={"error": "User not created"}, status_code=status.HTTP_400_BAD_REQUEST)