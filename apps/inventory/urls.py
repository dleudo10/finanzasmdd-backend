from django.urls import path, include
from .views import (
    CategoryViewSet, 
    ListPriceViewSet,
    WarehouseViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'list-price', ListPriceViewSet, basename='list_price')
router.register(r'warehouse', WarehouseViewSet, basename='warehouse')

urlpatterns = [
    path("", include(router.urls)),
]