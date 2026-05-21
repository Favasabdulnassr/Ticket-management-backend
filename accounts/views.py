from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from .serializers import RegisterSerializer, UserSerializer
from tickets.permissions import IsAdminRole

User = get_user_model()


# ── Cookie helpers ────────────────────────────────────────────────
def _set_auth_cookies(response, access, refresh):
    """Attach access & refresh tokens as HttpOnly cookies."""
    response.set_cookie(
        key='access_token',
        value=str(access),
        httponly=True,
        secure=not settings.DEBUG,       # True in production (HTTPS)
        samesite='Lax',
        max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Lax',
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        path='/',
    )


def _clear_auth_cookies(response):
    """Remove auth cookies."""
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')


# ── Auth views ────────────────────────────────────────────────────
class CookieLoginView(APIView):
    """
    POST /api/v1/auth/login/
    Validates credentials, returns user data, sets JWT cookies.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'detail': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        tokens = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        response = Response({'user': user_data}, status=status.HTTP_200_OK)
        _set_auth_cookies(response, tokens.access_token, tokens)
        return response


class CookieRefreshView(APIView):
    """
    POST /api/v1/auth/refresh/
    Reads refresh_token from cookie, issues a new access token cookie.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        raw_refresh = request.COOKIES.get('refresh_token')
        if not raw_refresh:
            return Response(
                {'detail': 'Refresh token not found.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(raw_refresh)
            new_access = refresh.access_token
        except (TokenError, InvalidToken):
            response = Response(
                {'detail': 'Refresh token is invalid or expired.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            _clear_auth_cookies(response)
            return response

        response = Response({'detail': 'Token refreshed.'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=str(new_access),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            path='/',
        )
        return response


class CookieLogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklists the refresh token and clears cookies.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        raw_refresh = request.COOKIES.get('refresh_token')
        if raw_refresh:
            try:
                token = RefreshToken(raw_refresh)
                token.blacklist()
            except (TokenError, InvalidToken, AttributeError):
                pass  # Token already blacklisted or blacklist not enabled

        response = Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)
        _clear_auth_cookies(response)
        return response


# ── Existing views ────────────────────────────────────────────────
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """Admin-only: list all users for the assign ticket dropdown."""
    serializer_class = UserSerializer
    permission_classes = (IsAdminRole,)

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('username')
