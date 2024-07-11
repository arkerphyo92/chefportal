from ninja import Router
from django.db.models import Q, Avg
from ..models import Recipe
from .search_schemas import RecipeSearchSchema, RecipeResponseSchema, ErrorSchema

search = Router(tags=["search"])

@search.get("/search", response={200: list[RecipeResponseSchema], 404: ErrorSchema})
def filter_recipes(request, filters: RecipeSearchSchema):
    recipes = Recipe.objects.all()

    if filters.search_query:
        recipes = recipes.filter(Q(name__icontains=filters.search_query) | Q(description__icontains=filters.search_query))

    if filters.category_id:
        recipes = recipes.filter(category_id=filters.category_id)

    if filters.food_type_id:
        recipes = recipes.filter(food_type_id=filters.food_type_id)

    # if filters.min_rating:
    #     recipes = recipes.filter(reviews__rating__gte=filters.min_rating)

    # recipes = recipes.annotate(avg_rating=Avg('reviews__rating'))

    if not recipes:
        return 404, {"message": "No recipes found."}

    # Convert QuerySet to list of RecipeResponseSchema instances
    response_data = []
    for recipe in recipes:
        response_data.append(RecipeResponseSchema(
            id=recipe.id,
            name=recipe.name,
            slug=recipe.slug,
            description=recipe.description,
            tag=recipe.tag,
            # avg_rating=recipe.avg_rating,
            category=recipe.category.name if recipe.category else None,
            food_type=recipe.food_type.name if recipe.food_type else None,
            video_path=recipe.video_path.url if recipe.video_path else None,
            video_stream_path=recipe.video_stream_path.url if recipe.video_stream_path else None,
            pdf_path=recipe.pdf_path.url if recipe.pdf_path else None,
            image_path=recipe.image_path.url if recipe.image_path else None,
            user_id=recipe.user_id,
            created_at=recipe.created_at,
            updated_at=recipe.updated_at,
        ))

    return 200, response_data
