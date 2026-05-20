from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, CurrentUserView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('me/', CurrentUserView.as_view(), name='me'),
]
