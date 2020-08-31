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
                attrs={'placeholder': 'Ingrese el nombre del Periodo', 'class': 'form-control'})
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
            'hasta': forms.SelectDateWidget(attrs={'class': 'select2', 'data-width': 'fit'})
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(PeriodoForm, self).clean()
        periodo_inicio = cleaned_data.get('desde', None)
        periodo_fin = cleaned_data.get('hasta', None)
        # if periodo_fin < periodo_inicio:
        #     self.add_error('hasta', 'la fecha final no puede ser menor a la incial')
        if periodo_inicio is not None:
            pi = periodo_inicio.year
            ye = Periodo.objects.raw('SELECT COUNT(*)as id from periodo where EXTRACT(YEAR FROM desde) = %(pi)s',
                                     {'pi': pi})
            for y in ye:
                if y.id > 0:
                    self.add_error('desde', 'Periodo ya existente con este rango de fechas')
                else:
                    if periodo_fin <= periodo_inicio:
                        self.add_error('hasta', 'No puede ingresar el final mayor que el inicio')
