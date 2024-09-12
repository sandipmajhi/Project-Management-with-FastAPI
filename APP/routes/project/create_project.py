
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

router = APIRouter()

@router.post('/create_project', dependencies=[Depends(JWTBearer())] , tags=["Create a Project"])
async def CreateProject(project: Project, current_user: dict = Depends(get_current_user)):
    try: 
        check_permissions(["emps"], str(current_user.id))
    except:
        try:
            check_permissions(["admin"], str(current_user.id))
        except:
            return JSONResponse(content={"error": "You don't have permission to create a project"}, status_code=status.HTTP_403_FORBIDDEN)
    
    try:
    
        print(project)
        try:
            # project.start_date = str(project.start_date)
            project.end_date = str(project.end_date)
            try:
                project_object = conn.local.project.insert_one(dict(project))
            except Exception as e:
                return JSONResponse(content={"error": f'{e}'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return JSONResponse(content={"error":f"{e}"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        response = ProjectEntity(conn.local.project.find_one(ObjectId(project_object.inserted_id)))
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content={"error": "Project not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    

