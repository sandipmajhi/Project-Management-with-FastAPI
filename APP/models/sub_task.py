from pydantic import BaseModel


from typing import Optional

class SubTask(BaseModel):
    """Task model."""
    __tablename__="task"
    sub_task_name: str
    sub_task_description: Optional[str]=None
    sub_task_status: Optional[str]=None
    task: str
    start_date: str
    end_date: str

class AssignSubTask(BaseModel):
    sub_task: str
    user: str


