from rest_framework.views import APIView
from ..serializers import TenantSerializer
from rest_framework.response import Response
from rest_framework import status
from permissions import IsTenantOwner

class TenantAPIView(APIView):
    permission_classes = [IsTenantOwner]
    
    def get(self, request):
        serializer = TenantSerializer(request.tenant)
        return Response({
            "success": True,
            "message" : "Perfil de usuario obtenido correctamente",
            "data" : serializer.data,
            "errors" : None
        }, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = TenantSerializer(
            request.tenant,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            tenant_update = serializer.save()
            
            return Response({
                "success" : True,
                "message" : "Tenant editado correctamente",
                "data" : TenantSerializer(tenant_update).data,
                "errors" : None
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success" : False,
            "message" : "Error al editar el Tenant",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)