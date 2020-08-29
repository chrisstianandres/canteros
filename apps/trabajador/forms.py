from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Trabajador


class TrabajadorForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombres'].widget = TextInput(
                attrs={'placeholder': 'Ingrese los nombres del trabajador', 'class': 'form-control'})
            self.fields['apellidos'].widget = TextInput(
                attrs={'placeholder': 'Ingrese los apellidos del trabajador', 'class': 'form-control'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el numero de cedula del trabajador', 'class': 'form-control'})
            self.fields['correo'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control'})
            self.fields['telefono'].widget.attrs['placeholder'] = 'Ingrese un numero de telefono'
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese su direccion con maximo 50 caracteres', 'class': 'form-control'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = Trabajador
        fields = ['nombres',
                  'apellidos',
                  'cedula',
                  'genero',
                  'correo',
                  'telefono',
                  'direccion'
                  ]
        labels = {
            'nombres': 'Nombres',
            'apellidos': 'Apellidos',
            'cedula': 'N° de Cedula',
            'genero': 'Genero',
            'correo': 'Correo',
            'telefono': 'Telefono',
            'direccion': 'Direccion'

        }
        widgets = {
            'nombres': forms.TextInput(),
            'apellidos': forms.TextInput(),
            'cedula': forms.TextInput(),
            'genero': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'direccion': forms.TextInput()
        }
