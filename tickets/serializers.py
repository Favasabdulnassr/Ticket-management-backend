from rest_framework import serializers
from .models import Ticket

class TicketListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'priority', 'status', 'created_by', 'created_by_name', 'assigned_to', 'assigned_to_name', 'created_at')

class TicketDetailSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class TicketCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority')
        
    def validate_priority(self, value):
        valid_priorities = dict(Ticket.PRIORITY_CHOICES).keys()
        if value not in valid_priorities:
            raise serializers.ValidationError("Invalid priority level.")
        return value

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'status', 'assigned_to', 'resolution_comment')
        
    def validate_priority(self, value):
        valid_priorities = dict(Ticket.PRIORITY_CHOICES).keys()
        if value not in valid_priorities:
            raise serializers.ValidationError("Invalid priority level.")
        return value

    def validate_status(self, value):
        valid_statuses = dict(Ticket.STATUS_CHOICES).keys()
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status.")
        return value
        
    def validate_resolution_comment(self, value):
        request = self.context.get('request')
        if request and request.user.role != 'ADMIN' and value:
            raise serializers.ValidationError("Only admins can add or edit resolution comments.")
        return value

class TicketResolveSerializer(serializers.ModelSerializer):
    resolution_comment = serializers.CharField(required=True)
    
    class Meta:
        model = Ticket
        fields = ('resolution_comment',)

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user.role != 'ADMIN':
            raise serializers.ValidationError("Only admins can resolve tickets and add resolution comments.")
        return attrs
