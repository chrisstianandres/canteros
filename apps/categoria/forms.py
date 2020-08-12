from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del cantero', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una Descripcion', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Categoria
        fields = ['nombre',
                  'descripcion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput()
        }
