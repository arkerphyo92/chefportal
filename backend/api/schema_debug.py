from typing import Optional
import os
import sys
from datetime import datetime

# Add the directory containing your Django project to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Now import necessary Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chefportal.settings')
import django
django.setup()

# Now import your Ninja schema and other necessary modules
from ninja import Schema
from backend.api.reviews_schemas import ReviewsSchema  # Adjust the import path as needed

# Define your schema classes here
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

# Add more schema definitions as needed

# Example usage to validate and debug schema
def debug_recipe_schema():
    recipe_data = {
        'id': 1,
        'name': 'Test Recipe',
        'slug': 'test-recipe',
        'description': 'A test recipe',
        'tag': 'test',
        'user_id': 1,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
    }

    try:
        # Validate RecipeSchema instance
        recipe = RecipeSchema(**recipe_data)
        recipe.validate()  # Use .validate() to catch validation errors during debugging
        print("Recipe validated successfully:", recipe.dict())

    except Exception as e:
        print("Error validating RecipeSchema:", e)

# Call the debug function to test and validate RecipeSchema
if __name__ == "__main__":
    debug_recipe_schema()
