from pydantic import BaseModel, EmailStr, Field


class Project(BaseModel):
    __tablename__ = "project"
    project_name: str
    project_code: str
    start_date: str
    end_date: str


class Assign(BaseModel):
    __tablename__ = "assign"
    project: list[str]
    empa_user: str
    

    

