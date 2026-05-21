from django.urls import path
from .views import (
    RegisterView, CurrentUserView, UserListView,
    CookieLoginView, CookieRefreshView, CookieLogoutView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieLoginView.as_view(), name='login'),
    path('refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('logout/', CookieLogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('users/', UserListView.as_view(), name='user-list'),
]
