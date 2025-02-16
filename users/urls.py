from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SignupViewSet, LoginViewSet

router = DefaultRouter()
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = router.urls