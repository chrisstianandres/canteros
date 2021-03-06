from django import forms
from datetime import *
from .models import Asig_labor
from tempus_dominus.widgets import DatePicker

from ..labor.models import Labor
from ..trabajador.models import Trabajador
from ..periodo.models import Periodo

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


class Asig_LaborForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_asig'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['periodo'].widget.attrs = {
                'class': 'form-control',
                'disabled': True,
            }
            self.initial['periodo'] = Periodo.objects.get(estado=1)
            self.fields['labor'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
            self.initial['labor'] = Labor.objects.all().first()

        # habilitar, desabilitar, y mas

    class Meta:
        model = Asig_labor
        fields = [
            'fecha_asig',
            'periodo',
            'labor'
        ]
        labels = {
            'fecha_asig': 'Fecha de Asignacion',
            'periodo': 'Periodo',
            'labor': 'Labor'
        }
        widgets = {
            'fecha_asig': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            # 'periodo': forms.TextInput()
        }


class Asig_LaborForm_pag(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_asig'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['periodo'].widget.attrs = {
                'class': 'form-control',
                # 'value': Periodo.objects.get(estado=0),
                'disabled': True,
            }
            self.fields['labor'].widget.attrs = {
                'class': 'form-control',
                'disabled': True,
            }
            self.fields['trabajador'].widget.attrs = {
                'class': 'form-control',
                # 'value': Periodo.objects.get(estado=0),
                'disabled': True,
            }
            self.fields['estado'].widget.attrs = {
                'class': 'form-control selectpicker',
                'disabled': True,
                'data-style': 'btn-danger',
            }
            self.fields['desde'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['hasta'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['total_dias'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['valor_a_pag'].widget.attrs = {
                'class': 'form-control form-control-sm',
                'readonly': True,
            }
            self.fields['saldo'].widget.attrs = {
                'class': 'form-control form-control-sm',
                'readonly': True,
            }
            self.fields['valor_pag'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm'
            }

        # habilitar, desabilitar, y mas

    class Meta:
        model = Asig_labor
        fields = [
            'valor_pag',
            'valor_a_pag',
            'saldo',
            'trabajador',
            'fecha_asig',
            'periodo',
            'labor',
            'desde',
            'hasta',
            'total_dias',
            'estado'
        ]
        labels = {
            'fecha_asig': 'Fecha de Asignacion',
            'periodo': 'Periodo',
            'valor_pag': 'Valor',
            'valor_a_pag': 'Valor a Cancelar',
            'saldo': 'Saldo',
            'trabajador': 'Trabajador',
            'estado': 'Estado',
            'labor': 'Labor',
            'desde': 'Desde',
            'hasta': 'Hasta',
            'total_dias': 'Dias Laborados',
        }
        widgets = {
            'fecha_asig': forms.DateInput(),
            'periodo': forms.Select(),
            'estado': forms.Select(),
            'valor_a_pag': forms.TextInput(),
            'valor_pag': forms.TextInput(),
            'saldo': forms.TextInput(),
            'trabajador': forms.Select(),
            'labor': forms.Select(),
            'desde': forms.TextInput(),
            'hasta': forms.TextInput(),
            'total_dias': forms.TextInput()
        }
