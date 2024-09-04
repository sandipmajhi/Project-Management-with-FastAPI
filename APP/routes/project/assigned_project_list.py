from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from routes.user import get_current_user
from auth.auth_bearer import JWTBearer
from config.db import conn
from schemas.project import AssignEntities, ProjectsEntity, AssignEntity, ProjectEntity
from bson import ObjectId
from schemas.user import userEntity

router = APIRouter()

@router.get('/assignedprojectlist', dependencies=[Depends(JWTBearer())], tags=["Assigned Project List employee level"])
async def AssignedProjectList(current_user: dict = Depends(get_current_user)):
    print(current_user.permissions)
    if current_user.role == "Level S" or current_user.permissions == "admin":
        try:
            assigned_emp = AssignEntities(conn.local.assign.find())

            for index,assign_project in enumerate(assigned_emp):
                empa_user = userEntity(conn.local.user.find_one(ObjectId(assign_project["empa"])))
                project_name_list = []
                for project in assigned_emp[index]["project_id"]:
                    project_entry = ProjectEntity(conn.local.project.find_one(ObjectId(project)))
                    project_name_list.append(project_entry["project_name"])
            
                assigned_emp[index]["project_names"]=project_name_list
                assigned_emp[index]["empa"] = empa_user["name"]
                assigned_emp[index]["empa"] = empa_user["name"]
            return JSONResponse(content=assigned_emp, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"error": f"Internal Server Error{e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif current_user.permissions == "empa":
        try:
            assigned_project = AssignEntity(conn.local.assign.find_one({"empa_user": current_user.id}))
            print(assigned_project)
            
            empa_user = userEntity(conn.local.user.find_one(ObjectId(assigned_project["empa"])))
            project_name_list = []
            for project in assigned_project["project_id"]:
                project_entry = ProjectEntity(conn.local.project.find_one(ObjectId(project)))
                project_name_list.append(project_entry["project_name"])
            
            assigned_project["project_names"]=project_name_list
            assigned_project["empa"] = empa_user["name"]
            return JSONResponse(content=assigned_project, status_code=status.HTTP_200_OK)
        except:
            return JSONResponse(content={"message": "No assigned project"}, status_code=404)
        
    else:
        return JSONResponse(content={"status": "not enough permission"}, status_code=403)
       
        
    