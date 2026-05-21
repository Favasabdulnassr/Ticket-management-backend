"""
Custom JWT authentication that reads tokens from HttpOnly cookies
instead of the Authorization header.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Extends SimpleJWT's default authentication to look for the
    access token in an HttpOnly cookie named 'access_token'.
    Falls back to the standard Authorization header if the cookie
    is not present (keeps Swagger / Postman working).
    """

    def authenticate(self, request):
        # 1. Try the cookie first
        raw_token = request.COOKIES.get('access_token')
        if raw_token:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        # 2. Fallback to Authorization header (useful for Swagger)
        return super().authenticate(request)
