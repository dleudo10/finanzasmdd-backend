from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import TenantUser

class AuthMultiTenantJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if not user_auth_tuple:
            return None

        user, validated_token = user_auth_tuple

        tenant_slug = validated_token.get("tenant_slug")

        tenant_user = TenantUser.objects.filter(
            user=user,
            tenant__slug=tenant_slug
        ).select_related("tenant").first()

        if not tenant_user:
            raise AuthenticationFailed("Tenant inválido")

        request.tenant_user = tenant_user
        request.tenant = tenant_user.tenant

        return (user, validated_token)