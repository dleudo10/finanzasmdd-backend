import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "La contraseña debe contener al menos 8 caracteres.",
                code="password_too_short",
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "La contraseña debe contener al menos una letra mayúscula.",
                code="password_no_upper",
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "La contraseña debe contener al menos una letra minúscula.",
                code="password_no_lower",
            )

        if not re.search(r"\d", password):
            raise ValidationError(
                "La contraseña debe contener al menos un número.",
                code="password_no_number",
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                "La contraseña debe contener al menos un carácter especial (!@#$%^&*).",
                code="password_no_symbol",
            )

    def get_help_text(self):
        return (
            "La contraseña debe contener al menos 8 caracteres e incluir: "
            "una letra mayúscula, una letra minúscula, un número y un carácter especial."
        )