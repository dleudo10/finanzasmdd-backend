from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.conf import settings
from django.middleware.csrf import get_token

class AuthService:
    
    @staticmethod
    def generate_tokens(*,
                        request,
                        user,
                        memberships,
                        message = "Login exitoso",
    ):
        
        claims = {
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
        }
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        if memberships.count() > 1:
            return Response({
                "success": True,
                "message": "Selecciona un tenant",
                "data": {
                    "requires_tenant_selection": True,
                    "access": str(access),
                    "tenants": [
                        {
                            "slug": m.tenant.slug,
                            "name": m.tenant.name
                        } for m in memberships
                    ]
                },
                "errors": None
            })
        
        memberships = memberships.first()
        claims["tenant_slug"] = memberships.tenant.slug
        claims["tenant"] = memberships.tenant.trade_name
        claims["role"] = memberships.role.name
        
        for key, value in claims.items():
            refresh[key] = value
            access[key] = value
            
        refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
        access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        
        response = Response({
            "success": True,
            "message": message,
            "data": {
                "requires_tenant_selection": False,
                "access": str(access),
                "access_expires_in" : access_max_age,
            },
            "errors": None
        })
        
        response["Cache-Control"] = "no-store"
        response["Pragma"] = "no-cache"
        
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False, # True en produccionn (https)
            samesite="lax", 
            max_age=refresh_max_age, 
        )
        
        csrftoken = get_token(request)
        response.set_cookie(
            key="csrftoken",
            value=str(csrftoken),
            httponly=False, 
            secure=False,
            samesite="lax", 
        )

        return response