from django.urls import path, include
from .views import CategoryViewSet, ListPriceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'list-price', ListPriceViewSet, basename='list_price')

urlpatterns = [
    path("", include(router.urls)),
]