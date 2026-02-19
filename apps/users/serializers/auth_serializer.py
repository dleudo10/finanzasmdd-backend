from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            
            if not user:
                raise serializers.ValidationError("Usuario o contraseña incorrectos")
            if user.is_superuser == True:
                raise serializers.ValidationError("Usuario o contraseña incorrectos")
            elif not user.is_active:
                raise serializers.ValidationError("Tu cuenta está inactiva. Contacta al administrador")
        else:
            raise serializers.ValidationError("Falta de credenciales")

        attrs['user'] = user
        return attrs