from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Cantero


class CanteroForm(forms.ModelForm):
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
                attrs={'placeholder': 'Ingrese el nombre del cantero', 'class': 'form-control'})
            self.fields['valor_dim'].widget = TextInput(
                attrs={'value': 1, 'class': 'form-control'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = Cantero
        fields = ['nombre',
                  'dimesion',
                  'valor_dim'
                  ]
        labels = {
            'nombre': 'Nombre',
            'dimesion': 'Tipo de Medida',
            'valor_dim': 'Dimension'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'dimesion': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'valor_dim': forms.TextInput()
        }
