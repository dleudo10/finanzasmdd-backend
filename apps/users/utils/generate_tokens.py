from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.middleware.csrf import get_token


def generate_tokens_response(request, user, memberships, message="Login exitoso"):
    """
    Generación de access y refresh token, seteando refresh en cookie HttpOnly
    """
    
    claims = {
        "email": user.email,
        "is_staff": user.is_staff,
        "name": user.name,
        "lastname": user.lastname,
    }
                
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
        
    for key, value in claims.items():
        refresh[key] = value
        access[key] = value
            
    refresh_max_age = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
    access_max_age = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    
    if memberships.count() == 1:
        tenant = memberships.first().tenant
        
        response = Response({
            "success": True,
            "message" : message,
            "data" : {
                "access": str(access),
                "access_expires_in" : access_max_age,
                "tenant_slug": str(tenant.slug)
            },
            "errors": None
        })
        
    # === Seguridad en headers ===
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
    
