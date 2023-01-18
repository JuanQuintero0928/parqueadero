from django import forms
from .models import Categoria, RegistroEntrada, VehiculoRegistrado, Descuento

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['tipo','tarifa']
        labels = {
            'tipo':'Tipo Categoria',
            'tarifa':'Tarifa',
        }
        widgets = {
            'tipo': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese una categoria'
                }
            ),
            'tarifa': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese la tarifa'
                }
            )
        }

class VehiculoRegistradoForm(forms.ModelForm):
    class Meta:
        model = VehiculoRegistrado
        fields = ("tipo","placa","descuento")
        labels = {
            'tipo_id':'Tipo Vehiculo',
            'placa':'Placa',
            'descuento_id':'Descuento',
        }
        widgets = {
            'tipo_id': forms.SelectMultiple(),
            'placa': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese placa del vehiculo',
                }
            ),
            'descuento_id':forms.SelectMultiple(),
        }

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ("placa",)

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ("tipoDescuento","porcentaje")
        wigets = {
            'tipoDescuento': forms.TextInput(
                attrs={
                    'placeholder':'Nombre Descuento'
                }
            ),
            'porcentaje': forms.NumberInput()
        }
