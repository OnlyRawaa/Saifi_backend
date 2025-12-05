from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class ChildBase(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    birthdate: str
    gender: str = Field(..., pattern="^(Male|Female|male|female)$")
    interests: Optional[List[str]] 


class ChildCreate(ChildBase):
    parent_id: str


class ChildUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    interests: Optional[List[str]] = None
