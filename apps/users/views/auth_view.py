from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from ..serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from ..utils.generate_tokens import generate_tokens_response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ..models import TenantUser
from django.contrib.auth import get_user_model
from ..services.auth_services import AuthService
User = get_user_model()

# === VISTA DE IICIO DE SESIÓN ===
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success" : False,
                "message" : "Error en el inicio de sesión",
                "data": None,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = serializer.validated_data['user']
        memberships = (
            TenantUser.objects
            .filter(user=user)
            .select_related("tenant", "role")
        )
        
        if not memberships.exists():
            return Response({
                "success" : False,
                "message" : "Error en el inicio de sesión",
                "data": None,
                "errors": {"message": "El usuario no pertenece a ningun Tenant"}
            }, status=status.HTTP_403_FORBIDDEN)
            
        return AuthService.generate_tokens(
            request=request,
            user=user,
            memberships=memberships
        )        
        
# === VISTA DE CIERRE DE SESIÓN ===
@method_decorator(csrf_protect, name="dispatch")
class LogOutAPIView(APIView):    
    def post(self, request):
        refresh = request.COOKIES.get("refresh_token")
        
        if not refresh:
            response = Response({
                "success": False,
                "message": "No se econtró el token de actualización",
                "data": None,
                "errors" : {
                    "refresh_token" : "No se encontró token de actualizació en las cookies"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie("refresh_token")
            response.delete_cookie("csrftoken")
            return response
        
        try :
            token = RefreshToken(refresh)
            try:
                token.blacklist()
            except AttributeError:
                pass
        except TokenError:
            response = Response({
                "success": False,
                "message": "Token inválido o ya expirado.",
                "data": None,
                "errors": {
                    "refresh_token": "El token no es válido o ya expiró."
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie("refresh_token")
            response.delete_cookie("csrftoken")
            return response
        
        response = Response({
            "success": True,
            "message": "Cierre de sesión exitoso.",
            "data": None,
            "errors": None
        }, status=status.HTTP_200_OK)
        
        response.delete_cookie("refresh_token")
        response.delete_cookie("csrftoken")
        
        return response
    
@method_decorator(csrf_protect, name="dispatch")
class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        
        try:
            if not refresh_token:
                raise AuthenticationFailed("No se encontró el token de actualización.")

            token = RefreshToken(refresh_token)            
            user_id = token.get("user_id")
            user = User.objects.filter(id=user_id, is_active=True).first()
            
            if not user:
                raise AuthenticationFailed("Usuario no válido o inactivo.")

            # sub = user.membership.organization.subscriptions.filter(status='active').exists()
            # if not sub: raise AuthenticationFailed("Suscripción de empresa vencida.")
            tenant_slug = token.get("tenant_slug")
            tenant_user = TenantUser.objects.filter(user=user, tenant__slug=tenant_slug)
            return AuthService.generate_tokens(
                request=request,
                user=user,
                memberships=tenant_user,
                message="Sesión renovada."
            )

        except (TokenError, AuthenticationFailed) as e:
            response = Response({
                "success": False,
                "message": str(e),
                "errors": {"auth": "Sesión expirada o inválida"}
            }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Limpieza centralizada
            response.delete_cookie("refresh_token")
            response.delete_cookie("csrftoken")
            return response