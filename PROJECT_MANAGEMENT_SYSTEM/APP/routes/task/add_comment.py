from fastapi import APIRouter, Depends, status
from models.user import User
from models.adminTask import TaskAdmin, EditTaskAdmin, SaveEditTaskAdmin, UserComment, OwnerComment, ShowComment
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from fastapi.responses import JSONResponse
from schemas.task import AdminTaskEntities
from models.task import Date
from datetime import datetime
import sys, json

router = APIRouter()


@router.post('/add_comment_user', dependencies=[Depends(JWTBearer())], tags=["Add comment user"])
async def AddCommentUser(comment: UserComment, current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception:
    #     return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        comment = dict(comment)
        
        user_comment = conn.local.comment.find_one({"user_id":comment["user_id"],"task_id":comment["task_id"]})
        
        if user_comment is not None:
            new_comment = user_comment["comment"] +" "+"\n"+ comment["comment"]
            comment["comment"] = new_comment
            comment["datetime"] = datetime.strptime(comment["datetime"], "%d-%m-%Y %H:%M")
            ack = conn.local.comment.update_one({"user_id":comment["user_id"],"task_id":comment["task_id"]},{"$set":comment})
            if ack.acknowledged:
                return JSONResponse(content={"message":"comment added"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"error": "comment not added"}, status_code=status.HTTP_400_BAD_REQUEST)

        comment["created_at"] = datetime.now()
        comment["datetime"] = datetime.strptime(comment["datetime"], "%d-%m-%Y %H:%M")
        ack = conn.local.comment.insert_one(comment)
        if ack.acknowledged:
            return JSONResponse(content={"message":"comment added"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "comment not added"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




@router.post('/add_comment_owner', dependencies=[Depends(JWTBearer())], tags=["Add comment owner"])
async def AddCommentOwner(comment: OwnerComment, current_user: dict = Depends(get_current_user)):
    # try:
    #     # Check permissions
    #     check_permissions(["admin"], str(current_user.id))
    # except Exception:
    #     return JSONResponse(content={"error": "You don't have permission to create an admin-only task"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        comment = dict(comment)
        
        user_comment = conn.local.owner_comment.find_one({"user_id":comment["user_id"],"task_id":comment["task_id"]})
        
        if user_comment is not None:
            new_comment = user_comment["comment"] +" "+"\n"+ comment["comment"]
            comment["comment"] = new_comment
            comment["datetime"] = datetime.strptime(comment["datetime"], "%d-%m-%Y %H:%M")
            ack = conn.local.owner_comment.update_one({"user_id":comment["user_id"],"task_id":comment["task_id"]},{"$set":comment})
            if ack.acknowledged:
                return JSONResponse(content={"message":"comment added"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"error": "comment not added"}, status_code=status.HTTP_400_BAD_REQUEST)

        comment["created_at"] = datetime.now()
        comment["datetime"] = datetime.strptime(comment["datetime"], "%d-%m-%Y %H:%M")
        ack = conn.local.owner_comment.insert_one(comment)
        # ack = conn.local.comment.update_one({"task_id":comment["task_id"], "user_id":comment["user_id"]},{"$set":{"owner_comment":str(ack.inserted_id)}})
        if ack.acknowledged:
            return JSONResponse(content={"message":"comment added"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error": "comment not added"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.post('/show_comment_user', dependencies=[Depends(JWTBearer())], tags=["Show comment user"])
async def showCommentUser(showcomment: ShowComment, current_user: dict = Depends(get_current_user)):
    try:
        showcomment = dict(showcomment)

        comment = conn.local.comment.find_one({"task_id":showcomment["task_id"],  "user_id":current_user.id})
        
        if comment is not None:
            del comment['_id']
            comment["created_at"] = str(comment["created_at"])
            comment["datetime"] = str(comment["datetime"])
            user = conn.local.user.find_one({"_id":ObjectId(comment["user_id"])})
            comment["username"]=user["name"]
            owner_comment = conn.local.owner_comment.find_one({"task_id":comment["task_id"]})
            if owner_comment is not None:
                comment["owner_comment"] = owner_comment["comment"]
            admin_comment = conn.local.task_by_admin.find_one({"_id":ObjectId(showcomment["task_id"])})
            if admin_comment is not None:
                remarks = admin_comment["remarks"]
                comment["admin_comment"] = remarks
                comment["task_name"] = admin_comment["task_name"]

            # comments_list.append(comment)
                
            # print(comments_list)
            return JSONResponse(content=comment, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "No comment found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(sys.exc_info())
        return JSONResponse(content={"error":f"{e}"}, status_code=status.HTTP_400_BAD_REQUEST)



@router.post('/user_comments', dependencies=[Depends(JWTBearer())], tags=["User comments"])
async def showUserComments(showcomment: ShowComment, current_user: dict = Depends(get_current_user)):
    try:        
        showcomment = dict(showcomment)

        check_owner = conn.local.task_by_admin.find_one({"_id":ObjectId(showcomment["task_id"]), "task_owner":current_user.id})
        check_admin = conn.local.task_by_admin.find_one({"_id":ObjectId(showcomment["task_id"]), "created_by":current_user.id})
        
        print(check_admin, check_owner, current_user.id)
        if (check_owner is not None) or (check_admin is not None):

            comments = conn.local.comment.find({"task_id":showcomment["task_id"]})

            comments_list = []

            for comment in comments:
                print(comment,"hello")
                del comment['_id']
                comment["created_at"] = str(comment["created_at"])
                comment["datetime"] = str(comment["datetime"])
                user = conn.local.user.find_one({"_id":ObjectId(comment["user_id"])})
                comment["username"]=user["name"]
                owner_comment = conn.local.owner_comment.find_one({"task_id":comment["task_id"]})
                if owner_comment is not None:
                    comment["owner_comment"] = owner_comment["comment"]
                admin_comment = conn.local.task_by_admin.find_one({"_id":ObjectId(showcomment["task_id"])})
                if admin_comment is not None:
                    remarks = admin_comment["remarks"]
                    comment["admin_comment"] = remarks
                    comment["task_name"] = admin_comment["task_name"]

                comments_list.append(comment)
                
            print(comments_list)
            return JSONResponse(content=comments_list, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"error":"You are not the owner of the task"}, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(sys.exc_info())
        return JSONResponse(content={"error":f"{e}"}, status_code=status.HTTP_400_BAD_REQUEST)




@router.post('/show_comment_owner', dependencies=[Depends(JWTBearer())], tags=["Show comment owner"])
async def showComment(showcomment: ShowComment, current_user: dict = Depends(get_current_user)):
    try:
        showcomment = dict(showcomment)

        comment = conn.local.owner_comment.find_one({"task_id":showcomment["task_id"],  "user_id":current_user.id})
        print(comment)

        if comment is not None:
            del comment['_id']
            comment["created_at"] = str(comment["created_at"])
            comment["datetime"] = str(comment["datetime"])
            user = conn.local.user.find_one({"_id":ObjectId(comment["user_id"])})
            comment["username"]=user["name"]
            
            
            admin_comment = conn.local.task_by_admin.find_one({"_id":ObjectId(showcomment["task_id"])})
            if admin_comment is not None:
                remarks = admin_comment["remarks"]
                comment["admin_comment"] = remarks
                comment["task_name"] = admin_comment["task_name"]

            # comments_list.append(comment)
                
            # print(comments_list)
            return JSONResponse(content=comment, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message":"You havn't put any comment yet"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(sys.exc_info())
        return JSONResponse(content={"error":f"{e}"}, status_code=status.HTTP_400_BAD_REQUEST)

