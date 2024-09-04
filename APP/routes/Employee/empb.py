from fastapi import APIRouter, Depends,status
from models.user import User
from config.db import conn
from bson import ObjectId
from schemas.empb import EmpbEntity, EmpbEntities
from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt, decode_jwt
from passlib.context import CryptContext
from password_manager.password import hash_password, verify_password
from permissions.permissions import check_permissions
from routes.user import get_current_user
from fastapi.responses import JSONResponse

empb = APIRouter()


@empb.post('/empb_register', dependencies=[Depends(JWTBearer())], tags=["Register Level-B User"])
async def EmpbRegister(user: User, current_user: dict = Depends(get_current_user)):
    
    try: 
        check_permissions(["admin"], str(current_user.id))
    except:
        return JSONResponse(content={"error": "You don't have permission to create a Level B user"}, status_code=status.HTTP_400_BAD_REQUEST)

    try:
        user.password = hash_password(user.password)
        user = dict(user)
        user.update({"permissions":"empb"})
        user.update({"role":"Level B"})

        try:
            print(user)
            user_object = conn.local.user.insert_one(user)
            dbObj = conn.local.empb.insert_one({"user":user_object.inserted_id})
        except Exception as e:
            return JSONResponse(content={"error: This email already Exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        access_token = sign_jwt(str(user["_id"]))
        response = EmpbEntity(conn.local.empb.find_one(ObjectId(dbObj.inserted_id)))
        response.update(access_token)
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse(content={"error": "User not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    

@empb.get('/empb_allusers', dependencies=[Depends(JWTBearer())], tags=["Show all Level-B Users"])
async def EmpsAllUsers(current_user: dict = Depends(get_current_user)):
    try:
        check_permissions(["emps"], str(current_user.id))
    except:
        try:
            check_permissions(["admin"], str(current_user.id))
        except:
            check_permissions(["empa"], str(current_user.id))

    response = EmpbEntities(conn.local.empb.find())
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)