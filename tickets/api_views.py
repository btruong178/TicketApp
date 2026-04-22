from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tickets.models import Ticket
from tickets.serializers import TicketSerializer

class TicketModelViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]