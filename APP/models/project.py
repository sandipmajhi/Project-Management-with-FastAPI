from pydantic import BaseModel, EmailStr, Field


class Project(BaseModel):
    __tablename__ = "project"
    project_name: str
    project_description: str
    project_code: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str


class Assign(BaseModel):
    __tablename__ = "assign"
    project: str
    empa_user: str
    

    

