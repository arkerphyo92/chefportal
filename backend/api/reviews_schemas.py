from ninja import Schema
from datetime import datetime

class ReviewsSchema(Schema):
    id: int
    reaction: bool
    favorite: bool
    comment: str
    rating: int
    recipe_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class ReviewCreateSchema(Schema):
    reaction: bool
    favorite: bool
    comment: str
    rating: int
    recipe_id: int
    user_id: int
    
class ReviewUpdateSchema(Schema):
    reaction: bool
    favorite: bool
    comment: str
    rating: int 
    
    class Config:
        from_attributes = True   
    
    
class ErrorSchema(Schema):
    message: str
        
