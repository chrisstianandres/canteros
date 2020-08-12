from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput, Select

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
                attrs={'placeholder': 'Ingrese el nombre del insumo', 'class': 'form-control', 'autofocus': True})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion', 'class': 'form-control form-rounded'})
            self.fields['categoria'].widget.attrs = {
                'class': 'form-control selectpicker',
                'data-live-search': 'true'
            }

        # habilitar, desabilitar, y mas

    class Meta:
        model = Insumo
        fields = ['nombre',
                  'categoria',
                  'descripcion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'categoria': 'Categoria',
            'descripcion': 'Descripcion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'categoria': forms.Select(),
            'descripcion': forms.TextInput(),
        }
