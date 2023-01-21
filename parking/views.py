from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Empresa, Categoria, VehiculoRegistrado, RegistroEntrada, Descuento, Factura
from .forms import CategoriaForm, VehiculoRegistradoForm, RegistroEntradaForm, DescuentoForm, EmpresaForm
from datetime import datetime
import math

# Create your views here.

def calculoParqCarro():
    objCarro = VehiculoRegistrado.objects.filter(estadoParqueadero = True).exclude(tipo_id = 1)
    numCarros = len(objCarro)
    datoCarro = {'numCarros':numCarros}
    return (datoCarro)

def calculoParqMoto():
    objMoto = VehiculoRegistrado.objects.filter(estadoParqueadero = True, tipo_id = 1)
    numMotos = len(objMoto)
    datosMoto ={'numMotos':numMotos}
    return (datosMoto)

class Inicio(TemplateView):
    template_name = 'index.html'

def inicio(request):
    datoMoto = calculoParqMoto()
    datoCarro = calculoParqCarro()
    return render(request, 'index.html', {'datoMoto':datoMoto,'datoCarro':datoCarro})

class ListarEmpresa(ListView):
    model = Empresa
    template_name = 'parking/listar_empresa.html'
    context_object_name = 'empresas'
    queryset = Empresa.objects.filter(estado = True)

class EditarEmpresa(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'parking/editar_empresa.html'
    success_url = reverse_lazy('parking:listar_empresa')

class ListarCategoria(ListView):
    model = Categoria
    template_name = 'parking/listar_categoria.html'
    context_object_name = 'categorias'
    queryset = Categoria.objects.filter(estado = True)

class CrearCategoria(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'parking/crear_categoria.html'
    success_url = reverse_lazy('parking:listar_categoria')

class EditarCategoria(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'parking/crear_categoria.html'
    success_url = reverse_lazy('parking:listar_categoria')

class ListarVehiculoRegistrado(ListView):
    model = VehiculoRegistrado
    template_name = 'parking/listar_vehiculoregistro.html'
    context_object_name = 'vehiculosregistrados'
    queryset = VehiculoRegistrado.objects.filter(estado = True)

class CrearVehiculo(CreateView):
    model = VehiculoRegistrado
    form_class = VehiculoRegistradoForm
    template_name = 'parking/crear_vehiculoregistrado.html'
    success_url = reverse_lazy('parking:listar_vehiculoregistrados')

class EditarVehiculo(UpdateView):
    model = VehiculoRegistrado
    form_class = VehiculoRegistradoForm
    template_name = 'parking/crear_vehiculoregistrado.html'
    success_url = reverse_lazy('parking:listar_vehiculoregistrados')

class ListarRegistroEntrada(ListView):
    model = RegistroEntrada
    template_name = 'parking/listar_registroentrada.html'
    context_object_name = 'registrosentradas'
    queryset = RegistroEntrada.objects.filter(estado = False)

class CrearRegistroEntrada(CreateView):
    model = RegistroEntrada
    form_class = RegistroEntradaForm
    template_name = 'parking/crear_registroentrada.html'
    success_url = reverse_lazy('parking:registro_entrada')

    def _get_queryset(self):    # Retorna la consulta
        return self.model.objects.filter(estado=False)

    def get_context_data(self, **kwargs):   #Retorna la informacion que va hacer enviada al Template
        # estado = VehiculoRegistrado()
        # estado.estadoParqueadero = True
        context = {}
        context['registros'] = self._get_queryset
        context['form'] = self.form_class   #Envio el formulario al template
        context['model'] = self.model
        return context
    
    def get(self, request, *args, **kwargs):    # Retorna toda la informacion cuando se hace la peticion
        return render(request, self.template_name, self.get_context_data())
    
def crearRegistroEntrada(request):
    if request.method == 'POST':
        formulario = RegistroEntradaForm(request.POST)
        if formulario.is_valid():
            objeto = RegistroEntrada()
            objeto.placa = formulario.cleaned_data['placa']
            objetoVehiculo = VehiculoRegistrado.objects.get(placa = objeto.placa)
            objetoVehiculo.estadoParqueadero = True
            cupoTotal = Empresa.objects.get(pk = 1)
            if objetoVehiculo.tipo_id == 1:
                cupoActualMoto = calculoParqMoto()
                for cupo in cupoActualMoto.values():
                    cupoMoto = cupo
                if cupoMoto < cupoTotal.cuposMoto:
                    objeto.save()           #Crea el registro entrada
                    objetoVehiculo.save()   #Actualiza el estado del vehiculo a true
                    messages.info(request,'Moto registrada con exito.')
                    return redirect('parking:crear_registroEntrada')
                else:
                    messages.error(request,'Parqueadero lleno para motos.')
                    return redirect('parking:crear_registroEntrada')
            else:
                cupoActualCarro = calculoParqCarro()
                for cupo in cupoActualCarro.values():
                    cupoCarro = cupo
                if cupoCarro < cupoTotal.cuposCarro:
                    objeto.save()           #Crea el registro entrada
                    objetoVehiculo.save()   #Actualiza el estado del vehiculo a true
                    messages.info(request,'Vehiculo registrada con exito.')
                    return redirect('parking:crear_registroEntrada')
                else:
                    messages.error(request,'Parqueadero lleno para carro.')
                    return redirect('parking:crear_registroEntrada')
        else:
            messages.error(request,'Error al guardar la información, validar nuevamente los datos ingresados.')
            return redirect('parking:crear_registroEntrada')
    else:
        formulario = RegistroEntradaForm()
        return render(request, 'parking/crear_registroentrada.html', {'form':formulario})

class ListarDescuento(ListView):
    model = Descuento
    template_name = 'parking/listar_descuentos.html'
    context_object_name = 'descuentos'
    queryset = Descuento.objects.all()

class CrearDescuento(CreateView):
    model = Descuento
    form_class = DescuentoForm
    template_name = 'parking/crear_descuento.html'
    success_url = reverse_lazy('parking:listar_descuento')

class EditarDescuento(UpdateView):
    model = Descuento
    form_class = DescuentoForm
    template_name = 'parking/crear_descuento.html'
    success_url = reverse_lazy('parking:listar_descuento')

class ListarFactura(ListView):
    model = Factura
    template_name = 'parking/listar_factura.html'
    context_object_name = 'facturas'
    queryset = Factura.objects.all()

# ---------------------------------------------------------------------------
#Queda pendiente el modulo de facturas hacerlo por medio de una clase
class CrearFactura(ListView):
    model = RegistroEntrada
    template_name = 'parking/listar_factura.html'
    context_object_name = 'facturar'
    queryset = Descuento.objects.all()

def crearFactura(request, pk):
    factura = RegistroEntrada.objects.get(pk =pk)
    idVehiculo = VehiculoRegistrado.objects.get(pk = factura.placa_id)
    idDesuento = Descuento.objects.get(pk = idVehiculo.descuento_id) # Se obtiene el id del descuento
    idTarifa = Categoria.objects.get(pk = idVehiculo.tipo_id)
    fechaActual = datetime.now() # Fecha y Hora actual
    fechaIngreso = factura.horaIngreso #Se obtiene la hora de Ingreso
    diff = fechaActual - fechaIngreso
    minutos = (diff.seconds)/60 # Minutos que estuvo en parqueadero
    # Datos solo para mostrar en el template
    horasTemplate = math.floor(minutos/60)
    minutosTemplate = round((minutos % 60),0)
    horas = math.ceil(minutos/60) # Horas en parqueadero redondeado hacia arriba

    if diff.days > 0:
        dias = diff.days
        pagar = (((dias*24) + horas) * idTarifa.tarifa)
    else:
        pagar = horas * idTarifa.tarifa
        dias = 0

    if idDesuento.porcentaje > 0:
        valorDescuento = (pagar * idDesuento.porcentaje)/100
        valorPagar = pagar-valorDescuento
    else:
        valorPagar = pagar
        valorDescuento = 0
        
    datos = {'factura':factura,
        'idVehiculo':idVehiculo,
        'idTarifa':idTarifa,
        'idDescuento':idDesuento,
        'fechaActual':fechaActual,
        'minutosTemplate':minutosTemplate,
        'horasTemplate':horasTemplate,
        'dias':dias,
        'pagar':pagar,
        'valorDescuento':valorDescuento,
        'valorPagar':valorPagar
    }
    if request.method == 'POST':
        factura.estado = True
        factura.save()
        idVehiculo.estadoParqueadero = False
        creacionfactura = Factura()
        creacionfactura.horaSalida = fechaActual
        creacionfactura.valorPagar = valorPagar
        creacionfactura.estado = True
        creacionfactura.registroEntrada = RegistroEntrada.objects.get(pk=pk)
        creacionfactura.save()
        idVehiculo.save()
        messages.info(request,'Factura realizada con exito.')
        return redirect('parking:registro_entrada')
    return render(request, 'parking/facturar.html', {'datos':datos})
