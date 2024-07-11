from django.contrib import admin

from .models import Profile, Recipe, Category, Ingredient, Instruction, Review, FoodType

# Register your models here.
admin.site.register(Profile)
admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(Review)
admin.site.register(FoodType)
