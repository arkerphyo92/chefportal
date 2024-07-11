# urls.py

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from backend.api.recipes_api import recipe
from backend.api.reviews_api import review
from backend.api.search_api import search
from backend.api.auth_api import auth_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

api = NinjaAPI()

# Include the routers from each module
api.add_router('', recipe)
api.add_router('', review)
api.add_router('', search)
api.add_router('auth', auth_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
