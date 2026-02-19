from django import forms
from apps.core.choices import TypeDocument, TypePerson, SubscriptionStatus
from ...models import Tenant, Plan
from django.contrib.auth import get_user_model
User = get_user_model()

class TenantForm(forms.ModelForm):
    email = forms.EmailField(label="Correo")
    name = forms.CharField(label="Nombre del propietario")
    lastname = forms.CharField(label="Apellido del propietario")
    owner_password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    plan = forms.ModelChoiceField(queryset=Plan.objects.all())
    plan_status = forms.ChoiceField(label="Estado de la suscripción", choices=SubscriptionStatus.choices)
    observations = forms.Textarea()

    class Meta:
        model = Tenant
        fields = ["email", "name", "lastname", "trade_name", "type_person", "document_type", "document_number", "phone",]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con ese email")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        owner_password = cleaned_data.get('owner_password')
        confirm_password = cleaned_data.get('confirm_password')
        type_person = cleaned_data.get('type_person')
        document_type = cleaned_data.get('document_type')
        
        
        # validar tipo de persona con typo de documento
        if type_person == TypePerson.LEGAL and document_type != TypeDocument.NIT:
            raise forms.ValidationError('Para las personas juridicos el tipo de documento debe de ser NIT')
        
        if type_person == TypePerson.NATURAL and document_type == TypeDocument.NIT:
            raise forms.ValidationError('Para las personas naturales el tipo de documento debe de ser diferente de NIT')    
        
        # Validar contraseñas
        if owner_password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')
