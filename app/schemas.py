from pydantic import BaseModel
from typing import List, Optional

# -------------------- User Schemas --------------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # ✅ updated for Pydantic v2


# -------------------- Token Schemas --------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# -------------------- Task Schemas --------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False  # ✅ allow user to optionally set

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    owner_id: int

    class Config:
        from_attributes = True  # ✅ updated for Pydantic v2
