from ninja import Schema
from typing import Optional
from datetime import datetime

class RecipeSearchSchema(Schema):
    search_query: Optional[str] = None
    category_id: Optional[int] = None
    food_type_id: Optional[int] = None
    min_rating: Optional[int] = None

class RecipeResponseSchema(Schema):
    id: int
    name: str
    slug: str
    description: str
    tag: str
    # avg_rating: Optional[float] = None
    category: Optional[str] = None
    food_type: Optional[str] = None
    video_path: Optional[str] = ""
    video_stream_path: Optional[str] = ""
    pdf_path: Optional[str] = ""
    image_path: Optional[str] = ""
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   
    
class ErrorSchema(Schema):
    message: str
        
