from django.contrib import admin
from .models import Empresa, Categoria, VehiculoRegistrado, RegistroEntrada, Descuento, Factura

# Register your models here.

class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('nit','nombre','representanteLegal','cuposMoto','cuposCarro','estado',)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ['tipo']
    list_display = ('tipo','tarifa','estado',)

class VehiculoAdmin(admin.ModelAdmin):
    search_fields = ['placa']
    list_display = ('tipo','placa','descuento','estado','estadoParqueadero')

class RegistroEntradaAdmin(admin.ModelAdmin):
    list_display = ('horaIngreso','placa','estado',)

class DescuentoAdmin(admin.ModelAdmin):
    search_fields = ['tipoDescuento']
    list_display = ('tipoDescuento','porcentaje',)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('registroEntrada','horaSalida','valorPagar','estado')

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(VehiculoRegistrado, VehiculoAdmin)
admin.site.register(RegistroEntrada, RegistroEntradaAdmin)
admin.site.register(Descuento, DescuentoAdmin)
admin.site.register(Factura, FacturaAdmin)
