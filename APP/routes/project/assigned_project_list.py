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
            assigned_project = AssignEntities(conn.local.assign.find())

            for index,assign_item in enumerate(assigned_project):
                project = ProjectEntity(conn.local.project.find_one(ObjectId(assign_item["project_id"])))
                user = userEntity(conn.local.user.find_one(ObjectId(assign_item["empa"])))
                assigned_project[index]["username"] = user["name"]
                assigned_project[index]["user_id"] = user["id"]
                assigned_project[index]["project_id"] = project["project_id"]
                assigned_project[index]["project_name"] = project["project_name"]
                assigned_project[index]["project_description"] = project["project_description"]
                assigned_project[index]["project_code"] = project["project_code"]
                assigned_project[index]["project_start_date"] = project["project_start_date"]
                assigned_project[index]["project_end_date"] = project["project_end_date"]



            # for index,assign_project in enumerate(assigned_emp):
            #     empa_user = userEntity(conn.local.user.find_one(ObjectId(assign_project["empa"])))
            #     project_name_list = []
            #     for project in assigned_emp[index]["project_id"]:
            #         project_entry = ProjectEntity(conn.local.project.find_one(ObjectId(project)))
            #         project_name_list.append({
            #         "project_id": str(project_entry["project_id"]),
            #         "project_name": project_entry["project_name"],
            #         "project_description": project_entry["project_description"],
            #         "project_code": project_entry["project_code"],
            #         "project_start_date": project_entry["project_start_date"],
            #         "project_end_date":project_entry["project_end_date"]
            #     })
            
            #     assigned_emp[index]["projects"]=project_name_list
            #     assigned_emp[index]["empa"] = empa_user["name"]
            #     assigned_emp[index]["user_id"] = empa_user["id"]
            #     # assigned_emp[index]["empa"] = empa_user["name"]
            #     del assigned_emp[index]["project_id"]
            return JSONResponse(content=assigned_project, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"error": f"Internal Server Error{e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif current_user.permissions == "empa":
        try:
            assigned_project = AssignEntities(conn.local.assign.find({"empa_user": current_user.id}))
            print(assigned_project)

            for index,assign_item in enumerate(assigned_project):
                project = ProjectEntity(conn.local.project.find_one(ObjectId(assign_item["project_id"])))
                user = userEntity(conn.local.user.find_one(ObjectId(assign_item["empa"])))
                assigned_project[index]["username"] = user["name"]
                assigned_project[index]["user_id"] = user["id"]
                assigned_project[index]["project_id"] = project["project_id"]
                assigned_project[index]["project_name"] = project["project_name"]
                assigned_project[index]["project_description"] = project["project_description"]
                assigned_project[index]["project_code"] = project["project_code"]
                assigned_project[index]["project_start_date"] = project["project_start_date"]
                assigned_project[index]["project_end_date"] = project["project_end_date"]
            
            # empa_user = userEntity(conn.local.user.find_one(ObjectId(assigned_project["empa"])))
            # project_name_list = []
            # for project in assigned_project["project_id"]:
            #     project_entry = ProjectEntity(conn.local.project.find_one(ObjectId(project)))
            #     project_name_list.append({
            #         "project_id": str(project_entry["project_id"]),
            #         "project_name": project_entry["project_name"],
            #         "project_description": project_entry["project_description"],
            #         "project_code": project_entry["project_code"],
            #         "project_start_date": project_entry["project_start_date"],
            #         "project_end_date":project_entry["project_end_date"]
            #     })
            
            # assigned_project["projects"]=project_name_list
            # assigned_project["empa"] = empa_user["name"]
            # assigned_project["user_id"] = empa_user["id"]
            # del assigned_project["project_id"]
            return JSONResponse(content=assigned_project, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message": f"No assigned project{e}"}, status_code=404)
        
    else:
        return JSONResponse(content={"status": "not enough permission"}, status_code=403)
       
        
    