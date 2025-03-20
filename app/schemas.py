from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    address: Optional[str] = Field(None, example="123 Main St, City, Country")
    phone: Optional[str] = Field(None, example="+1234567890")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, example="Jane Doe")
    email: Optional[EmailStr] = Field(None, example="jane.doe@example.com")
    address: Optional[str] = Field(None, example="456 Oak St, City, Country")
    phone: Optional[str] = Field(None, example="+0987654321")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip() if v else None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class UserList(BaseModel):
    users: list[UserResponse]
    count: int

class DeleteResponse(BaseModel):
    message: str