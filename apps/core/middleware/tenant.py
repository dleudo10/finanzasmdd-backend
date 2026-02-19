from apps.users.models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        
        if not request.user.is_authenticated:
            return self.get_response(request)

        auth = getattr(request, "auth", None)
        if not auth:
            return self.get_response(request)
            
        tenant_slug = auth.get("tenant_slug")
        if not tenant_slug:
            return self.get_response(request)

        request.tenant = Tenant.objects.filter(
            slug=tenant_slug,
            is_active=True
        ).first()

        return self.get_response(request)
