from fastapi import APIRouter, Depends, status
from models.user import User
from config.db import conn
from bson import ObjectId
from schemas.emps import EmpsEntity, EmpsEntities
from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt, decode_jwt
from passlib.context import CryptContext
from password_manager.password import hash_password, verify_password
from routes.user import get_current_user
from permissions.permissions import check_permissions
from fastapi.responses import JSONResponse



emps = APIRouter()




@emps.post('/emps_register', dependencies=[Depends(JWTBearer())] , tags=["Register Level-S User"])
async def EmpsRegister(user: User, current_user: dict = Depends(get_current_user)):
    check_permissions(["admin"], str(current_user.id))
    try:
        user.password = hash_password(user.password)
        user = dict(user)
        if user["email"]=="":
            return JSONResponse(content={"error":"email is required"}, status_code=status.HTTP_206_PARTIAL_CONTENT)
        user.update({"permissions":"emps"})
        user.update({"role":"Level S"})

        try:
            user_object = conn.local.user.insert_one(user)
            dbObj = conn.local.emps.insert_one({"user":user_object.inserted_id})
        except:
            return JSONResponse(content={"error: This email already Exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        access_token = sign_jwt(str(user["_id"]))
        response = EmpsEntity(conn.local.emps.find_one(ObjectId(dbObj.inserted_id)))
        response.update(access_token)
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={"message": "User not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    
@emps.get('/emps_allusers', dependencies=[Depends(JWTBearer())], tags=["Show all Level-S Users"])
async def EmpsAllUsers(current_user: dict = Depends(get_current_user)):
    check_permissions(["admin"], str(current_user.id))
    response = EmpsEntities(conn.local.emps.find())
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)