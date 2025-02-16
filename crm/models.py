from django.db import models
from users.models import CustomUser

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')
    vehicle_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.phone_number

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Labor cost for the service

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='appointments')
    services = models.ManyToManyField(Service, related_name='appointments')  # Services provided in the appointment
    items_used = models.ManyToManyField(Inventory, related_name='appointments')  # Products used in the appointment
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.customer.user.phone_number} - {self.date_time}"

    @property
    def total_cost(self):
        """
        Calculate the total cost of the appointment, including the base fees of all services and the cost of items used.
        """
        services_cost = sum(service.base_fee for service in self.services.all())
        items_cost = sum(item.price for item in self.items_used.all())
        return services_cost + items_cost
    