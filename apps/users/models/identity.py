from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from apps.core.models import (
    TimesTampTime,
    BaseState
)
from simple_history.models import HistoricalRecords
from apps.core.choices import (
    TypeDocument, 
) 

# === MANAGER DE USUARIO ===
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("El usuario debe de tener un correo electronico")
        
        if not password:
            raise ValueError("El usuario debe de tener una contraseña")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": email})
    
    def create_user(self, email, password, **extra_fields): 
        extra_fields["is_superuser"] = False  
        extra_fields.setdefault("is_staff", False)
                      
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_superuser"] = True        
        extra_fields["is_staff"] = True        

        return self._create_user(email, password, **extra_fields)
 
# === MODELO USUARIO ===
class User(AbstractBaseUser, PermissionsMixin, BaseState, TimesTampTime):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    document_type = models.CharField(max_length=2, choices=TypeDocument.choices, default=TypeDocument.CC)
    document_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "lastname"]
    
    history = HistoricalRecords()
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "user"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        