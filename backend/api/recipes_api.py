from ninja.errors import HttpError
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from ..models import Recipe, Category, FoodType, User, Review
from .recipes_schemas import RecipeSchema, RecipeCreateSchema, ErrorSchema, RecipeUpdateSchema
from .reviews_schemas import ReviewsSchema
import os
from ninja import Router, File
from ninja.files import UploadedFile
from ninja.errors import HttpError, ValidationError
from django.http import JsonResponse
# Pagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, HttpResponseNotFound

# JWT
from .jwt import JWTAuthBearer


# Permissions
from .decorators import group_required

recipe = Router(tags=["recipes"])

#JWT
jwt_auth = JWTAuthBearer()

@recipe.get("/recipes", response=list[RecipeSchema], auth=jwt_auth)
@group_required(group_name="recipe")  # Apply the custom decorator with group name
def list_recipes(request, page: int = 1):
    """
    List recipes with pagination.

    Args:
        page (int, optional): The page number to retrieve. Defaults to 1.
    """
    recipes = Recipe.objects.all()
    
    PAGE_SIZE = 10
    paginator = Paginator(recipes, PAGE_SIZE)  # Use PAGE_SIZE for custom size

    try:
        paginated_recipes = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest("Invalid page number")
    except EmptyPage:
        return HttpResponseNotFound("No recipes found for this page")
    # Convert queryset to list of RecipeSchema
    recipe_list = []
    for recipe in paginated_recipes.object_list:
        recipe_data = RecipeSchema.from_orm(recipe).dict() # model and schema all data
        ## if want to update partially
        # reviews = Review.objects.filter(recipe_id=recipe.id)
        # recipe_data = RecipeSchema(
        #     id=recipe.id,
        #     name=recipe.name,
        #     slug=recipe.slug,
        #     description=recipe.description,
        #     tag=recipe.tag,
        #     category_id=recipe.category_id,
        #     food_type_id=recipe.food_type_id,
        #     video_data=recipe.video_data.name if recipe.video_data else None,
        #     video_stream_data=recipe.video_stream_data.name if recipe.video_stream_data else None,
        #     pdf_data=recipe.pdf_data.name if recipe.pdf_data else None,
        #     image_data=recipe.image_data.name if recipe.image_data else None,
        #     user_id=recipe.user.id,
        #     created_at=recipe.created_at,
        #     updated_at=recipe.updated_at,
        #     reviews=[ReviewsSchema.from_orm(review).dict() for review in reviews]  # Convert reviews to schema format
        # )

        reviews = Review.objects.filter(recipe_id=recipe.id)
        recipe_data['reviews'] = [ReviewsSchema.from_orm(review).dict() for review in reviews]
        recipe_list.append(recipe_data)

    return recipe_list


@recipe.get("/recipes/{recipe_slug}", response=RecipeSchema)
# @group_required(group_name="recipe")
def get_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    reviews = Review.objects.filter(recipe_id=recipe.id)
    recipe_data = RecipeSchema.from_orm(recipe).dict()  # Convert Recipe object to dictionary
    
    # Update the recipe_data dictionary with reviews data
    recipe_data['reviews'] = [ReviewsSchema.from_orm(review).dict() for review in reviews]
    
    return recipe_data



# Create recipe endpoint
@recipe.post("/recipes", response={200: RecipeSchema, 404: ErrorSchema, 400: ErrorSchema})
def create_recipe(request, data_in: RecipeCreateSchema, 
                  video_file: UploadedFile = File(...), 
                  video_stream_file: UploadedFile = File(...), 
                  pdf_file: UploadedFile = File(...), 
                  image_file: UploadedFile = File(...)):
    # try:
        # Validate input data
        # if not data_in.name:
        #     raise ValidationError(
        #         detail=[
        #             {"loc": ["body", "name"], "msg": "Name is required.", "type": "value_error.missing"}
        #         ]
        #     )
        # if not data_in.description:
        #     raise ValidationError(
        #         detail=[
        #             {"loc": ["body", "description"], "msg": "Description is required.", "type": "value_error.missing"}
        #         ]
        #     )
        # if not data_in.tag:
        #     raise ValidationError(
        #         detail=[
        #             {"loc": ["body", "tag"], "msg": "Tag is required.", "type": "value_error.missing"}
        #         ]
        #     )

        # Handle file uploads
        recipe = Recipe(
            name=data_in.name,
            description=data_in.description,
            tag=data_in.tag,
            category_id=data_in.category_id,
            food_type_id=data_in.food_type_id,
            user=request.user
        )

        if video_file:
            recipe.video_data.save(video_file.name, video_file)
        if video_stream_file:
            recipe.video_stream_data.save(video_stream_file.name, video_stream_file)
        if pdf_file:
            recipe.pdf_data.save(pdf_file.name, pdf_file)
        if image_file:
            recipe.image_data.save(image_file.name, image_file)

        recipe.save()

        # Return the created recipe using RecipeSchema
        return RecipeSchema(
            id=recipe.id,
            name=recipe.name,
            slug=recipe.slug,
            description=recipe.description,
            tag=recipe.tag,
            category_id=recipe.category_id,
            food_type_id=recipe.food_type_id,
            video_data=recipe.video_data.url if recipe.video_data else None,
            video_stream_data=recipe.video_stream_data.url if recipe.video_stream_data else None,
            pdf_data=recipe.pdf_data.url if recipe.pdf_data else None,
            image_data=recipe.image_data.url if recipe.image_data else None,
            user_id=recipe.user.id,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at
        )

    # except ValidationError as ve:
    #     print(f"Validation error: {ve}")
    #     raise HttpError(422, f"Validation error: {ve}")
    
    # except Exception as e:
    #     print(f"Error creating recipe: {e}")
    #     raise HttpError(500, f"Error creating recipe: {e}")

# Update Recipe
# Import necessary modules
from typing import Optional

@recipe.put("/recipes/{recipe_slug}", response={200: RecipeSchema, 404: ErrorSchema})
# @group_required(group_name="recipe")
def update_recipe(
    request,
    recipe_slug: str,
    payload: RecipeUpdateSchema = None,
    video_file: Optional[UploadedFile] = File(None),
    video_stream_file: Optional[UploadedFile] = File(None),
    pdf_file: Optional[UploadedFile] = File(None),
    image_file: Optional[UploadedFile] = File(None)
):
    try:
        print(f"Updating recipe with slug: {recipe_slug}")

        # Attempt to retrieve the recipe object
        recipe = get_object_or_404(Recipe, slug=recipe_slug)

        # Log the retrieved recipe
        print(f"Retrieved recipe: {recipe}")

        # Update recipe fields based on payload
        if payload:
            print("Payload data:", payload.dict())
            if payload.category_id is not None:
                update_category_type = get_object_or_404(Category, id=payload.category_id)
                recipe.category = update_category_type
            if payload.food_type_id is not None:
                update_food_type = get_object_or_404(FoodType, id=payload.food_type_id)
                recipe.food_type = update_food_type
            if payload.user_id is not None:
                update_user = get_object_or_404(User, id=payload.user_id)
                recipe.user = update_user
            if payload.name:
                recipe.name = payload.name
            if payload.description:
                recipe.description = payload.description
            if payload.tag:
                recipe.tag = payload.tag

        # Handle file uploads
        if video_file:
            print(f"Uploading video file: {video_file.name}")
            recipe.video_data.save(video_file.name, video_file)
        if video_stream_file:
            print(f"Uploading video stream file: {video_stream_file.name}")
            recipe.video_stream_data.save(video_stream_file.name, video_stream_file)
        if pdf_file:
            print(f"Uploading PDF file: {pdf_file.name}")
            recipe.pdf_data.save(pdf_file.name, pdf_file)
        if image_file:
            print(f"Uploading image file: {image_file.name}")
            recipe.image_data.save(image_file.name, image_file)

        # Save updated recipe
        recipe.full_clean()  # Validate using Django model validation
        recipe.save()

        # Return updated recipe in simplified RecipeSchema format
        updated_recipe = RecipeSchema(
            id=recipe.id,
            name=recipe.name,
            slug=recipe.slug,
            description=recipe.description,
            tag=recipe.tag,
            category_id=recipe.category.id if recipe.category else None,
            food_type_id=recipe.food_type.id if recipe.food_type else None,
            video_data=recipe.video_data.url if recipe.video_data else None,
            video_stream_data=recipe.video_stream_data.url if recipe.video_stream_data else None,
            pdf_data=recipe.pdf_data.url if recipe.pdf_data else None,
            image_data=recipe.image_data.url if recipe.image_data else None,
            user_id=recipe.user.id,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at
        )
        return updated_recipe

    except HttpError as http_error:
        raise http_error
    except ValidationError as ve:
        # Build a detailed error response in the specified format
        detail = []
        for field_name, errors in ve.error_dict.items():
            for error in errors:
                detail.append({
                    "type": "validation_error",
                    "loc": ["body", field_name],
                    "msg": str(error)
                })
        return JsonResponse({"detail": detail}, status=400)
    except Exception as e:
        print(f"Error updating recipe: {e}")
        return JsonResponse({"error": "Recipe not found"}, status=404)


    
    
# @recipe.delete("/recipes/{recipe_slug}", auth=jwt_auth)
# @group_required(group_name="recipe")
# def delete_recipe(request, recipe_slug):
#     recipe = Recipe.objects.get(slug=recipe_slug)
#     recipe.delete()
#     return {"message": "Recipe deleted successfully"}






def is_valid_video_extension(file_path):
    valid_extensions = ['.mp4', '.avi', '.mkv', '.mov']  # List of allowed video extensions
    ext = os.path.splitext(file_path)[1]  # Extract file extension from the provided path
    return ext.lower() in valid_extensions

def is_valid_pdf_extension(file_path):
    valid_extensions = ['.pdf']  # List of allowed video extensions
    ext = os.path.splitext(file_path)[1]  # Extract file extension from the provided path
    return ext.lower() in valid_extensions

def is_valid_image_extension(file_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.icon']  # List of allowed video extensions
    ext = os.path.splitext(file_path)[1]  # Extract file extension from the provided path
    return ext.lower() in valid_extensions




