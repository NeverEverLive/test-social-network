from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

from src.components.base_response.schema import BaseResponse


class PostSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID]
    like: Optional[int]
    dislike: Optional[int]
    text: str

    class Config:
        orm_mode = True
        validate_assignment = True
        allow_population_by_field_name = True


class PostResponse(BaseResponse):
    post: Optional[PostSchema]

    class Config:
        allow_population_by_field_name = True


class PostsResponse(BaseResponse):
    posts: Optional[List[PostSchema]]

    class Config:
        allow_population_by_field_name = True
