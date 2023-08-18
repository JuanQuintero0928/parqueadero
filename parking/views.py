from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Empresa, Categoria, VehiculoRegistrado, RegistroEntrada, Descuento, Factura
from .forms import CategoriaForm, VehiculoRegistradoForm, RegistroEntradaForm, DescuentoForm, EmpresaForm, RegistroEntradaDeleteForm, FacturaForm, VehiculoConsultaForm
from datetime import datetime
import math

# Funcion para obtener el numero de vehiculos estacionados.
def cupoActual():
    cupoMoto = 0
    cupoCarro = 0
    cuposActual = VehiculoRegistrado.objects.filter(estadoParqueadero = True)
    for obj in cuposActual:
        if obj.tipo.cupoEspacio == 'moto':
            cupoMoto = cupoMoto + 1
        else:
            cupoCarro = cupoCarro + 1
    datos = {
        'moto':cupoMoto,
        'vehiculo':cupoCarro
    }
    return datos

class Inicio(TemplateView):
    def get(self, request, *args, **kwargs):
        dato = cupoActual()
        queryEmpresa = Empresa.objects.get(pk=1)
        cupoMoto = dato['moto']
        cupoCarro = dato['vehiculo']
        difMoto = queryEmpresa.cuposMoto - dato['moto']
        difCarro = queryEmpresa.cuposCarro - dato['vehiculo']
        datos = {
            'cupoMoto':cupoMoto,
            'cupoCarro':cupoCarro,
            'difMoto':difMoto,
            'difCarro':difCarro
        }
        return render(request, 'index.html', {'queryEmpresa':queryEmpresa, 'datos':datos})

class ListarEmpresa(ListView):
    model = Empresa
    template_name = 'parking/listar_empresa.html'
    context_object_name = 'empresas'
    queryset = Empresa.objects.filter(estado = True).order_by('pk')

class EditarEmpresa(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'parking/editar_empresa.html'
    success_url = reverse_lazy('parking:listar_empresa')

class ListarCategoria(ListView):
    model = Categoria
    template_name = 'parking/listar_categoria.html'
    context_object_name = 'categorias'
    queryset = Categoria.objects.filter(estado = True).order_by('pk')

class CrearCategoria(CreateView, SuccessMessageMixin):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'parking/crear_categoria.html'
    success_url = reverse_lazy('parking:listar_categoria')
    success_message = "Creado exitosamente"

class EditarCategoria(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'parking/crear_categoria.html'
    success_url = reverse_lazy('parking:listar_categoria')

class ListarVehiculoRegistrado(View):
    model = VehiculoRegistrado
    template_name = 'parking/listar_vehiculoregistro.html'

    def get(self, request, *args, **kwargs):
        form = VehiculoConsultaForm()
        query = self.model.objects.filter(estado =True).order_by('pk')
        paginator = Paginator(query,7)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        return render(request, self.template_name, {'datos':query, 'form': form})
    
    def post(self, request, *args, **kwargs):
        formulario = VehiculoConsultaForm(request.POST)
        if formulario.is_valid():
            placa = formulario.cleaned_data['placa'].upper()
            query = VehiculoRegistrado.objects.filter(placa__icontains = placa)
            return render(request, self.template_name, {'datos':query, 'form': formulario})
        else:
            print('placa no existe')
            form = VehiculoConsultaForm()
            query = self.model.objects.filter(estado =True).order_by('pk')
            return render(request, self.template_name, {'datos':query, 'form': form})


class CrearVehiculo(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': VehiculoRegistradoForm()}
        return render(request, 'parking/crear_vehiculoregistrado.html', context)

    def post(self, request, *args, **kwargs):
        try:
            formulario = VehiculoRegistradoForm(request.POST)
            if formulario.is_valid():
                obj = VehiculoRegistrado()
                obj.placa = formulario.cleaned_data['placa'].upper()                   # Si la placa se escribe en minusculas, la pasamos a mayusculas para realizar la consulta    
                query = VehiculoRegistrado.objects.filter(placa = obj.placa).count()   # Si la consulta no obtiene coincidencia automaticamente arroja error y entra al expecion que redirije al formulario
                if query == 0:
                    obj.tipo = formulario.cleaned_data['tipo']
                    obj.descuento = formulario.cleaned_data['descuento']
                    obj.save()
                    messages.info(request, 'Vehiculo creado exitosamente.')
                    return HttpResponseRedirect(reverse_lazy('parking:listar_vehiculoregistrados'))
                else:
                    messages.warning(request,'El vehiculo ya se encuentra en la base de datos.')
                    return render(request, 'parking/crear_vehiculoregistrado.html', {'form': formulario})
            else:
                messages.warning(request,'Falta informacion en el formulario.')
                return render(request, 'parking/crear_vehiculoregistrado.html',{'form': formulario})
        except Exception as e:
            messages.error(request,'Algo salio mal, contactar con el administrador.')
            return render(request, 'parking/crear_vehiculoregistrado.html', {'form': formulario})

class EditarVehiculo(UpdateView):
    # model = VehiculoRegistrado
    # form_class = VehiculoRegistradoForm
    # template_name = 'parking/crear_vehiculoregistrado.html'
    # success_url = reverse_lazy('parking:listar_vehiculoregistrados')

    def get(self, request, pk, *args, **kwargs):
        form_update = get_object_or_404(VehiculoRegistrado, pk=pk)          # Por medio del get_object_or_404, envio el modelo seguido de la validacion
        form = VehiculoRegistradoForm(initial={'tipo':form_update.tipo, 'placa':form_update.placa, 'descuento':form_update.descuento})  # Se inician las variables para mostrarlas en el formulario
        return render(request, 'parking/crear_vehiculoregistrado.html', {'form':form})
    
    def post(self, request, pk, *args, **kwargs):
        try:
            formulario = VehiculoRegistradoForm(request.POST)
            if formulario.is_valid():
                obj = VehiculoRegistrado.objects.get(pk=pk)                 # Obtengo el objeto a actualizar
                placaDigitada = formulario.cleaned_data['placa'].upper()    # Variable con placa digitada en mayuscula
                if obj.placa == placaDigitada:
                    obj.tipo = formulario.cleaned_data['tipo']
                    obj.descuento = formulario.cleaned_data['descuento']
                    obj.save()
                    messages.info(request, 'Vehiculo actualizado con exito.')
                    return HttpResponseRedirect(reverse_lazy('parking:listar_vehiculoregistrados'))
                else:
                    obj.placa = formulario.cleaned_data['placa'].upper()
                    obj.tipo = formulario.cleaned_data['tipo']
                    obj.descuento = formulario.cleaned_data['descuento']
                    obj.save()
                    messages.info(request, 'Vehiculo actualizado con exito.')
                    return HttpResponseRedirect(reverse_lazy('parking:listar_vehiculoregistrados'))
            else:
                messages.warning(request,'El vehiculo ya se encuentra en la base de datos.')
                return render(request,'parking/crear_vehiculoregistrado.html', {'form': formulario})
        except Exception as e:
            messages.error(request, 'Algo salio mal, contactar con el administrador.')
            return render(request, 'parking/crear_vehiculoregistrado.html', {'form': formulario})

class ListarRegistroEntrada(ListView):
    model = RegistroEntrada
    template_name = 'parking/listar_registroentrada.html'
    
    def get(self, request, *args, **kwargs):
        query = self.model.objects.filter(estado = False, eliminado = False)
        paginator = Paginator(query,7)
        page = request.GET.get('page')
        query = paginator.get_page(page)
        return render (request, self.template_name, {'datos':query})

class CrearRegistroEntrada(CreateView):
    # model = RegistroEntrada
    # form_class = RegistroEntradaForm
    # template_name = 'parking/crear_registroentrada.html'
    # success_url = reverse_lazy('parking:registro_entrada')

    def get(self, request, *args, **kwargs):
        formulario = RegistroEntradaForm()
        return render(request, 'parking/crear_registroentrada.html', {'form': formulario})
    
    def post(self, request, *args, **kwargs):
        formulario = RegistroEntradaForm(request.POST)
        try:
            if formulario.is_valid():
                placaEscrita = formulario.cleaned_data['placa'].upper()
                objVehiculo = VehiculoRegistrado.objects.get(placa = placaEscrita)          # Si la consulta no encuentra coincidencias, va al excepcion
                if objVehiculo.estadoParqueadero == False:
                    cuposTotal = Empresa.objects.get(pk=1)                                      #Solo sirve con una empresa
                    if objVehiculo.tipo_id == 1:                                                # Ojo, valor quemado
                        dato = cupoActual()                                                     # Funcion que calcula el numero de motos estacionadas actualmente
                        if dato['moto'] < cuposTotal.cuposMoto:
                            obj = RegistroEntrada()
                            obj.placa = objVehiculo
                            objVehiculo.estadoParqueadero = True
                            obj.save()                                                          # Objeto del modelo RegistroEntrada
                            objVehiculo.save()                                                  # Objeto del modelo Empresa
                            messages.info(request, 'Moto registrada con exito.')
                            return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
                        else:
                            messages.warning(request, 'Parqueadero lleno para motos')
                            return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
                    else:
                        dato = cupoActual()
                        if dato['vehiculo'] < cuposTotal.cuposCarro:
                            obj = RegistroEntrada()
                            obj.placa = objVehiculo
                            objVehiculo.estadoParqueadero = True
                            obj.save()
                            objVehiculo.save()
                            messages.info(request, 'Carro registrado con exito.')
                            return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
                        else:
                            messages.warning(request, 'Parqueadero lleno para carros')
                            return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
                else:
                    messages.warning(request,'El vehiculo ya esta dentro del parqueadero.')
                    return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
            else:
                messages.warning(request, 'Validar informacion suministrada en el formulario.')
                return render(request, 'parking/listar_registroentrada.html', {'form': formulario})
        except Exception as e:
            print(e)
            messages.warning(request, 'El vehiculo no se encuentra registrado.')
            return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))

class EliminarRegistroEntrada(DeleteView):
    model = RegistroEntrada
    template_name = 'parking/eliminar_registroEntrada.html'
    # success_url = reverse_lazy('parking:registro_entrada')

    def get(self, request, pk, *args, **kwargs):
        form = RegistroEntradaDeleteForm()
        return render(request, self.template_name, {'object': self.model.objects.get(pk=pk), 'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        formulario = RegistroEntradaDeleteForm(request.POST)
        if formulario.is_valid():
            objetoRegistro = RegistroEntrada.objects.get(pk=pk)
            objetoRegistro.observaciones = formulario.cleaned_data['observaciones']
            if not objetoRegistro.observaciones:
                messages.warning(request, 'Debe selecionar una opcion para la eliminación.')
                return render(request, 'parking/eliminar_registroEntrada.html', {'form': formulario})
            else:
                objetoRegistro.eliminado = True
                objetoRegistro.placa.estadoParqueadero = False
                objetoRegistro.save()
                objetoRegistro.placa.save()
                messages.info(request, 'Eliminado con exito')
                return HttpResponseRedirect(reverse_lazy('parking:registro_entrada'))
        else:
            messages.warning(request, 'Validar nuevamente el formulario')
            return render(request, self.template_name, {'object': self.model.objects.get(pk=pk), 'form': formulario})

class ListarDescuento(ListView):
    model = Descuento
    template_name = 'parking/listar_descuentos.html'
    context_object_name = 'descuentos'
    queryset = Descuento.objects.all().order_by('pk')

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

class CrearFactura(View):
    model = RegistroEntrada
    template_name = 'parking/facturar.html'

    def get(self, request, *args, **kwargs):
        form = FacturaForm()
        registroEntrada = self.model.objects.get(pk = kwargs['pk'])
        fechaActual = datetime.now()                                        # Fecha y Hora actual
        fechaIngreso = registroEntrada.horaIngreso                          #Se obtiene la hora de Ingreso
        diff = fechaActual - fechaIngreso
        minutos = (diff.seconds)/60                                         # Minutos que estuvo en parqueadero
        # Datos solo para mostrar en el template
        horasTemplate = math.floor(minutos/60)
        minutosTemplate = int(round((minutos % 60),0))
        horas = math.ceil(minutos/60)                                       # Horas en parqueadero redondeado hacia arriba
        if diff.days > 0:
            dias = diff.days
            pagar = int((((dias*24) + horas) * registroEntrada.placa.tipo.tarifa))
        else:
            pagar = int(horas * registroEntrada.placa.tipo.tarifa)
            dias = 0

        if registroEntrada.placa.descuento.porcentaje > 0:
            valorDescuento = int((pagar * registroEntrada.placa.descuento.porcentaje)/100)
            valorPagar = int(pagar-valorDescuento)
        else:
            valorPagar = int(pagar)
            valorDescuento = 0  

        datos = {'registroEntrada':registroEntrada,
            'fechaActual':fechaActual,
            'minutosTemplate':minutosTemplate,
            'horasTemplate':horasTemplate,
            'dias':dias,
            'pagar':pagar,
            'valorDescuento':valorDescuento,
            'valorPagar':valorPagar
        }
        print(round(valorPagar,0))
        return render(request, 'parking/facturar.html', {'datos':datos, 'form': form})

    def post(self, request, *args, **kwargs):
        formulario = FacturaForm(request.POST)
        if formulario.is_valid():
            valorPagar = formulario.cleaned_data['valorPagar']
            diasEstacionado = formulario.cleaned_data['diasEstacionado']
            horasEstacionado = formulario.cleaned_data['horasEstacionado']
            minutosEstaciondo = formulario.cleaned_data['minutosEstaciondo']
            valorSinDescuento = formulario.cleaned_data['valorSinDescuento']
            descuento = formulario.cleaned_data['descuento']
            fechaActual = datetime.now()                                        # Fecha y Hora actual
            registroEntrada = RegistroEntrada.objects.get(pk=kwargs['pk'])
            registroEntrada.estado = True
            registroEntrada.save()                                      
            registroEntrada.placa.estadoParqueadero = False                     # Objeto del vehiculo
            registroEntrada.placa.save()
            creacionfactura = Factura()                                         #Objeto de creacion de factura
            creacionfactura.horaSalida = fechaActual
            creacionfactura.valorPagar = valorPagar
            creacionfactura.diasEstacionado = diasEstacionado
            creacionfactura.horasEstacionado = horasEstacionado
            creacionfactura.minutosEstaciondo = minutosEstaciondo
            creacionfactura.valorSinDescuento = valorSinDescuento
            creacionfactura.descuento = descuento
            creacionfactura.estado = True
            creacionfactura.registroEntrada = RegistroEntrada.objects.get(pk=kwargs['pk'])
            creacionfactura.save()
            messages.info(request,'Factura realizada con exito.')
            return redirect('parking:registro_entrada')
        else:
            messages.warning(request,'No se pudo registrar la factura, comunicarse con el administrador.')
            return redirect('parking:registro_entrada')

# ------------------------EJEMPLO DE VISTAS BASADAS EN CLASES---------------------------------------------------
def crearRegistroEntrada(request):
    if request.method == 'POST':
        formulario = RegistroEntradaForm(request.POST)
        if formulario.is_valid():
            try:
                objeto = RegistroEntrada()
                placaEscrita = formulario.cleaned_data['placa']
                objetoVehiculo = VehiculoRegistrado.objects.get(placa = placaEscrita)
                objeto.placa = objetoVehiculo
                if objetoVehiculo.estadoParqueadero == True:
                    messages.warning(request,'El vehiculo esta dentro del parqueadero, validar información.')
                    return redirect('parking:crear_registroEntrada')
                else:
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
                            return redirect('parking:registro_entrada')
                        else:
                            messages.warning(request,'Parqueadero lleno para motos.')
                            return redirect('parking:crear_registroEntrada')
                    else:
                        cupoActualCarro = calculoParqCarro()
                        for cupo in cupoActualCarro.values():
                            cupoCarro = cupo
                        if cupoCarro < cupoTotal.cuposCarro:
                            objeto.save()           #Crea el registro entrada
                            objetoVehiculo.save()   #Actualiza el estado del vehiculo a true
                            messages.info(request,'Vehiculo registrada con exito.')
                            return redirect('parking:registro_entrada')
                        else:
                            messages.warning(request,'Parqueadero lleno para carro.')
                            return redirect('parking:crear_registroEntrada')
            except Exception as e:
                messages.warning(request,'El vehiculo no se encuentra registrado en la base de datos, primero debe crearlo para continuar con el proceso')
                return redirect('parking:crear_registroEntrada')
        else:
            messages.error(request,'Error al guardar la información, validar nuevamente los datos ingresados.')
            return redirect('parking:crear_registroEntrada')
    else:
        formulario = RegistroEntradaForm()
        return render(request, 'parking/crear_registroentrada.html', {'form':formulario})

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
