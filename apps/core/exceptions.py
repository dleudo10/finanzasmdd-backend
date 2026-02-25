from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:

        if isinstance(exc, ValidationError):
            message = "Error en la validación de los datos"

        elif isinstance(exc, NotAuthenticated):
            message = "No autorizado o sesión expirada"

        elif isinstance(exc, PermissionDenied):
            message = "No tienes permisos para realizar esta acción"

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            message = "Recurso no encontrado"

        elif 500 <= response.status_code < 600:
            message = "Error interno del servidor"

        else:
            message = response.data.get("detail", "Ha ocurrido un error")

        return Response({
            "success": False,
            "message": message,
            "data": None,
            "errors": response.data
        }, status=response.status_code)

    # Error no manejado por DRF
    return Response({
        "success": False,
        "message": "Error inesperado",
        "data": None,
        "errors": None
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)