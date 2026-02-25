from .base_view import BaseViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class BaseStateViewSet(BaseViewSet):
    """ ViewSet base para modelos que heredan de BaseState """

    @action(detail=True, methods=['patch'])
    @transaction.atomic
    def change_state(self, request, pk=None):
        instance = self.get_object()
        
        self.run_hook("pre_change_state", instance)
        
        instance.change_status()
        
        self.run_hook("post_change_status", instance)
        
        return Response(
            {"id": instance.pk, "is_active" : instance.is_active},
            status=status.HTTP_200_OK
        )
        