from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True)
    skills = models.IntegerField(blank=True, null=True)
    favorite_cuisine = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.bio

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class FoodType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


def validate_video_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.avi', '.mkv', '.mov']  # Add more extensions if needed
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Only MP4, AVI, MKV, and MOV formats are allowed.'))

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    description = models.TextField()
    tag = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    food_type = models.ForeignKey(FoodType, on_delete=models.SET_NULL, null=True)
    video_data = models.FileField(upload_to='videos/', blank=True)  # New field for video
    video_stream_data = models.FileField(upload_to='videos/stream/', blank=True)  # New field for video stream
    pdf_data = models.FileField(upload_to='pdf/', blank=True)  # New field for PDF
    image_data = models.FileField(upload_to='images/', blank=True)  # New field for image
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.FloatField()
    notes = models.TextField(blank=True)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredients')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Instruction(models.Model):
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='instructions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.description

class Review(models.Model):
    reaction = models.BooleanField()
    favorite = models.BooleanField()
    comment = models.TextField(blank=True)
    rating = models.PositiveIntegerField()
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment