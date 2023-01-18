from django.db import models
from datetime import datetime

# Create your models here.

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nit = models.CharField('Nit', max_length=11, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=50, blank=False, null=False)
    representanteLegal = models.CharField('Representante legal', max_length=200, blank=False, null=False)
    cuposMoto = models.IntegerField('Cupos Moto', blank=False, null=False)
    cuposCarro = models.IntegerField('Cupos Autos', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField('Tipo Vehiculo', max_length=50, blank=False, null=False)
    tarifa = models.IntegerField('Tarifa', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    def __str__(self):
        return self.tipo

class Descuento(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDescuento = models.CharField('Tipo Descuento', max_length=200, blank=False, null=False)
    porcentaje = models.IntegerField('Porcentaje', blank=False, null=False)

    def __str__(self):
        return self.tipoDescuento

class VehiculoRegistrado(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    placa = models.CharField('Placa', max_length=6, blank=False, null=False)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    class Meta:
        verbose_name = 'Vehiculo Registrado'
        verbose_name_plural = 'Vehiculos Registrados'
    
    def __str__(self):
        # return '{0},{1}'.format(self.placa,self.descuento)
        return self.placa

class RegistroEntrada(models.Model):
    # fechaActual = datetime.now()
    id = models.AutoField(primary_key=True)
    horaIngreso = models.DateTimeField('Fecha y Hora', auto_now=True, auto_now_add=False)
    placa = models.ForeignKey(VehiculoRegistrado, on_delete=models.CASCADE)
    estado = models.BooleanField('Activo/Desactivo', default=False)

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
    horaSalida = models.DateTimeField('Fecha y Hora', auto_now=True, auto_now_add=False)
    valorPagar = models.IntegerField('Valor a Pagar', blank=False, null=False)
    estado = models.BooleanField('Activo/Desactivo', default=True)

    def __str__(self):
        return self.registroEntrada