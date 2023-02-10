from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import ListarEmpresa, ListarCategoria, ListarVehiculoRegistrado, CrearCategoria, ListarRegistroEntrada, ListarDescuento, crearFactura, CrearVehiculo, CrearRegistroEntrada, CrearDescuento, EditarCategoria, EditarDescuento, EditarVehiculo, crearRegistroEntrada, EditarEmpresa, EliminarRegistroEntrada, CrearFactura

urlpatterns = [
    path('listar_empresa/', login_required(ListarEmpresa.as_view()), name='listar_empresa'),
    path('listar_categoria/', login_required(ListarCategoria.as_view()), name='listar_categoria'),
    path('crear_categoria/', login_required(CrearCategoria.as_view()), name='crear_categoria'),
    path('listar_vehiculosregistrados/', login_required(ListarVehiculoRegistrado.as_view()), name='listar_vehiculoregistrados'),
    path('registro_entrada/', login_required(ListarRegistroEntrada.as_view()), name='registro_entrada'),
    path('listar_descuento/', login_required(ListarDescuento.as_view()), name='listar_descuento'),
    path('crearFactura/<int:pk>', login_required(CrearFactura.as_view()), name='crearFactura'),
    path('crear_vehiculo/', login_required(CrearVehiculo.as_view()), name='crear_vehiculo'),
    path('crear_registroEntrada/', login_required(CrearRegistroEntrada.as_view()), name='crear_registroEntrada'),
    path('crear_descuento/', login_required(CrearDescuento.as_view()), name='crear_descuento'),
    path('editar_categoria/<int:pk>', login_required(EditarCategoria.as_view()), name='editar_categoria'),
    path('editar_descuento/<int:pk>', login_required(EditarDescuento.as_view()), name='editar_descuento'),
    path('editar_vehiculo/<int:pk>', login_required(EditarVehiculo.as_view()), name='editar_vehiculo'),
    path('editar_empresa/<int:pk>', login_required(EditarEmpresa.as_view()), name='editar_empresa'),
    path('eliminar_registroEntrada/<int:pk>', login_required(EliminarRegistroEntrada.as_view()), name='eliminar_registroEntrada'),
]
