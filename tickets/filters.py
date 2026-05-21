import django_filters
from .models import Ticket

class TicketFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')

    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'created_at']
