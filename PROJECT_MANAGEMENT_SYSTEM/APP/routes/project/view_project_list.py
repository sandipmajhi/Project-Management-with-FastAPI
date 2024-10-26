
from fastapi import APIRouter, Depends, status
from models.user import User
from models.project import Project, Assign
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from schemas.project import ProjectEntity, AssignEntity, ProjectsEntity
from fastapi.responses import JSONResponse
from datetime import datetime

router = APIRouter()

def serialize_project(task):
    # Convert datetime fields to string
    task["created_at"] = task["created_at"].isoformat() if isinstance(task["created_at"], datetime) else task["created_at"]
    return task

@router.get('/viewprojectlist', dependencies=[Depends(JWTBearer())], tags=["View Projects List"])
async def ViewProjectList(current_user: dict = Depends(get_current_user)):
    try: 
        check_permissions(["emps"], str(current_user.id))
    except:
        try:
            check_permissions(["admin"], str(current_user.id))
        except:
            return JSONResponse(content={"error": "You don't have permission to create a project"}, status_code=status.HTTP_403_FORBIDDEN)

    try:
        project_list = ProjectsEntity(conn.local.project.find())

        project_list.sort(key=lambda x: x.get("created_at"), reverse=False)
        serialized_projects = [serialize_project(project) for project in project_list]
        return JSONResponse(content=serialized_projects, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"error": "No Project found"}, status_code=status.HTTP_404_NOT_FOUND)