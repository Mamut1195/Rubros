from django import forms
from .models import  Equipo


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'

    class Media:
        js = ('js/alquiler_condicional.js',)  # Archivo JavaScript personalizado
