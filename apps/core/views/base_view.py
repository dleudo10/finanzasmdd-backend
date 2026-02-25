from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from apps.core.mixin import ResponseWrapperMixin
from ..pagination import CustomPagination

class BaseViewSet(
    ResponseWrapperMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    filterset_fields = []
    ordering_fields = ["created_at", "id"]
    ordering = ["-created_at", "-id"]
    pagination_class = CustomPagination
    serializer_action_classes = {}
    permission_action_classes = {}
    
    # -------------------------
    # SERIALIZER POR ACCIÓN
    # -------------------------
    def get_serializer_class(self):
        if hasattr(self, "action"):
            return self.serializer_action_classes.get(
                self.action,
                super().get_serializer_class()
            )
        return super().get_serializer_class()
    
    # -------------------------
    # PERMISOS POR ACCIÓN
    # -------------------------
    def get_permissions(self):
        if hasattr(self, "action"):
            perms = self.permission_action_classes.get(self.action)
            if perms:
                return [p() for p in perms]
        return super().get_permissions()
    
    # -------------------------
    # HOOK RUNNER
    # -------------------------
    def run_hook(self, hook_name, *args):
        method = getattr(self, hook_name, None)
        if callable(method):
            method(*args)
            
    # -------------------------
    # OVERRIDES LIMPIOS
    # -------------------------
    def perform_create(self, serializer):
        self.run_hook("pre_create", serializer)
        serializer.save()
        self.run_hook("post_create", serializer)

    def perform_update(self, serializer):
        self.run_hook("pre_update", serializer)
        serializer.save()
        self.run_hook("post_update", serializer)

    def perform_destroy(self, instance):
        self.run_hook("pre_destroy", instance)
        instance.delete()
        self.run_hook("post_destroy", instance)