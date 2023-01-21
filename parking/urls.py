from django.urls import path
from .views import ListarEmpresa, ListarCategoria, ListarVehiculoRegistrado, CrearCategoria, ListarRegistroEntrada, ListarDescuento, ListarFactura, crearFactura, CrearVehiculo, CrearRegistroEntrada, CrearDescuento, EditarCategoria, EditarDescuento, EditarVehiculo, crearRegistroEntrada, EditarEmpresa

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
    path('crear_registroEntrada/', crearRegistroEntrada, name='crear_registroEntrada'),
    path('crear_descuento/', CrearDescuento.as_view(), name='crear_descuento'),
    path('editar_categoria/<int:pk>', EditarCategoria.as_view(), name='editar_categoria'),
    path('editar_descuento/<int:pk>', EditarDescuento.as_view(), name='editar_descuento'),
    path('editar_vehiculo/<int:pk>', EditarVehiculo.as_view(), name='editar_vehiculo'),
    path('editar_empresa/<int:pk>', EditarEmpresa.as_view(), name='editar_empresa'),
]
