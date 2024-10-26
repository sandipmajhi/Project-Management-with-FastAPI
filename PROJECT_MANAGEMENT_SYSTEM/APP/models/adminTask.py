from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class TaskAdmin(BaseModel):
    """TaskAdmin model for admin only tasks"""
    project:str
    task_name:str
    task_description:str
    dependency:str
    status:Optional[str]=None
    task_owner:str
    assigned:Optional[list[str]]=None
    start_date_and_time:str
    target_end_date_and_time:str
    target_duration:str
    actual_end_date_and_time:Optional[str]=None
    actual_duration:Optional[str]=None
    remarks:Optional[str]=None
    created_at: date = Field(default_factory=datetime.now)


class EditTaskAdmin(BaseModel):
    """TaskAdmin model for admin only tasks"""
    task_id:str


class SaveEditTaskAdmin(BaseModel):
    """TaskAdmin model for admin only tasks"""
    task_id:str
    task_name:str
    project:str
    task_description:str
    dependency:str
    status:Optional[str]=None
    task_owner:str
    assigned:Optional[list[str]]=None
    start_date_and_time:str
    target_end_date_and_time:str
    target_duration:str
    actual_end_date_and_time:Optional[str]=None
    actual_duration:Optional[str]=None
    remarks:Optional[str]=None


class UserComment(BaseModel):
    """Comment model for comments"""
    comment:str
    task_id: str
    user_id: str
    datetime: str

class OwnerComment(BaseModel):
    """Comment model for comments"""
    comment:str
    task_id: str
    user_id: str
    datetime: str

class ShowComment(BaseModel):
    """Comment model for comments"""
    task_id:str
    
    