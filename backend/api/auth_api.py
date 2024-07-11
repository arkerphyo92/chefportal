# auth_api.py

from ninja import Router
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

auth_router = Router(tags=["auth"])

@csrf_exempt
@auth_router.post("/auth-check")
def auth_check(request):
    try:
        # Extract username and password from the request body
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

        # Retrieve the groups the user belongs to
        groups = user.groups.values_list('name', flat=True)
        
        return JsonResponse({"message": "Authenticated successfully", "groups": list(groups)}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
