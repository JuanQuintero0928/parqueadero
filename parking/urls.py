from django.urls import path
from .views import ListarEmpresa, ListarCategoria, ListarVehiculoRegistrado, CrearCategoria, ListarRegistroEntrada, ListarDescuento, ListarFactura, crearFactura, CrearVehiculo, CrearRegistroEntrada, CrearDescuento

urlpatterns = [
    path('listar_empresa/', ListarEmpresa.as_view(), name='listar_empresa'),
    path('listar_categoria/', ListarCategoria.as_view(), name='listar_categoria'),
    path('crear_categoria/', CrearCategoria.as_view(), name='crear_categoria'),
    path('listar_vehiculosregistrados/', ListarVehiculoRegistrado.as_view(), name='listar_vehiculoregistrados'),
    path('registro_entrada/', ListarRegistroEntrada.as_view(), name='registro_entrada'),
    path('listar_descuento/', ListarDescuento.as_view(), name='listar_descuento'),
    path('crearFactura/<int:pk>', crearFactura, name='crearFactura'),
    path('listar_factura/', ListarFactura.as_view(), name='listar_factura'),
    path('crear_vehiculo/', CrearVehiculo.as_view(), name='crear_vehiculo'),
    path('crear_registroEntrada/', CrearRegistroEntrada.as_view(), name='crear_registroEntrada'),
    path('crear_descuento/', CrearDescuento.as_view(), name='crear_descuento'),
]
