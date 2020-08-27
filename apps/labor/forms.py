from datetime import *

from django import forms
from django.forms import TextInput

from .models import Labor


class LaborForm(forms.ModelForm):
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
            self.fields['valor_dia'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm',
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Labor
        fields = ['nombre',
                  'descripcion',
                  'valor_dia'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'valor_dia': 'Varlor por día de trabajo',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
            'valor_dia': forms.TextInput()
        }
