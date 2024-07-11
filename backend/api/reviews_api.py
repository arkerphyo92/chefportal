from django.shortcuts import get_object_or_404
from backend.models import Review, Recipe
from backend.api.reviews_schemas import ReviewsSchema, ReviewCreateSchema, ReviewUpdateSchema, ErrorSchema
from ninja import Router

review = Router(tags=["reviews"])

@review.get("/reviews", response=list[ReviewsSchema])
def list_reviews(request):
    reviews = Review.objects.all()
    return reviews

@review.get("recipes/{recipe_slug}/reviews", response={200:list[ReviewsSchema],404:ErrorSchema})
def list_reviews(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return 404, {'message': 'The slug not found'}
    try:
        reviews = Review.objects.filter(recipe=recipe)
    except Review.DoesNotExist:
        return 404, {'message' : "There is no reviews"}
     # Fetch reviews related to the specific recipe
    reviews = Review.objects.filter(recipe=recipe)
    return reviews

@review.delete("recipes/{recipe_slug}/reviews", response={200:dict, 404:ErrorSchema})
def delete_list_reviews(request, recipe_slug):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return 404, {'message': 'The slug not found'}

    reviews = Review.objects.filter(recipe=recipe)    
    if not reviews.exists():
        return 404, {'message' : "There is no reviews"}
    
     # Fetch reviews related to the specific recipe
    reviews.delete()
    return {"message": "Reviews for this recipe deleted successfully"}

@review.get("/recipes/{recipe_slug}/reviews/{id}", response={200:ReviewsSchema,404:ErrorSchema})
def get_review(request, recipe_slug, id: int):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return 404, {'message': 'The slug not found'}
    try:
        review = Review.objects.get(id=id, recipe=recipe)
    except Review.DoesNotExist:
        return 404, {'message': 'This review id not found in this recipe'}
    return review


@review.post("recipes/{recipe_slug}/reviews", response={200:ReviewsSchema,404:ErrorSchema})
def create_review(request, recipe_slug, payload: ReviewCreateSchema):
    if not isinstance(payload.reaction, bool) or not isinstance(payload.favorite, bool):
        raise ValueError('Reaction and favorite must be boolean')
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        raise ValueError("Recipe not found")
    single_review = payload.model_dump()
    review_model = Review.objects.create(recipe=recipe, **single_review)
    return review_model

# Update Recipe
@review.put("/recipes/{recipe_slug}/reviews/{id}", response={200:ReviewsSchema,404:ErrorSchema})
def update_review(request, recipe_slug, id:int, payload: ReviewUpdateSchema):
    # Retrieve the existing recipe by its slug
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return 404, {'message': 'The slug not found'}
    
    try:
        review = Review.objects.get(id=id, recipe=recipe)
    except Review.DoesNotExist:
        return 404, {'message': 'The review id not found'}
    
    if not isinstance(payload.reaction, bool) or not isinstance(payload.favorite, bool):
        raise ValueError('Reaction and favorite must be boolean')
    
    # Update the review fields based on the payload data
    review.reaction = payload.reaction  # Update the reaction
    review.favorite = payload.favorite # Update the favorite
    review.comment = payload.comment
    review.rating = payload.rating
    # Save the updated recipe back to the database
    review.save()
    # Return the updated recipe
    return review


@review.delete("/recipes/{recipe_slug}/reviews/{id}", response={200:ReviewsSchema,404:ErrorSchema})
def delete_recipe(request, recipe_slug, id:int):
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
    except Recipe.DoesNotExist:
        return 404, {'message': 'The slug not found'}
    
    try:
        review = Review.objects.get(id=id, recipe=recipe)
    except Review.DoesNotExist:
        return 404, {'message': 'The review id not found'}
    
    review.delete()
    return {"message": "Review of this recipe deleted successfully"}