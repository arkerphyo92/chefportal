from ninja import Schema
from typing import Optional
from datetime import datetime
from .reviews_schemas import ReviewsSchema
class RecipeSchema(Schema):
    id: int
    name: str
    slug: str
    description: str
    tag: str
    category_id: Optional[int] = None
    food_type_id: Optional[int] = None
    reviews: list[ReviewsSchema] = []
    video_data: Optional[str] = None
    video_stream_data: Optional[str] = None
    pdf_data: Optional[str] = None
    image_data: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RecipeUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[str] = None
    category_id: Optional[int] = None
    food_type_id: Optional[int] = None
    user_id: Optional[int] = None    
        
    class Config:
        from_attributes = True

class RecipeCreateSchema(Schema):
    name: str
    description: str
    tag: str
    category_id: Optional[int] = None
    food_type_id: Optional[int] = None
    user_id: int

    class Config:
        from_attributes = True


class ErrorSchema(Schema):
    message: str