from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentBase(BaseModel):
    roll_no: str = Field(min_length=1, max_length=30)
    name: str = Field(min_length=1, max_length=120)
    department: str = Field(min_length=1, max_length=100)
    semester: str = Field(min_length=1, max_length=30)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=30)
    gender: Optional[str] = Field(default=None, max_length=30)
    address: Optional[str] = Field(default=None, max_length=300)

class StudentCreate(StudentBase): pass
class StudentUpdate(StudentBase): pass
class StudentOut(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
