from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
