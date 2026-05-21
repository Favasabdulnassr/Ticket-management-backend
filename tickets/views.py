from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, viewsets,mixins,filters, status

class TicketPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import (
    TicketCreateSerializer, TicketListSerializer, TicketDetailSerializer,
    TicketUpdateSerializer, TicketResolveSerializer
)
from .permissions import IsTicketOwner, IsAdminRole

class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserTicketListView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description']

    def get_queryset(self):
        # Users can only view their own tickets
        return Ticket.objects.filter(created_by=self.request.user)

class UserTicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = [IsAuthenticated, IsTicketOwner]
    
    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)

class AdminTicketViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Ticket.objects.all()
    pagination_class = TicketPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'created_by__username', 'assigned_to__username']

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'resolve':
            return TicketResolveSerializer
        return TicketUpdateSerializer

    @action(detail=True, methods=['patch'])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status='RESOLVED')
        return Response(serializer.data, status=status.HTTP_200_OK)
