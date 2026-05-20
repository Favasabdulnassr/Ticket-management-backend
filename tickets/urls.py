from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketCreateView, UserTicketListView, UserTicketDetailView, AdminTicketViewSet

app_name = 'tickets'

router = DefaultRouter()
router.register(r'admin/tickets', AdminTicketViewSet, basename='admin-tickets')

urlpatterns = [
    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/my/', UserTicketListView.as_view(), name='ticket-list-my'),
    path('tickets/<int:pk>/', UserTicketDetailView.as_view(), name='ticket-detail'),
    path('', include(router.urls)),
]
