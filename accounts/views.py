from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from tickets.permissions import IsAdminRole

User = get_user_model()

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
