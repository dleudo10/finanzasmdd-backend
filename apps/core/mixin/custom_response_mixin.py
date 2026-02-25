from rest_framework.response import Response


class ResponseWrapperMixin:

    success_messages = {
        "list": "Datos obtenidos exitosamente.",
        "retrieve": "Registro obtenido exitosamente.",
        "create": "Registro creado exitosamente.",
        "update": "Registro actualizado exitosamente.",
        "partial_update": "Registro actualizado exitosamente.",
        "destroy": "Registro eliminado exitosamente.",
        "change_state": "Estado actualizado correctamente.",
    }

    def finalize_response(self, request, response, *args, **kwargs):

        if response.exception:
            response.data = {
                "success": False,
                "message": "Ocurrió un error en la solicitud.",
                "data": None,
                "errors": response.data
            }
            return super().finalize_response(request, response, *args, **kwargs)

        if isinstance(response.data, dict):
            message = self.success_messages.get(
                getattr(self, "action", ""),
                "Operación realizada correctamente."
            )

            response.data = {
                "success": True,
                "message": message,
                "data": response.data,
                "errors": None
            }

        return super().finalize_response(request, response, *args, **kwargs)