from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model CRUD operations.

    Attributes:
        requester_name: Username of the ticket requester (read-only).
        assigned_to_name: Username of the assigned user (read-only).
        requester: User PK used when creating a ticket (write-only).
        assigned_to: User PK for assignment; accepts null (write-only).
    """
    requester_name = serializers.CharField(source='requester.username', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    requester = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False, write_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'requester', 'requester_name', 'assigned_to', 'assigned_to_name',
                  'created_at', 'updated_at']