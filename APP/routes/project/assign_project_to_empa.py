
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from models.user import User
from models.project import Project, Assign
from config.db import conn
from bson import ObjectId
from auth.auth_bearer import JWTBearer
from routes.user import get_current_user
from permissions.permissions import check_permissions
from schemas.project import ProjectEntity, AssignEntity, ProjectsEntity

router = APIRouter()


@router.post('/assign_project_to_empa', dependencies=[Depends(JWTBearer())] , tags=["Assign project to Level-A user"])
async def AssignProjecttoEmpa(assign: Assign, current_user: dict = Depends(get_current_user)):

    try: 
        check_permissions(["emps"], str(current_user.id))
    except:
        try:
            check_permissions(["admin"], str(current_user.id))
        except:
            return JSONResponse(content={"message":"You don't have permission to create a project"}, status_code=status.HTTP_403_FORBIDDEN)
    
    if assign is not None:        
        print(dict(assign))

        try:

            # Checking if the project is exists 
            for projects in assign.project:
                project_availability = conn.local.project.find_one(ObjectId(projects))
                # If the Project is Not Exists
                if project_availability is None:
                    return JSONResponse(content={"message":"Project not found"}, status_code=status.HTTP_404_NOT_FOUND)
                
            # Checking if the user is exists
            user_availability = conn.local.empa.find_one({"user":ObjectId(assign.empa_user)})
            print(user_availability)
            # If the user is not exists return "user not found"
            if user_availability is None:
                return JSONResponse(content={"message":"User not Found"}, status_code=status.HTTP_404_NOT_FOUND)


            # If the project is already assigned to some user
            project_is_assigned = conn.local.assign.find_one({"project": {"$in": assign.project}})
            if project_is_assigned is not None:
                return JSONResponse(content={"message":"Project is already assigned to some user"}, status_code=status.HTTP_306_RESERVED)

            # Checking if this user is already assigned into some project
            old_assign = conn.local.assign.find_one({"empa_user":assign.empa_user})
            print(old_assign)


            # If the user is already assigned into some project then append the project into that user's project assign list
            if old_assign is not None:
                conn.local.assign.update_one({"empa_user":assign.empa_user}, {"$addToSet":{"project": {"$each": assign.project}}})
                
                response = AssignEntity(conn.local.assign.find_one({"empa_user":assign.empa_user}))
                return JSONResponse(content=response, status_code=status.HTTP_200_OK)

            else:
                # If the user is not assigned into any project then create a new document into assign collection
                try:
                    assign_object = conn.local.assign.insert_one(dict(assign))
                    response = AssignEntity(conn.local.assign.find_one(ObjectId(assign_object.inserted_id)))
                    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

                except:
                    return JSONResponse(content={"message":"assign already exists"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)
            
        except Exception as e:
            return {
            "status":f"{e}"
        }
        
    else:
        return {"message": "Project not Assigned"}        
