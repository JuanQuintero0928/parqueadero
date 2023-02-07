from django.db import models
from datetime import datetime

# Create your models here.

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nit = models.CharField('Nit', max_length=11, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=50, blank=False, null=False, unique=True)
    representanteLegal = models.CharField('Representante legal', max_length=200, blank=False, null=False)
    cuposMoto = models.PositiveIntegerField('Cupos Moto', blank=False, null=False)
    cuposCarro = models.PositiveIntegerField('Cupos Autos', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)
    direccion = models.CharField('Direccion', max_length=100, default="")
    ciudad = models.CharField('Ciudad/Dpto', max_length=100, default="")

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    opciones = (
        ("moto","Motocicleta"),
        ("vehiculo","Vehiculo")
    )
    id = models.AutoField(primary_key=True)
    tipo = models.CharField('Tipo Vehiculo', max_length=50, blank=False, null=False, unique=True)
    tarifa = models.FloatField('Tarifa', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)
    cupoEspacio = models.CharField('Ocupa espacio de :', choices=opciones, max_length=20)

    def __str__(self):
        return self.tipo

class Descuento(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDescuento = models.CharField('Tipo Descuento', max_length=200, blank=False, null=False, unique=True)
    porcentaje = models.FloatField('Porcentaje', blank=False, null=False)

    def __str__(self):
        return self.tipoDescuento

class VehiculoRegistrado(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    placa = models.CharField('Placa', max_length=6, blank=False, null=False)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE)
    estadoParqueadero = models.BooleanField('In/Out', default=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    class Meta:
        verbose_name = 'Vehiculo Registrado'
        verbose_name_plural = 'Vehiculos Registrados'
    
    def __str__(self):
        # return '{0},{1}'.format(self.placa,self.descuento)
        return self.placa

class OpcionesEliminacion(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.TextField('Descripcion', blank=False, null=False)

    class Meta:
        verbose_name = 'Opciones de Eliminacion'
        verbose_name_plural = 'Opciones de Eliminacion'
        ordering = ['pk']

    def __str__(self):
        return self.descripcion

class RegistroEntrada(models.Model):
    # fechaActual = datetime.now()
    id = models.AutoField(primary_key=True)
    horaIngreso = models.DateTimeField('Fecha y Hora', auto_now=False, auto_now_add=True)
    placa = models.ForeignKey(VehiculoRegistrado, on_delete=models.CASCADE)
    estado = models.BooleanField('Activo/Desactivo', default=False)
    eliminado = models.BooleanField('Eliminado', default=False)
    observaciones = models.ForeignKey(OpcionesEliminacion, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Registro Entrada'
        verbose_name_plural = 'Registros de Entradas'
        ordering = ['pk']
    
    def __str__(self):
        return '{0},{1}'.format(self.placa, self.horaIngreso)
        # return self.placa

class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    registroEntrada = models.ForeignKey(RegistroEntrada, on_delete=models.CASCADE)
    horaSalida = models.DateTimeField('Fecha y Hora', auto_now=False, auto_now_add=True)
    valorPagar = models.FloatField('Valor a Pagar', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    def __str__(self):
        return self.registroEntrada