#  =================================Created by Sandip 27-09-2024======================================
#          ======================================  ======================================
from fastapi import APIRouter, Body, Depends, security, HTTPException, status
from models.user import UserLoginSchema, PyUser
from config.db import conn
from bson import ObjectId
from fastapi.responses import JSONResponse
from auth.auth_bearer import JWTBearer
from auth.auth_handler import sign_jwt, decode_jwt
from password_manager.password import verify_password
from models.token import Token
from schemas.user import userEntity, usersEntity


user = APIRouter()


def check_user(data: UserLoginSchema):
    users = conn.local.user.find({"email":data.email})
    for user in users:
        if user["email"] == data.email and verify_password(data.password,user["password"]):
            return True
    return False

def get_current_user(token: str = Depends(JWTBearer())) -> PyUser:
    decoded = decode_jwt(token)
    user_id = decoded.get('user_id')

    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID"    
        )

    user_data = conn.local.user.find_one({"_id": ObjectId(user_id)})

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    print(user_data)
    # Create and return a PyUser instance based on MongoDB data
    return PyUser(
        id=str(user_data["_id"]),
        mozi_id=user_data["mozi_id"],
        role=user_data["role"],
        name=user_data["name"],
        permissions=user_data["permissions"]
    )


@user.post("/login", tags=["user login"])
async def user_login(login_credentials:UserLoginSchema):
    if check_user(login_credentials):
        try:
            user = conn.local.user.find_one({"email":login_credentials.email})
            token_found = conn.local.tokens.find_one({"user":str(user["_id"])})
            if user is None:
                raise FileNotFoundError("User not found")
        except:
            return JSONResponse(content={"error":"user doesn't exists"}, status_code=status.HTTP_404_NOT_FOUND)

        if token_found is not None:       
            token = sign_jwt(str(user["_id"]))
            token.update({"user":str(user["_id"])})    
            token.update({"role":str(user["role"])})    
            conn.local.tokens.update_one({"user":str(user["_id"])},{"$set":{"access_token":token["access_token"],"refresh_token":token["refresh_token"]}})
            return JSONResponse(content=token, status_code=status.HTTP_200_OK)
        
        token = sign_jwt(str(user["_id"]))
        token.update({"user":str(user["_id"])})
        conn.local.tokens.insert_one(dict(token))
        print(token)
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"error": "Wrong login details!"}, status_code=status.HTTP_400_BAD_REQUEST)

@user.get("/logout", tags=["user logout"])
async def user_logout(token:str = Depends(JWTBearer())):
    deleted_token = conn.local.tokens.delete_one({"access_token":token})
    if deleted_token.deleted_count == 0:
        return JSONResponse(content={"error":"token not found!"}, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={"message":"logout successful"}, status_code=status.HTTP_200_OK)


@user.get("/get_all_users", dependencies=[Depends(JWTBearer())], tags=["Get All Users"])
async def get_all_users(current_user: dict = Depends(get_current_user)):
    try:
        users = usersEntity(conn.local.user.find())
        if users is None:
            return JSONResponse(content={"error":"No users found"}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=users, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error":str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
