from rest_framework import serializers
from .models import (
    Customer,
    Service,
    Inventory,
    Appointment
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'vehicle_info']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'base_fee']
        
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'name', 'price']
        
class AppointmentCreateSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    items_used = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all(), many=True)
    
    class Meta:
        model = Appointment
        fields = ['customer', 'services', 'items_used', 'date_time']
        
    def create(self, validated_data):
        services = validated_data.pop('services')
        items_used = validated_data.pop('items_used')
        
        # Create the appointment
        appointment = Appointment.objects.create(**validated_data)
        
        # Add services to the appointment
        appointment.services.set(services)
        
        # Add inventory items to the appointment
        appointment.items_used.set(items_used)
        
        # Calculate the total cost (assuming each service has a cost and each inventory item has a price)
        total_cost = sum([service.base_fee for service in services]) + sum([item.price for item in items_used])
        appointment.total_cost = total_cost
        appointment.save()
        
        return appointment
        
class AppointmentSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    items_used = InventorySerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'services', 'items_used', 'date_time', 'total_cost']
        
    def get_total_cost(self, obj):
        return obj.total_cost