from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, InventoryViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')
router.register(r'inventories', InventoryViewSet, basename='inventories')
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = router.urls
