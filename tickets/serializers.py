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
        
    def validate_assigned_to(self, value):
        # Allow null (unassigned)
        if not value:
            return None
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # If DRF already converted to a User instance, use it directly
        if isinstance(value, User):
            assigned_user = value
        else:
            try:
                assigned_user = User.objects.get(pk=value)
            except User.DoesNotExist:
                raise serializers.ValidationError("Assigned user does not exist.")
        if assigned_user.role != 'ADMIN' and not assigned_user.is_staff and not assigned_user.is_superuser:
            raise serializers.ValidationError("Only admin users can be assigned to tickets.")
        return assigned_user

    def validate(self, attrs):
        request = self.context.get('request')
        if request and 'resolution_comment' in attrs:
            user = request.user
            if user.role != 'ADMIN' and not user.is_staff and not user.is_superuser:
                raise serializers.ValidationError({"resolution_comment": "Only admins can add or edit resolution comments."})
        return attrs

class TicketResolveSerializer(serializers.ModelSerializer):
    resolution_comment = serializers.CharField(required=True)
    
    class Meta:
        model = Ticket
        fields = ('resolution_comment',)

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.role != 'ADMIN' and not user.is_staff and not user.is_superuser:
                raise serializers.ValidationError("Only admins can resolve tickets and add resolution comments.")
        
        if not attrs.get('resolution_comment', '').strip():
            raise serializers.ValidationError({
                "resolution_comment": "Resolution comment is required when resolving a ticket."
            })
            
        return attrs
