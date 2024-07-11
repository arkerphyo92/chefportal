from rest_framework_simplejwt.authentication import JWTAuthentication
from ninja.security import HttpBearer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class JWTAuthBearer(HttpBearer):
    def authenticate(self, request, token):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
            request.user = user  # Attach the user to the request for later use
            return user
        except (InvalidToken, TokenError):
            return None