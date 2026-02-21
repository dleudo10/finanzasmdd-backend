from django.urls import path, include
from .views import (
    LoginAPIView,  
    SelectTenantAPIView,
    LogOutAPIView, 
    RefreshTokenAPIView, 
    ProfileAPIView, 
    ChangePasswordAPIView,
    TenantAPIView,
    RoleViewSet,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/select-tenant/", SelectTenantAPIView.as_view(), name="select_tenant"),
    path("auth/logout/", LogOutAPIView.as_view(), name="logout"),
    path("auth/tokens/refresh/", RefreshTokenAPIView.as_view(), name="refresh_token"),
    path("profile/me/", ProfileAPIView.as_view(), name="me"),
    path("profile/change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("tenant/", TenantAPIView.as_view(), name="tenant"),
    path("", include(router.urls)),
]