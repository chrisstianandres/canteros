from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Insumo


class InsumoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del insumo', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion', 'class': 'form-control form-rounded'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = Insumo
        fields = ['nombre',
                  'descripcion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
        }
