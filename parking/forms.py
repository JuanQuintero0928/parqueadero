from django import forms
from .models import Categoria, RegistroEntrada, Descuento, VehiculoRegistrado, Empresa

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

class RegistroEntradaForm(forms.Form):
    placa = forms.ModelChoiceField(queryset=VehiculoRegistrado.objects.filter(estadoParqueadero = False))

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ("tipoDescuento","porcentaje")
        widgets = {
            'tipoDescuento': forms.TextInput(
                attrs={
                    'placeholder':'Nombre Descuento'
                }
            ),
            'porcentaje': forms.NumberInput()
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ("nit","nombre","representanteLegal","cuposMoto","cuposCarro")
        labels = {
            'nit':'Nit',
            'nombre':'Nombre',
            'representanteLegal':'Representante Legal',
            'cuposMoto':'Cupos Moto',
            'cuposCarro':'Cupos Carro',
        }
        widgets = {
            'nit': forms.TextInput(),
            'nombre': forms.TextInput(),
            'representanteLegal': forms.TextInput(),
            'cuposMoto': forms.NumberInput(),
            'cuposCarro': forms.NumberInput(),
        }
