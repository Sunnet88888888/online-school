from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field



class CreateCommentRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
    )


class UpdateCommentRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
    )


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    text: str
    created_at: datetime
    updated_at: datetime | None