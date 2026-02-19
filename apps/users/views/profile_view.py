from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsOwner
from ..serializers import ProfileSerializer
from rest_framework import status
from apps.core.permission.tenant_required import TenantRequired

class ProfileAPIView(APIView):
    permission_classes = [IsOwner, TenantRequired]
    
    def get(self, request):
        serializer = ProfileSerializer(request.user, context={'tenant': request.tenant})
        return Response({
            "success": True,
            "message" : "Perfil de usuario obtenido correctamente",
            "data" : serializer.data,
            "errors" : None
        }, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = ProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True,
            context={'tenant': request.tenant}
        )
        
        if serializer.is_valid():
            user_update = serializer.save()

            return Response({
                "success" : True,
                "message" : "Perfil editado correctamente",
                "data": ProfileSerializer(user_update, context={'tenant': request.tenant}).data,
                "errors": None
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success" : False,
            "message" : "Error al editar el perfil",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)