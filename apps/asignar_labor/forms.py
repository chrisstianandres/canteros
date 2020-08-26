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
                # 'value': Periodo.objects.get(estado=0),
                'disabled': True,
            }
            self.initial['periodo'] = Periodo.objects.get(estado=1)
            self.fields['labor'].widget.attrs = {
                'class': 'form-control selectpicker',
                'data-live-search': "true",
                'data-width': "80%"
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

#
# class Asig_Labor_trabForm(forms.ModelForm):
#     # constructor
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.Meta.fields:
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#             })
#             self.fields['trabajador'].widget.attrs = {
#                 'class': 'form-control selectpicker',
#                 'data-live-search': "true"
#             }
#             self.fields["insumo"].queryset = Insumo.objects.filter(stock__gte=1)
#         # habilitar, desabilitar, y mas
#
#     class Meta:
#         model = Detalle_asig_insumo
#         fields = [
#             'insumo'
#         ]
