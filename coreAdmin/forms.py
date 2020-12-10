from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from coreAdmin.models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [ "usuario", "tipoIdentificacion", "identificacion", "telefono", "pais", "provincia", "canton", "distrito", "barrio", "direccion" ]

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ya esta utilizado")
        return email