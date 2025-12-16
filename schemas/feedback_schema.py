from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class FeedbackCreate(BaseModel):
    parent_id: UUID
    child_id: UUID
    provider_id: UUID
    activity_id: UUID
    rating: int  # 1 – 5
    comment: Optional[str] = None


class FeedbackOut(BaseModel):
    feedback_id: UUID
    parent_id: UUID
    child_id: UUID
    provider_id: UUID
    activity_id: UUID
    rating: int
    comment: Optional[str]
    date: datetime
