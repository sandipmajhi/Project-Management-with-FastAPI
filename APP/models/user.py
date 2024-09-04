from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from sqlalchemy import Integer, ForeignKey
from datetime import date, datetime

class User(BaseModel):
    __tablename__ = 'user'
    name: str
    email: EmailStr 
    is_superuser: bool = False
    created_at: date = Field(default_factory=datetime.now)
    password: str

class PyUser(BaseModel):
    id: str
    role: str
    permissions: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
