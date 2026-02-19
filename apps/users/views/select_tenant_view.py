from rest_framework.views import APIView
from ..models import TenantUser
from rest_framework.response import Response
from rest_framework import status
from ..services.auth_services import AuthService

class SelectTenantAPIView(APIView):
    
    def post(self, request):
        tenant_slug = request.data.get("tenant_slug")
        
        membership = (
            TenantUser.objects
            .filter(
                user=request.user,
                tenant__slug=tenant_slug,
                tenant__is_active=True
            )
            .select_related("tenant")
            .first()
        )
        
        if not membership:
            return Response({
                "success": False,
                "message": "Acceso denegado",
                "data": None,
                "errors": [{"message": "No pertenece a este tenant"}]  
            }, status=status.HTTP_403_FORBIDDEN)
            
        return AuthService.generate_tokens(
            request=request,
            user=request.user,
            memberships=[membership]
        )