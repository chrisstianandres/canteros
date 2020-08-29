from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Periodo


class PeriodoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        yearsd = range(this_year, this_year + 1)
        yearsh = range(this_year, this_year + 2)
        for field in self.Meta.fields:
            # self.fields[field].widget.attrs.update({
            #     'class': 'form-control'
            # })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del Periodo', 'class': 'form-control form-rounded'})
            self.fields['desde'].widget = SelectDateWidget(years=yearsd, attrs={
                'class': 'form-control', 'data-width': '30%', 'container': 'body'})
            self.fields['hasta'].widget = SelectDateWidget(years=yearsh, attrs={
                'class': 'form-control', 'data-width': '30%', 'container': 'body'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Periodo
        fields = ['nombre',
                  'desde',
                  'hasta'
                  ]
        labels = {
            'nombre': 'Nombre',
            'desde': 'Inicio',
            'hasta': 'Fin'

        }
        widgets = {
            'nombre': forms.TextInput(),
            'desde': forms.SelectDateWidget(),
            'hasta': forms.SelectDateWidget(attrs={'class': 'selectpicker', 'data-width': 'fit'})
        }
