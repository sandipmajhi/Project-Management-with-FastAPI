from pydantic import BaseModel


from typing import Optional

class Task(BaseModel):
    """Task model."""
    __tablename__="task"
    task_name: str
    task_description: Optional[str]=None
    task_status: Optional[str]=None
    project: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str

class AssignTask(BaseModel):
    task: str
    user: str


