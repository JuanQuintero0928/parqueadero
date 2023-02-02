from django import forms
from .models import Categoria, RegistroEntrada, Descuento, VehiculoRegistrado, Empresa

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['tipo','tarifa','cupoEspacio']
        labels = {
            'tipo':'Tipo Categoria',
            'tarifa':'Tarifa',
            'cupoEspacio':'Ocupa espacio de',
        }
        widgets = {
            'tipo': forms.TextInput(
                attrs={
                    'placeholder':'...',
                    'class':'form-control cont-capitalize'
                }
            ),
            'tarifa': forms.NumberInput(
                attrs={
                    'placeholder':'$',
                    'min':0,
                    'class':'form-control'
                }
            ),
            'cupoEspacio': forms.Select(
                attrs={
                    'class':'form-control'
                }
            )
        }

class VehiculoRegistradoForm(forms.ModelForm):
    class Meta:
        model = VehiculoRegistrado
        fields = ('tipo',"placa","descuento")
        labels = {
            'tipo':'Tipo Vehiculo',
            'placa':'Placa',
            'descuento':'Descuento',
        }
        widgets = {
            'tipo': forms.Select(
                attrs={
                    'class':'form-control'
                }
            ),
            'placa': forms.TextInput(
                attrs={
                    'placeholder':'...',
                    'class':'form-control cont-uppercase'
                }
            ),
            'descuento':forms.Select(
                attrs={
                'class':'form-control'
                }
            ),
        }

class RegistroEntradaForm(forms.Form):
    placa = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control cont-uppercase','maxlength':'6','placeholder':'Example : AAA123'}))
    # placa = forms.ModelChoiceField(queryset=VehiculoRegistrado.objects.filter(estadoParqueadero = False))
    # # CHOICES = queryset=VehiculoRegistrado.objects.all()
    # CHOICES = [('1', 'First'), ('2', 'Second')]
    # placa = forms.TextInput(choices=CHOICES)
    # placa.choices

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ("tipoDescuento","porcentaje")
        widgets = {
            'tipoDescuento': forms.TextInput(
                attrs={
                    'placeholder':'...',
                    'class':'form-control'
                }
            ),
            'porcentaje': forms.NumberInput(
                attrs={
                    'placeholder':'%',
                    'min':0,
                    'class':'form-control'
                }
            )
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
            'nit': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'representanteLegal': forms.TextInput(
                attrs={
                        'class':'form-control'
                    }
            ),
            'cuposMoto': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'cuposCarro': forms.NumberInput(
                attrs={
                    'class':'form-control'
                }
            ),
        }

class RegistroEntradaDeleteForm(forms.ModelForm):
    class Meta:
        model = RegistroEntrada
        fields = ['observaciones']
        labels = {
            'observaciones':'¿Motivo de la eliminación?'
        }
        widgets = {
            'observaciones': forms.Select(
                attrs={
                    'class':'form-control'
                }
            )
        }
