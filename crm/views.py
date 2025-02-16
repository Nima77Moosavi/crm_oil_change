from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Customer, 
    Service,
    Inventory,
    Appointment
)
from .serializers import (
    ServiceSerializer,
    InventorySerializer,
    AppointmentCreateSerializer,
    AppointmentSerializer,
)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    @action(detail=True, methods=['get'])
    def total_cost(self, request, pk=None):
        appointment = self.get_object()
        return Response({'total_cost': appointment.total_cost})
