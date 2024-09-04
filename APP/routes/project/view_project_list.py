
from fastapi import APIRouter, Depends
from models.user import User
from models.project import Project, Assign
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from schemas.project import ProjectEntity, AssignEntity, ProjectsEntity


router = APIRouter()

@router.get('/viewprojectlist', dependencies=[Depends(JWTBearer())], tags=["View Projects List"])
async def ViewProjectList(current_user: dict = Depends(get_current_user)):
    try:
        check_permissions(["admin"], current_user.id)
    except:
        check_permissions(["admin"], current_user.id)

    try:
        project_list = ProjectsEntity(conn.local.project.find())
        return project_list
    except:
        return {"error": "No Project found"}