from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

class Project(BaseModel):
    __tablename__ = "project"
    project_name: str
    project_description: str
    project_code: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    created_at: date = Field(default_factory=datetime.now)


class Assign(BaseModel):
    __tablename__ = "assign"
    project: str
    empa_user: str
    assigned_at: date = Field(default_factory=datetime.now)
    

    

