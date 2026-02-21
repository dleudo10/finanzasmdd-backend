from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsOwner
from ..serializers import ProfileSerializer, ChangePasswordSerializer
from rest_framework import status

# === VISTA DE PERFIL DE USUARIO ===
class ProfileAPIView(APIView):
    permission_classes = [IsOwner]
    
    def get(self, request):
        serializer = ProfileSerializer(request.user, context={'request': request})
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
            context={'request': request}
        )
        
        if serializer.is_valid():
            user_update = serializer.save()

            return Response({
                "success" : True,
                "message" : "Perfil editado correctamente",
                "data": ProfileSerializer(user_update, context={'request': request}).data,
                "errors": None
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success" : False,
            "message" : "Error al editar el perfil",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
       
# === VISTA DE CAMBIO DE CONTRASEÑA === 
class ChangePasswordAPIView(APIView):
    permission_classes = [IsOwner]
    
    def patch(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        ) 
        
        if serializer.is_valid():
            serializer.save()

            return Response({
                "success" : True,
                "message" : "Cambio de contraseña exitoso",
                "data": None,
                "errors": None
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success" : False,
            "message" : "Error al cambiar la contraseña",
            "data": None,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        